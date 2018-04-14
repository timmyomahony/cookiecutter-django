# New Server Setup

## Create a user

```sh
$ apt-get install sudo
$ adduser --home /home/admin/ --shell /bin/bash admin
```

If you get the error:

```sh
adduser: The group `admin` already exists.

when adding a user, include the flag `--ingroup admin`:

```sh
$ adduser --home /home/admin/ --shell /bin/bash admin --ingroup admin
```

add the group to sudoers

```sh
$ addgroup admin sudo
```

Then switch to the user:

```sh
$ su admin
```

and go home:

```sh
$ cd ~/
```

## Update OS

Update:

```sh
$ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dselect-upgrade
```

## Install dependencies

```sh
$ sudo apt-get install vim git docker docker-compose supervisor 
```
## Configure git

```sh
$ sudo git config --global user.name "Timmy O'Mahony"
$ sudo git config --global user.email "hey@timmyomahony.com"
$ sudo git config --global core.editor "vim"
```

## Add SSH key

Once you have access to the new server (usually via username/password), you
need to add your own personal public key to the server so that you can access
it over SSH (in the next step, we'll disable password access)

*On your machine*, if you don't already have one, create a public/private key
pair and **make sure to use a passphase**

```sh
$ ssh-keygen -t rsa -b 4096
```

Copy the contents of the *public key*:

```sh
$ cat ~/.ssh/id_rsa.pub
```

*Back on the server*, add the public key to the `~/.ssh/authorized_keys` file:

```sh
$ vim ~/.ssh/authorized_keys
```

and update the permissiones

```sh
$ chmod 0600 ~/.ssh/authorized_keys
```

Make sure there aren't any spaces around the public key, or any blanks lines.

You should now be able to log out of the server, and log in again with you 
key:

```sh
$ ssh -i ~/.ssh/id_rsa {{ cookiecutter.email }}
```

## Update SSH configuration

Restrict SSH login to public/private key only. Open the SSH config:

```sh
$ vim /etc/ssh/sshd_config
```

Uncomment:

```sh
AuthorizedKeysFile     %h/.ssh/authorized_keys
```

Change the default port:

```sh
Port 30000
```

Disable password login:

```sh
PasswordAuthentication no
```

Prevent root login:

```sh
PermitRootLogin no
```

Enable key login

```sh
PubkeyAuthentication yes
```

Restart SSH:

```sh
$ service ssh restart
```

## Add Github deployment key

To be able to get the codebase, we need to create a public/private key pair on
the server. **The private key should never leave the server, so make sure to 
generate it on the server, not locally on your laptop**

```sh
$ ssh-keygen -t rsa -b 4096
```

Copy the contents of the *public key*:

```sh
$ cat ~/.ssh/id_rsa.pub
```

Now add a new "Deployment Key" via Github

- https://github.com/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/settings/keys

And paste in the public key for the server.

On the server, open/create the SSH config file:

```sh
$ vim ~/.ssh/config
```

and add the following:

```
Host github.com
    User git
    IdentityFile ~/.ssh/id_rsa
```

## Clone the repo

```sh
$ cd ~/
$ git clone git@github.com:{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.git
$ cd {{ cookiecutter.project_slug }}
```

## Setup accounts

For deployment, you need accounts with:

- Amazon AWS (for asset hosting)
- Sentry.io (for errors)
- Mailgun (for emails)

So make sure those are created and configured.

### Setup AWS Bucket

Create a new bucket and add the following policy:

```json
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "PublicReadForGetBucketObjects",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{{ cookiecutter.project_slug }}/*"
        }
    ]
}
```

and the following CORS configuration:

```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>Authorization</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

## Add environment variables

```sh
$ cp env.example .env
```

```
POSTGRES_PASSWORD=...  # make sure there's no colons
POSTGRES_USER={{ cookiecutter.project_slug }}
CONN_MAX_AGE=60

# Domain name, used by caddy
DOMAIN_NAME={{ cookiecutter.domain_name }}

# General settings
# DJANGO_READ_DOT_ENV_FILE=True
DJANGO_ADMIN_URL=admin-dashboard/
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=...
DJANGO_ALLOWED_HOSTS={{ cookiecutter.domain_name }}

# AWS Settings
DJANGO_AWS_ACCESS_KEY_ID=
DJANGO_AWS_SECRET_ACCESS_KEY=
DJANGO_AWS_STORAGE_BUCKET_NAME={{ cookiecutter.project_name }}

# Used with email
DJANGO_MAILGUN_API_KEY=key-xxx
DJANGO_SERVER_EMAIL={{ cookiecutter.email }}
MAILGUN_SENDER_DOMAIN=mg.{{ cookiecutter.domain_name }}

# Security! Better to use DNS for this task, but you can use redirect
DJANGO_SECURE_SSL_REDIRECT=False

# Sentry
DJANGO_SENTRY_DSN=...
```

## Setup Docker

Add our user to the `docker` group:

```sh
$ sudo usermod -aG docker admin
```

Build the Docker image (this will take a while):

```sh
$ sudo docker-compose -f production.yml build
```

## Setup Django

Migrate the DB

```sh
$ sudo docker-compose -f production.yml run django python manage.py migrate
```

Collect the static files

```sh
$ sudo docker-compose -f production.yml run django python manage.py collectstatic --noinput
```

## Setup Supervisor

We need a process manager to start/stop the docker containers.

First, make its possible to restart  the supervisor processes as a non-root user
by editing `/etc/supervisor/supervisor.conf` file and adding the following:

```
[unix_http_server]
file=/var/run/supervisor.sock
...
chown=admin:admin

...

[supervisorctl]
serverurl = unix:///var/run/supervisor.sock
```

hen make sure to create the socket file:

```
sudo touch /var/run/supervisor.sock
sudo chown admin:admin /var/run/supervisor.sock
```

Create a new config:

```sh
$ sudo vim /etc/supervisor/conf.d/{{ cookiecutter.project_slug }}.conf
```

and add the following:

```
[program:{{ cookiecutter.project_slug }}]
command=docker-compose -f production.yml up --build
directory=/home/admin/{{ cookiecutter.project_slug }}
user=admin
redirect_stderr=true
autostart=true
autorestart=true
priority=10
```

then start it

```sh
$ supervisorctl reread
```

```sh
$ supervisorctl update
```

and check the status

```sh
$ supervisorctl status
```

## Resources

This deployment is based on the default `django-cookiecutter` Docker deployement
strategy, so more information can be found here:

- https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

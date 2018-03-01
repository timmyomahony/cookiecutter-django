# Local development

## Clone the repo

The first step is to clone the repo to you machine: 

```sh
$ git clone git@github.com:{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.git
$ cd {{ cookiecutter.project_slug }}
```

## Install Docker

Make sure you have Docker installed on your machine. On Ubuntu this should
be easy:

```sh
$ sudo apt-get install docker docker-compose
```

On Windows of Mac, you need to install the Docker deskop pacakges from here:

- https://docs.docker.com/engine/installation/

## Setup Docker

First build the Docker images (this will take a while):

```sh
$ docker-compose -f local.yml build
```

then start the Docker containers:

```sh
$ docker-compose -f local.yml up
```

This should automatically start everything required to work on the site.

Launch the browser at:

```sh
http://localhost:3000
```

Any changes to the SCSS and JS files should automatically reload the browser 
window so development should be easy.

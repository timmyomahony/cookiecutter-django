# Deployment Configuration

These are the step required to get an easy deployment configuration set up:

- Deployment with CircleCI
- Github notifications to Slack channel
- Sentry notifications to Slack channel
- CircleCI notifications to Slack channel

## CircleCI build and deployment

There is already a `.circleci` folder in the repo that is configured to build, test and deploy the codebase automatically via the `.config.yml` configuration file.

### Fabric Deployment

The actual deployment step is handled by a simple `deploy.py` [Fabric](http://www.fabfile.org/) script. This requires that we add a new public/private key pair that allows the CircleCI *build* server to login to our *deployment* server remotely.

Generate a new keypair on the local machine:

```sh
ssh-keygen -t rsa -b 4096 -C root@circleci 
```

In CircleCI dashboard, go to the settings for the new project. In "SSH Permissions", add a new SSH key and paste in the **private** key.

On the deployment server, add the **public** key to the `~/.ssh/authorized_keys`

### Slack notifications

You can add CircleCI notifications to a particular Slack channel. First enable the CircleCI integration by going to the apps section of your Slack org:

- https://weareferal.slack.com/apps

and enabling it. In the configuration, you'll get a webhook address. For example: 

```
https://hooks.slack.com/services/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
```

Add this to the "Notifications > Chat Notifications" of the CirlceCI project's settings.  

## Sentry Slack notifications

First, like the CircleCI integration, go to the "browse apps" section of the Slack organisation and add the Sentry integration. This will generate a webhook like:

```
https://hooks.slack.com/services/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
```

Then, on the settings page of the Sentry project, go to "Integrations > Add Integration" in the left hand sidebar. Search for "Slack" and hit "configure plugin". Add the webook URL and hit save. 

## Circle CI notifications
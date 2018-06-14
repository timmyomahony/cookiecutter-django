# Deployment Configuration

These are the step required to get an easy deployment configuration set up:

1. Deployment with CircleCI
2. CircleCI notifications to Slack channel
3. Sentry notifications to Slack channel
4. Github notifications to Slack channel

## 1. Deployment with CircleCI

There is already a `.circleci` folder in the repo that is configured to build, test and deploy the codebase automatically via the `.config.yml` configuration file.

### Fabric Deployment

The actual deployment step is handled by a simple `deploy.py` [Fabric](http://www.fabfile.org/) script. This requires that we add a new public/private key pair that allows the CircleCI *build* server to login to our *deployment* server remotely.

Generate a new keypair on the **local** machine:

```sh
ssh-keygen -t rsa -b 4096 -C root@circleci 
```

In CircleCI dashboard, go to the settings for the new project. In "SSH Permissions", add a new SSH key and paste in the **private** key (call it "CircleCI")

On the deployment server, add the **public** key to the `~/.ssh/authorized_keys`

## 2. CircleCI Slack notifications

- https://circleci.com/blog/slack-integration/

You can add CircleCI notifications to a particular Slack channel. 

Enable the CircleCI integration by going to the apps section of your Slack org:

- https://weareferal.slack.com/apps

If not already added, add "CircleCI". If already added, click "Manage" in the top right of the screen. 

Get a webhook address for the relevent channel you want to post to. For example: 

```
https://hooks.slack.com/services/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
```

Add this to the "Notifications > Chat Notifications" of the CirlceCI project's settings.  

## 3. Sentry Slack notifications

- https://docs.sentry.io/integrations/slack/

This works be allowing Sentry to post to your Slack account (as opposed to having to allow the reverse where Slack can read your Sentry data). __This only has to be done once per Slack account/Sentry Org. Once enabled you can change what gets posted to Slack via Slash commands__

## 4. Github Slack notifications

- https://get.slack.help/hc/en-us/articles/232289568-GitHub-for-Slack

This works be allowing Github to post to your Slack account (as opposed to having to allow the reverse where Slack can read your Github data). __This only has to be done once per Slack account/Github Org. Once enabled you can change what gets posted to Slack via Slash commands__

# Deployment Configuration

These are the step required to get an easy deployment configuration set up:

- Deployment with CircleCI
- Github notifications to Slack channel
- Sentry notifications to Slack channel
- CircleCI notifications to Slack channel

## CircleCI

There is already a `.circleci` folder in the repo that is configured to build, test and deploy the codebase automatically via the `.config.yml` configuration file.

The actual deployment step is handled by a simple [Fabric](http://www.fabfile.org/) script. This requires that we add a new public/private key pair that allows the CircleCI *build* server to *login* to our deployement server remotely.

Generate a new keypair on the local machine:

```sh

```

Then in CircleCI, go to the settings for the new project. In "SSH Permissions", add a new SSH key and paste in the **private** key.

On the deployment server, add the **private** key to the `~/.ssh/authorized_keys`

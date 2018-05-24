#!/usr/bin/python2

from fabric.api import env, run, cd, task, sudo

debug = False

"""
Deploy

Deploying new code is as easy as restarting the docker-compose process that
is being run by supervisor. This automatically migrates the DB and collects
static files.
"""

if debug:
    import paramiko
    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

env.user = 'admin'
env.hosts = []
env.compose_config = 'production.yml'
env.app = '/home/admin/{{cookiecutter.project_slug}}/'
    

@task
def production():
    env.branch = 'master'
    env.hosts = ['{{cookiecutter.domain_name}}.com:30000', ]


@task
def staging():
    env.branch = 'develop'
    env.hosts = ['{{cookiecutter.domain_name}}.com:30000', ]


@task
def checkout_code():
    run('git fetch && git checkout {0} && git pull origin {0}'.format(env.branch))


@task
def restart_app():
    run('supervisorctl restart {{cookiecutter.project_slug}}')


@task
def deploy():
    with cd(env.app):
        checkout_code()
        restart_app()

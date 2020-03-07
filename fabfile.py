#!/usr/bin/env python
# coding=utf-8
from fabric.api import env, hide
from fabric.decorators import task
from fabric.operations import run
from fabric.context_managers import cd

env.forward_agent = True
env.use_ssh_config = True


@task
def production():
    env.branch = 'master'
    env.hosts = ['starenka@starenka.net']
    env.project_dir = '/www/neblabolit.starenka.net'


@task
def deploy():
    with cd(env.project_dir):
        with hide('stdout'):
            run('git fetch')
            run('git reset --hard origin/%s' % env.branch)
        run('.env/bin/pip install -r requirements.pip')
        run('sudo supervisorctl restart neblabolit.starenka.net')

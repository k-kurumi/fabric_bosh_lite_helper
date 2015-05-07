#!/usr/bin/env python
# coding: utf-8

from fabric.api import sudo, task
from fabric.contrib import files

def update():
  sudo('DEBIAN_FRONTEND=noninteractive apt-get update')

def upgrade():
  update()
  sudo('DEBIAN_FRONTEND=noninteractive apt-get -qy upgrade')

def install(pkg_str=""):
  update()
  sudo('DEBIAN_FRONTEND=noninteractive apt-get install -qy %s' % " ".join(pkg_str.split()))

def build_dep(pkg):
  if not files.exists('/etc/apt/sources.list.d/mydep.list'):
    sudo('''echo 'deb-src http://jp.archive.ubuntu.com/ubuntu/ trusty main universe multiverse' > /etc/apt/sources.list.d/mydep.list''')

  update()
  sudo('DEBIAN_FRONTEND=noninteractive apt-get build-dep -qy %s' % pkg)

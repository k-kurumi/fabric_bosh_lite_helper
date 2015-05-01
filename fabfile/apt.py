#!/usr/bin/env python
# coding: utf-8

from fabric.api import sudo, task

def update():
  sudo('DEBIAN_FRONTEND=noninteractive apt-get update')

def upgrade():
  update()
  sudo('DEBIAN_FRONTEND=noninteractive apt-get -qy upgrade')

def install(pkg_str=""):
  update()
  sudo('DEBIAN_FRONTEND=noninteractive apt-get install -qy %s' % " ".join(pkg_str.split()))

def build_dep(pkg):
  update()
  sudo('DEBIAN_FRONTEND=noninteractive apt-get build-dep -qy %s' % pkg)

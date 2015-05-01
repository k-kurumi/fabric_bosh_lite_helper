#!/usr/bin/env python
# coding: utf-8

from fabric.api import env, sudo, task

@task
def file(filename):
  u'''
  fab -H <host> tail.file:/var/log/syslog
  host上のログファイルをtail -Fする
  '''
  env.output_prefix = False
  sudo('tail -F ' + filename)

@task
def job(jobname):
  u'''
  fab -H <host> tail.job:warden
  ジョブ名指定でgostenoする
  '''
  path = '/var/vcap/sys/log/%s/%s.log' % (jobname, jobname)
  sudo('tail -F %s | gosteno-prettify' % path)

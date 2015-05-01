#!/usr/bin/env python
# coding: utf-8

from fabric.api import env, sudo, get, task

import shutil
import os
import json

def get_json():
  get('/var/vcap/data/dea_next/db/instances.json', use_sudo=True)


def print_warden():
  for dirname in env.hosts:
    j = os.path.join(dirname, 'instances.json')

    if os.path.exists(j):
      with open(j) as fp:
        data = json.load(fp)

        for instance in data['instances']:
          name   = instance['application_name']
          guid   = instance['application_id']
          handle = instance['warden_handle']
          state  = instance['state']

          print handle, name, guid, state


def delete_json():
  for dirname in env.hosts:
    if os.path.exists(dirname):
      shutil.rmtree(dirname)


@task
def pp():
  u'''
  fab -H <host> warden.pp
  アプリのハンドル一覧を表示する
  '''
  delete_json()
  get_json()
  print_warden()


@task
def login(handle):
  u'''
  fab -H <host> warden.login:hdfjariej
  wardenのハンドルを指定してログインする
  '''
  # vi編集時に描画がおかしくなるためプレフィックスは消す
  env.output_prefix = False
  sudo('/var/vcap/data/warden/depot/' + handle + '/bin/wsh --socket /var/vcap/data/warden/depot/' + handle + '/run/wshd.sock --user vcap /bin/bash')

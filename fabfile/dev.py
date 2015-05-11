#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, cd, task, env
from fabric.contrib import files
from fabric.decorators import parallel

import os

from .apt import install as apt_install, build_dep as apt_build_dep

@task
@parallel
def init():
  u'''
  fab -H <host> dev.init
  vcapユーザに便利ツール一式をインストールする
  '''
  # NOTE vagrantにmosh接続は表示がおかしくなる(udp関連かも)
  pkg = """
  vim
  build-essential
  git
  exuberant-ctags
  curl
  wget
  tmux
  zsh
  tree
  trash-cli
  silversearcher-ag
  mosh
  """
  apt_install(pkg)
  sudo('chsh -s /bin/zsh %s' % env.user)

  pt()
  jq()
  gosteno()
  dotfiles()
  ssh_setting()


def pt():
  if not files.exists('/usr/local/bin/pt'):
    with cd('/tmp'):
      if not files.exists('pt_linux_amd64.tar.gz'):
        run('wget https://github.com/monochromegane/the_platinum_searcher/releases/download/v1.7.6/pt_linux_amd64.tar.gz')

      run('tar zxvf pt_linux_amd64.tar.gz')
      sudo('cp pt_linux_amd64/pt /usr/local/bin')


def jq():
  if not files.exists('/usr/local/bin/jq'):
    with cd('/tmp'):
      if not files.exists('jq'):
        run('wget http://stedolan.github.io/jq/download/linux64/jq')

      run('chmod +x jq')
      sudo('cp jq /usr/local/bin')


def gosteno():
  if not files.exists('/usr/local/bin/gosteno-prettify'):
    with cd('/tmp'):
      if not files.exists('gosteno-prettify-bin.v151.zip'):
        run('wget https://github.com/nsnt/gosteno/releases/download/v158/gosteno-prettify-bin.v151.zip')

      run('unzip -o gosteno-prettify-bin.v151.zip')
      sudo('cp ./gosteno-prettify /usr/local/bin')


def dotfiles():
  if not files.exists('~/dotfiles'):
    run('git clone https://github.com/k-kurumi/dotfiles.git')

    with cd('dotfiles'):
      run('./replace.sh')

  if not files.exists('~/.vim'):
    # neobundle
    run('curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh')
    run('~/.vim/bundle/neobundle.vim/bin/neoinstall')


def ssh_setting():
  if os.path.exists(os.path.expanduser('~/.ssh/id_rsa.pub')):
    with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fp:
      run('''mkdir ~/.ssh''')
      run('''echo "%s" >> ~/.ssh/authorized_keys''' % fp.read())

  run('''echo 'export PATH=/var/vcap/bosh/bin:$PATH' >> ~/.shenv_local''')
  sudo('''echo 'vcap ALL=NOPASSWD: ALL' > /etc/sudoers.d/vcap''')


def vim_latest():
  pkg = '''
  python-dev
  ruby-dev
  luajit
  liblua5.2-dev
  '''
  apt_install(pkg)
  apt_build_dep('vim')

  if not files.exists('/usr/local/bin/vim'):
    with cd('/tmp'):
      if not files.exists('/tmp/vim'):
        run('git clone https://github.com/vim/vim.git')

      with cd('vim'):
        run('''./configure \
          --prefix=/usr/local \
          --with-features=huge \
          --enable-multibyte \
          --enable-pythoninterp=yes \
          --enable-rubyinterp=yes \
          --enable-luainterp=yes \
          --enable-cscope \
          --enable-gpm \
          --enable-cscope \
          --enable-fail-if-missing
          ''')
        run('make')
        sudo('make install')

  else:
    print 'already installed: /usr/local/bin/vim'

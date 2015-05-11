#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, cd, task
from fabric.contrib import files
from fabric.decorators import parallel


@task
@parallel
def forward(fluentd_recv_host):
  u'''
  fab -H <host> fluentd.forward:<fluentd_recv_host>
  ログ収集用のfluentdを設定する
  '''
  fluentd(fluentd_recv_host)
  rsyslog()


def fluentd(fluentd_recv_host):
  with cd('/tmp'):
    if not files.exists('td-agent_2.2.0-0_amd64.deb'):
      run('wget http://packages.treasuredata.com/2/ubuntu/trusty/pool/contrib/t/td-agent/td-agent_2.2.0-0_amd64.deb')

    sudo('dpkg -i td-agent_2.2.0-0_amd64.deb')
    sudo(""" cat << EOF > /etc/td-agent/td-agent.conf
<source>
  @type syslog
  @label @syslog
  # 指定しないとエラーが出る
  format /^(?<timestamp>[^ ]+) (?<host>[^ ]*) (?<ident>[a-zA-Z0-9_\/\.\-]*)(?:\[(?<pid>[0-9]+)\])?[^\:]*\: *(?<message>.*)$/
  tag cf
  port 51400
  bind 0.0.0.0
</source>


<label @syslog>
<match **>
  type copy

  <store>
  type forward

  # dockerホスト宛にするときはudpが通らないらしい
  heartbeat_type tcp
  heartbeat_interval 5s

  flush_interval 10s

  send_timeout 60s
  recover_wait 10s
  phi_threshold 16
  hard_timeout 60s

    <server>
      name collector
      # dockerはipが変わるから、ポートが固定できるホストに送るのがよい
      host %s
      port 24224
      weight 60
    </server>
  </store>

  <store>
  type stdout
  </store>
</match>
</label>
EOF
    """ % fluentd_recv_host)
  sudo('/etc/init.d/td-agent restart')


def rsyslog():
  u'''
  ローカルのfluentdへのvcapログ転送を設定する
  '''
  # TODO /etc/rsyslog.dに直接配置すればmetronの有無に左右されない(ジョブ名の判定が必要になる)

  # NOTE loggregatorにはmetronが無い
  if files.exists('/var/vcap/jobs/metron_agent/config/syslog_forwarder.conf'):
    if not files.contains('/var/vcap/jobs/metron_agent/config/syslog_forwarder.conf', ':programname, startswith, "vcap." @127.0.0.1:51400;CfLogTemplate'):
      # 行末にvcapを捨てる設定が入っているため、その上の行へ追記する
      sudo(""" sed -i.bak '$i:programname, startswith, "vcap." @127.0.0.1:51400;CfLogTemplate' '/var/vcap/jobs/metron_agent/config/syslog_forwarder.conf' """)

      # metron_agentの再起動で /etc/rsyslog.d/ も更新される
      sudo("/var/vcap/bosh/bin/monit restart metron_agent")

    else:
      print "already metron setting"

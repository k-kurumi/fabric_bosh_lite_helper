# fabric_bosh_lite_helper
bosh-lite環境の便利ツールです。


## Require
- fabric


## Install
fabricはpython3系では動作しません

```
$ pip install -r requirements.txt
```


## Example

```
## タスク一覧
$ fab -l
Available commands:

    dev.init
    tail.file     fab -H <host> tail.file:/var/log/syslog
    tail.job      fab -H <host> tail.job:warden
    warden.login  fab -H <host> warden.login:hdfjariej
    warden.pp     fab -H <host> warden.pp



## タスク詳細
$ fab -d warden.pp
Displaying detailed information for task 'warden.pp':

    fab -H <host> warden.pp
    アプリのハンドル一覧を表示する

    Arguments:


###


## warden(アプリ)の一覧
$ fab -H 10.244.0.26 warden.pp
[10.244.0.26] Executing task 'warden.pp'
[10.244.0.26] download: /home/tron/prog/fabric/bosh_lite_helper/10.244.0.26/instances.json <- /var/vcap/data/dea_next/db/instances.json
18klh91fs5v go1 00963a05-9666-4040-bda1-04c44553a520 RUNNING
18klh91fs62 dora1 ebb3d23f-3319-45cf-9d1e-cef76fa144f4 RUNNING
18klh91fs6j myapp1 92a135dc-6840-483b-9d26-9ecbba3dc246 RUNNING
18klh91fs6l go3 308a25fa-5e2c-4c27-9537-0defa9b112cc RUNNING



## wardenへログイン
$ fab -H 10.244.0.26 warden.login:18klh91fs6l
[10.244.0.26] Executing task 'warden.login'
[10.244.0.26] sudo: /var/vcap/data/warden/depot/18klh91fs6l/bin/wsh --socket /var/vcap/data/warden/depot/18klh91fs6l/run/wshd.sock --user vcap /bin/bash
sudo password:
vcap@18klh91fs6l:~$



###


## ログのtail パス指定
$ fab -H 10.244.0.26 tail.file:/var/vcap/sys/log/warden/warden.log
[10.244.0.26] Executing task 'tail.file'
[10.244.0.26] sudo: tail -F /var/vcap/sys/log/warden/warden.log
sudo password:
{"timestamp":1430470403.5325906,"message":"info (took 0.042425)","log_level":"debug","source":"Warden::Container::Linux","data":{"handle":"18klh91fs62","request":{"handle":"18klh91fs62"},"response":{"state":"active","events":[],"host_ip":
"10.254.1.205","container_ip":"10.254.1.206","container_path":"/var/vcap/data/warden/depot/18klh91fs62","memory_stat":"#<Warden::Protocol::InfoResponse::MemoryStat:0x00000001f5a8d8>","cpu_stat":"#<Warden::Protocol::InfoResponse::CpuStat:0
x00000001f5e3e8>","bandwidth_stat":"#<Warden::Protocol::InfoResponse::BandwidthStat:0x00000002674d58>","job_ids":[511]}},"thread_id":16541800,"fiber_id":16394000,"process_id":144,"file":"/var/vcap/data/packages/warden/882e41a9fef53fc4ee51
f0966f86fb9a0494c9e4.1-7eb03cfdc72636f8c9e2086972d57e631d77d7b5/warden/lib/warden/container/base.rb","lineno":300,"method":"dispatch"}



## ログのtail ジョブ指定
$ fab -H 10.244.0.26 tail.job:warden
```

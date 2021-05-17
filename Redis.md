# Redis

- [Redis](#redis)
  - [install redis by bash](#install-redis-by-bash)
  - [system configuration](#system-configuration)
  - [ulimit on linux](#ulimit-on-linux)
  - [redis.conf configuration](#redisconf-configuration)
  - [redis systemd service file](#redis-systemd-service-file)
  - [firewall](#firewall)
  - [start redis](#start-redis)
  - [benchmark](#benchmark)
  - [redis in docker](#redis-in-docker)
  - [redis in zabbix](#redis-in-zabbix)
  - [redis-cli](#redis-cli)

[Redis home](https://redis.io/)

## install redis by bash

```bash
wget http://download.redis.io/releases/redis-5.0.5.tar.gz

tar -xzvf redis-5.0.5.tar.gz

cd redis-5.0.5

make

make PREFIX=/usr/local/redis install

cp redis.conf /usr/local/redis/
```

## system configuration

```bash
#
# @see https://redis.io/topics/admin
#

vim /etc/sysctl.conf

# vm.overcommit_memory = 1
# net.core.somaxconn = 1024

echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

## ulimit on linux

```bash
ulimit -n
```

```bash
vim /etc/security/limits.conf

# * 代表用户名，* 表示所有用户
* soft nofile 1000000
* hard nofile 1000000
```

```bash
/etc/systemd/system.conf

DefaultLimitNOFILE=65535
DefaultLimitNPROC=65535
```

## redis.conf configuration

```bash
#
# @see https://redis.io/topics/config
#
vim /usr/local/redis/redis.conf

# 注释掉
#bind 127.0.0.1

# pasword
requirepass Abc@dfdfdfdf

# 对外端口
port 6380

# systemd
daemonize yes

# use systemd
supervised systemd
```

## redis systemd service file

```bash
vim /lib/systemd/system/redis.service
```

```systemd
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/redis/bin/redis-server /usr/local/redis/redis.conf
ExecStop=/usr/local/redis/bin/redis-cli shutdown
Restart=always

[Install]
WantedBy=multi-user.target
```

## firewall

```bash
# 开启端口(permanent永久)
firewall-cmd --zone=public --add-port=6380/tcp --permanent

# 重启firewall生效
firewall-cmd --reload
```

## start redis

```bash
# 开机启动
systemctl enable redis

# 启动
systemctl start redis

# 停止
systemctl stop redis
```

## benchmark

```bash

cd /usr/local/redis

./bin/redis-benchmark -h localhost -p 6380 -a Abc@dfdfdfdf  -c 100 -n 100000
```

## redis in docker

``` bash
docker run -d  -p 6380:6379 redis --requirepass '123456'
```

``` bash
docker exec -it [container_id] redis-cli -h [host] -p [port] -a [password]

# eg.
docker exec -it 05f92d468e05 redis-cli -a 123456
```

## redis in zabbix

[Zabbix 3.0 从入门到精通(zabbix使用详解)](https://www.cnblogs.com/clsn/p/7885990.html)

[使用Zabbix官方模板监控Redis运行状况](https://www.cnblogs.com/configure/p/6253590.html)

[zbx_redis_template](https://github.com/ringliwei/zbx_redis_template)

## redis-cli

[redis-cli, the Redis command line interface](https://redis.io/topics/rediscli)

```bash
# Usage
redis-cli [OPTIONS] [cmd [arg [arg ...]]]
```

```bash

  -h <hostname>      Server hostname (default: 127.0.0.1).
  -p <port>          Server port (default: 6379).
  -s <socket>        Server socket (overrides hostname and port).
  -a <password>      Password to use when connecting to the server.
                     You can also use the REDISCLI_AUTH environment
                     variable to pass this password more safely
                     (if both are used, this argument takes predecence).
  -u <uri>           Server URI.
  -r <repeat>        Execute specified command N times.
  -i <interval>      When -r is used, waits <interval> seconds per command.
                     It is possible to specify sub-second times like -i 0.1.
  -n <db>            Database number.
  -x                 Read last argument from STDIN.
  -d <delimiter>     Multi-bulk delimiter in for raw formatting (default: \n).
  -c                 Enable cluster mode (follow -ASK and -MOVED redirections).
  --raw              Use raw formatting for replies (default when STDOUT is
                     not a tty).
  --no-raw           Force formatted output even when STDOUT is not a tty.
  --csv              Output in CSV format.
  --stat             Print rolling stats about server: mem, clients, ...
  --latency          Enter a special mode continuously sampling latency.
                     If you use this mode in an interactive session it runs
                     forever displaying real-time stats. Otherwise if --raw or
                     --csv is specified, or if you redirect the output to a non
                     TTY, it samples the latency for 1 second (you can use
                     -i to change the interval), then produces a single output
                     and exits.
  --latency-history  Like --latency but tracking latency changes over time.
                     Default time interval is 15 sec. Change it using -i.
  --latency-dist     Shows latency as a spectrum, requires xterm 256 colors.
                     Default time interval is 1 sec. Change it using -i.
  --lru-test <keys>  Simulate a cache workload with an 80-20 distribution.
  --replica          Simulate a replica showing commands received from the master.
  --rdb <filename>   Transfer an RDB dump from remote server to local file.
  --pipe             Transfer raw Redis protocol from stdin to server.
  --pipe-timeout <n> In --pipe mode, abort with error if after sending all data.
                     no reply is received within <n> seconds.
                     Default timeout: 30. Use 0 to wait forever.
  --bigkeys          Sample Redis keys looking for keys with many elements (complexity).
  --memkeys          Sample Redis keys looking for keys consuming a lot of memory.
  --memkeys-samples <n> Sample Redis keys looking for keys consuming a lot of memory.
                     And define number of key elements to sample
  --hotkeys          Sample Redis keys looking for hot keys.
                     only works when maxmemory-policy is *lfu.
  --scan             List all keys using the SCAN command.
  --pattern <pat>    Useful with --scan to specify a SCAN pattern.
  --intrinsic-latency <sec> Run a test to measure intrinsic system latency.
                     The test will run for the specified amount of seconds.
  --eval <file>      Send an EVAL command using the Lua script at <file>.
  --ldb              Used with --eval enable the Redis Lua debugger.
  --ldb-sync-mode    Like --ldb but uses the synchronous Lua debugger, in
                     this mode the server is blocked and script changes are
                     not rolled back from the server memory.
  --cluster <command> [args...] [opts...]
                     Cluster Manager command and arguments (see below).
  --verbose          Verbose mode.
  --no-auth-warning  Dont show warning message when using password on command
                     line interface.
  --help             Output this help and exit.
  --version          Output version and exit.
```

Cluster Manager Commands:
  Use --cluster help to list all available cluster manager commands.

Examples:

```bash
cat /etc/passwd | redis-cli -x set mypasswd
redis-cli get mypasswd
redis-cli -r 100 lpush mylist x
redis-cli -r 100 -i 1 info | grep used_memory_human:
redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
redis-cli --scan --pattern '*:12345*'
#(Note: when using --eval the comma separates KEYS[] from ARGV[] items)

# 指定主机, 端口, 密码, 数据库
redis-cli -a <password> -h <host> -p [port] -n [db] cmd arg
```

When no command is given, `redis-cli starts in interactive mode`.
`Type "help"` in interactive mode for information on available commands
and settings.

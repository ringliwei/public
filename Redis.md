# Redis

- [Redis](#redis)
  - [install redis by bash](#install-redis-by-bash)
  - [system configuration](#system-configuration)
  - [redis.conf configuration](#redisconf-configuration)
  - [redis systemd service file](#redis-systemd-service-file)
  - [firewall](#firewall)
  - [start redis](#start-redis)
  - [redis in docker](#redis-in-docker)
  - [redis in zabbix](#redis-in-zabbix)

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

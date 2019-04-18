# ElasticSearch-7.0.0

## install script

```bash

# ElasticSearch最好不在在root用户下执行
groupadd es7
useradd -g es7 es7

# 切换到用户es7
su es7
cd ~
mkdir software
cd software
#
# @see https://www.elastic.co/cn/downloads/elasticsearch
#
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.0.0-linux-x86_64.tar.gz

tar -zxvf elasticsearch-7.0.0-linux-x86_64.tar.gz

# rename
mv elasticsearch-7.0.0-linux-x86_64 elasticsearch-7.0.0-linux-x86_64-node-1

cd elasticsearch-7.0.0-linux-x86_64-node-1

vim config/elasticsearch.yml
# cluster.name: log-center
# node.name: node-1
# network.host: 192.168.0.78
# http.port: 9200
# discovery.seed_hosts: ["192.168.0.78"]

./bin/elasticsearch
#  
# error:
# max file descriptors [4096] for elasticsearch process is too low, increase to at least
#

# 解决
su root
# 需要输入密码

# 添加配置
vim /etc/security/limits.conf
# es7 soft nofile 65536
# es7 hard nofile 65536
# es7 soft nproc 4096
# es7 hard nproc 4096

# 添加配置
vim /etc/sysctl.conf
# vm.max_map_count=655360

su es7

./bin/elasticsearch
```
# Elastic Stack

## 准备

```bash
# Elastic Stack运行Group及User
groupadd es7
useradd -g es7 es7
```

```bash
#  
# maybe error:
# max file descriptors [4096] for elasticsearch process is too low, increase to at least
# max number of threads [1024] for user [xxx] is too low, increase to at least [2048]
# max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
#

#
# 解决方案如下：
#
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
```

## ElasticSearch-7.0.0

```bash
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

# node-1, node-2, node-3
cp elasticsearch-7.0.0-linux-x86_64{,-node-1}
cp elasticsearch-7.0.0-linux-x86_64{,-node-2}
cp elasticsearch-7.0.0-linux-x86_64{,-node-3}

#
# node-1
#
vim config/elasticsearch.yml
# cluster.name: log-center
# node.name: node-1
# network.host: 192.168.0.78
# http.port: 9200
# transport.port: 9300
# discovery.seed_hosts: ["192.168.0.78:9300", "192.168.0.78:9301", "192.168.0.78:9302"]

#
# node-2
#
vim config/elasticsearch.yml
# cluster.name: log-center
# node.name: node-2
# network.host: 192.168.0.78
# http.port: 9201
# transport.port: 9301
# discovery.seed_hosts: ["192.168.0.78:9300", "192.168.0.78:9301", "192.168.0.78:9302"]

#
# node-3
#
vim config/elasticsearch.yml
# cluster.name: log-center
# node.name: node-3
# network.host: 192.168.0.78
# http.port: 9202
# transport.port: 9302
# discovery.seed_hosts: ["192.168.0.78:9300", "192.168.0.78:9301", "192.168.0.78:9302"]

su root

# 防火墙
firewall-cmd --zone=public --add-port=9200/tcp --permanent
firewall-cmd --zone=public --add-port=9201/tcp --permanent
firewall-cmd --zone=public --add-port=9202/tcp --permanent

firewall-cmd --reload

su es7

#
# start node-1, node-2 ,node-3
#
./bin/elasticsearch
```

## kibana-7.0.0

```bash
su es7
cd ~
# mkdir software
cd software

#
# @see https://www.elastic.co/cn/downloads/kibana
#
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.0.0-linux-x86_64.tar.gz
tar -zxvf kibana-7.0.0-linux-x86_64.tar.gz

cd kibana-7.0.0-linux-x86_64

vim config/kibana.yml
# server.host: "192.168.0.78"
# elasticsearch.hosts: ["http://192.168.0.78:9200"]

firewall-cmd --zone=public --add-port=5601/tcp --permanent
firewall-cmd --reload

#
# start kibana
#
./bin/kibana


#
# add kibana Sample data.
#
```

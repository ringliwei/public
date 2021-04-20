# Network

```bash
# 网卡目录
cd /etc/sysconfig/network-scripts/

# 网络管理器配置
vim /etc/NetworkManager/NetworkManager.conf
```

## 设置网卡DNS

```bash
# 显示当前网络连接
nmcli connection show
enp3s0f0  ae47418b-bfb6-485f-9c7c-d03cc345249f  ethernet  enp3s0f0 
enp3s0f1  a5ebf403-309c-4eba-87e7-ebf3c93ffc25  ethernet  --    

# 修改网络连接对应的DNS服务器
nmcli con mod enp3s0f0 ipv4.dns "114.114.114.114 8.8.8.8"

# 配置生效
nmcli con up eno1

# 查看配置
cd /etc/sysconfig/network-scripts/
cat ifcfg-enp3s0f0

# 验证
ping www.baidu.com
```

> cat ifcfg-enp3s0f0

```ini
HWADDR=24:1C:04:11:D0:DC
TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
NAME=enp3s0f0
UUID=ae47418b-bfb6-485f-9c7c-d03cc345249f
DEVICE=enp3s0f0
ONBOOT=yes

PROXY_METHOD=none
BROWSER_ONLY=no
IPADDR=192.168.1.18
PREFIX=24
GATEWAY=192.168.1.1
DNS1=114.114.114.114
DNS2=8.8.8.8
```

## 设置静态ip

```bash
# 网卡目录
cd /etc/sysconfig/network-scripts/

# 找到对应网卡
vim ifcfg-enp3s0f0

# add
IPADDR=192.168.1.18
PREFIX=24
GATEWAY=192.168.1.1
```

## 网络管理器

```bash
vim /etc/NetworkManager/NetworkManager.conf

[main]
plugins=ifcfg-rh
dns=none


# 重启
systemctl restart NetworkManager.service


# /etc/resolv.conf
vim /etc/resolv.conf

nameserver 114.114.114.114
nameserver 8.8.8.8
```

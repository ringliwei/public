# CentOS7

## firewall-cmd - firewalld command line client

[firewalld](https://firewalld.org/)

开启常见端口命令：

```bash
firewall-cmd --zone=public --add-port=80/tcp --permanent

firewall-cmd --zone=public --add-port=443/tcp --permanent

firewall-cmd --zone=public --add-port=22/tcp --permanent

firewall-cmd --zone=public --add-port=21/tcp --permanent
```

关闭常见端口命令：

```bash
firewall-cmd --zone=public --remove-port=80/tcp --permanent

firewall-cmd --zone=public --remove-port=443/tcp --permanent

firewall-cmd --zone=public --remove-port=22/tcp --permanent

firewall-cmd --zone=public --remove-port=21/tcp --permanent
```

批量添加端口：

```bash
firewall-cmd --zone=public--add-port=4400-4600/udp --permanent

firewall-cmd --zone=public--add-port=4400-4600/tcp --permanent
```

systemd：

```bash
systemctl restart firewalld.service
systemctl start firewalld.service
systemctl stop firewalld.service
# 开机启动
systemctl enable firewalld.service
# 禁止开机启动
systemctl disable firewalld.service
# 查看运行状态
systemctl status firewalld.service   # firewall-cmd --state
```

重启防火墙：

```bash
firewall-cmd --reload
# 或者
service firewalld restart
```

防火墙状态：

```bash
firewall-cmd --state
```

查看端口列表：

```bash
firewall-cmd --list-ports

# 只查看永久开启的端口
firewall-cmd --list-ports --permanent
```
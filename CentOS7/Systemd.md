# Systemd

- [Systemd](#systemd)
  - [Command](#command)
    - [systemctl](#systemctl)
    - [journalctl](#journalctl)
    - [loginctl](#loginctl)
    - [timedatectl](#timedatectl)
    - [localectl](#localectl)
    - [hostnamectl](#hostnamectl)
    - [systemd-analyze](#systemd-analyze)
  - [History](#history)
  - [Reference](#reference)

Systemd 是 Linux 系统工具，用来启动守护进程，已成为大多数发行版的标准配置。

[systemd @github](https://github.com/systemd/systemd)

[systemd @freedesktop](https://www.freedesktop.org/wiki/Software/systemd/)

## Command

### systemctl

```bash
# 立即启动一个服务
systemctl start nginx.service

# 立即停止一个服务
systemctl stop nginx.service

# 重启一个服务
systemctl restart nginx.service

# 杀死一个服务的所有子进程
systemctl kill nginx.service

# 重新加载一个服务的配置文件
systemctl reload nginx.service

# 重载所有修改过的配置文件
systemctl daemon-reload

# 显示某个 Unit 的所有底层参数
systemctl show httpd.service

# 显示某个 Unit 的指定属性的值
systemctl show -p CPUShares httpd.service

# 查看 Unit 文件
systemctl cat crond.service

# 设置某个 Unit 的指定属性
systemctl set-property httpd.service CPUShares=500
```

```bash
# 重启系统
systemctl reboot

# 关闭系统，切断电源
systemctl poweroff

# CPU停止工作
systemctl halt

# 暂停系统
systemctl suspend

# 让系统进入冬眠状态
systemctl hibernate

# 让系统进入交互式休眠状态
systemctl hybrid-sleep

# 启动进入救援状态（单用户状态）
systemctl rescue
```

```bash
# 列出正在运行的 Unit
systemctl list-units

# 列出所有Unit，包括没有找到配置文件的或者启动失败的
systemctl list-units --all

# 列出所有没有运行的 Unit
systemctl list-units --all --state=inactive

# 列出所有加载失败的 Unit
systemctl list-units --failed

# 列出所有正在运行的、类型为 service 的 Unit
systemctl list-units --type=service
```

### journalctl

```bash
# 查看所有日志（默认情况下 ，只保存本次启动的日志）
journalctl

# 查看内核日志（不显示应用日志）
journalctl -k

# 查看系统本次启动的日志
journalctl -b
journalctl -b -0

# 查看上一次启动的日志（需更改设置）
journalctl -b -1

# 查看指定时间的日志
journalctl --since="2012-10-30 18:17:16"
journalctl --since "20 min ago"
journalctl --since yesterday
journalctl --since "2015-01-10" --until "2015-01-11 03:00"
journalctl --since 09:00 --until "1 hour ago"

# 显示尾部的最新10行日志
journalctl -n

# 显示尾部指定行数的日志
journalctl -n 20

# 实时滚动显示最新日志
journalctl -f

# 查看指定服务的日志
journalctl /usr/lib/systemd/systemd

# 查看指定进程的日志
journalctl _PID=1

# 查看某个路径的脚本的日志
journalctl /usr/bin/bash

# 查看指定用户的日志
journalctl _UID=33 --since today

# 查看某个 Unit 的日志
journalctl -u nginx.service
journalctl -u nginx.service --since today

# 实时滚动显示某个 Unit 的最新日志
journalctl -u nginx.service -f

# 合并显示多个 Unit 的日志
journalctl -u nginx.service -u php-fpm.service --since today

# 查看指定优先级（及其以上级别）的日志，共有8级
# 0: emerg
# 1: alert
# 2: crit
# 3: err
# 4: warning
# 5: notice
# 6: info
# 7: debug
journalctl -p err -b

# 日志默认分页输出，--no-pager 改为正常的标准输出
journalctl --no-pager

# 以 JSON 格式（单行）输出
journalctl -b -u nginx.service -o json

# 以 JSON 格式（多行）输出，可读性更好
journalctl -b -u nginx.serviceqq
 -o json-pretty

# 显示日志占据的硬盘空间
journalctl --disk-usage

# 指定日志文件占据的最大空间
journalctl --vacuum-size=1G

# 指定日志文件保存多久
journalctl --vacuum-time=1years
```

### loginctl

```bash
# 列出当前session
loginctl list-sessions

# 列出当前登录用户
loginctl list-users

# 列出显示指定用户的信息
loginctl show-user root
```

### timedatectl

```bash
# 查看当前时区设置
timedatectl

# 显示所有可用的时区
timedatectl list-timezones

# 设置当前时区
timedatectl set-timezone Asia/Shanghai
timedatectl set-time YYYY-MM-DD
timedatectl set-time HH:MM:SS
```

### localectl

```bash
# 查看本地化设置
localectl

# 设置本地化参数。
localectl set-locale LANG=en_GB.utf8
localectl set-keymap en_GB
```

### hostnamectl

```bash
# 显示当前主机的信息
hostnamectl

# 设置主机名。
hostnamectl set-hostname rhel7
```

### systemd-analyze

```bash
# 查看启动耗时
systemd-analyze

# 查看每个服务的启动耗时
systemd-analyze blame

# 显示瀑布状的启动过程流
systemd-analyze critical-chain

# 显示指定服务的启动流
systemd-analyze critical-chain atd.service
```

## History

[浅析 Linux 初始化 init 系统，第 1 部分 sysvinit](https://www.ibm.com/developerworks/cn/linux/1407_liuming_init1/index.html)

[浅析 Linux 初始化 init 系统，第 2 部分 UpStart](https://www.ibm.com/developerworks/cn/linux/1407_liuming_init2/index.html)

[浅析 Linux 初始化 init 系统，第 3 部分 Systemd](https://www.ibm.com/developerworks/cn/linux/1407_liuming_init3/index.html)

[LINUX PID 1 和 SYSTEMD](https://coolshell.cn/articles/17998.html)

## Reference

[Systemd 入门教程：命令篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)

[Systemd 入门教程：实战篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)

[Node 应用的 Systemd 启动](http://www.ruanyifeng.com/blog/2016/03/node-systemd-tutorial.html)

[Systemd 定时器教程](http://www.ruanyifeng.com/blog/2018/03/systemd-timer.html)

[Systemd 中文手册(v235)](http://www.jinbuguo.com/systemd/systemd.index.html)
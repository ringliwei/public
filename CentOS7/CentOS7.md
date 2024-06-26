# CentOS7

- [CentOS7](#centos7)
  - [user and group](#user-and-group)
  - [system info](#system-info)
  - [user info](#user-info)
  - [proc info](#proc-info)
  - [ulimit](#ulimit)
  - [sysctl](#sysctl)

## user and group

```bash
groupadd mysql

# -r, --system: Create a system account.
useradd -r -g mysql mysql

# append user1 to mysql group
usermod -a -G mysql user1

chown -R root:root /usr/local/mysql
```

## system info

```bash
# 版本信息
cat /etc/os-release
cat /etc/redhat-release
cat /etc/fedora-release
cat /proc/version
uname -a
hostnamectl
lsb_release -a

# CPU
lscpu
cat /proc/cpuinfo

lsmod
```

## user info

```bash
# Show who is logged on and what they are doing.
w

# show who is logged on
who

# print the user names of users currently logged in to the current host
users

# print effective userid
whoami

# print real and effective user and group IDs
id root

# show a listing of last logged in users
last
```

## proc info

```bash
# get process id
ps aux | grep redis

# show proc info
ll /proc/{process}
```

| Item    | Desc                           |
| ------- | ------------------------------ |
| cwd     | 进程工作目录                   |
| exe     | 执行程序的绝对路径             |
| cmdline | 程序运行时输入的命令行命令     |
| environ | 进程运行时的环境变量           |
| fd      | 进程打开或使用的文件的符号连接 |

## ulimit

- /etc/security/limits.conf
- /etc/security/limits.d

```bash
ulimit -a
```

## sysctl

- /etc/sysctl.conf
- /etc/sysctl.d

```bash
# 系统内核最大进程数
sysctl kernel.pid_max
```

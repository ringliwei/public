# CentOS7

- [CentOS7](#centos7)
  - [system info](#system-info)
  - [program path](#program-path)

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

## program path

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

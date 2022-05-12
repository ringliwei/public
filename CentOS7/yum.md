# Yum

- [Yum](#yum)
  - [download rpm](#download-rpm)

## download rpm

- 方法一

```bash
vim /etc/yum.conf

# add key
keepcache=1
```

```bash
yum install telnet -y
```

```bash
# 去cache目录查找
cd /var/cache/yum/
```

- 方法二

```bash
yum install yum-utils -y

# download
yumdownloader --destdir=/root telnet
```

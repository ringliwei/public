# Yum

- [Yum](#yum)
  - [yum-utils](#yum-utils)
  - [download rpm](#download-rpm)
  - [add repo](#add-repo)

## yum-utils

[yum-utils](https://man7.org/linux/man-pages/man1/yum-utils.1.html) - tools for manipulating repositories and extended
package management

```bash
yum install yum-utils -y
```

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

## add repo

```bash
yum install yum-utils -y
yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repo
```

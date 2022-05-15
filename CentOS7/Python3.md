# Python3

- [Python3](#python3)
  - [install](#install)
    - [python3.7](#python37)
    - [python3.10](#python310)

## install

### python3.7

```bash
-- Development tools
yum -y group install "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel \
    sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum -y install libffi-devel


wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar -xvJf Python-3.7.0.tar.xz


mkdir /usr/local/python3


./configure --prefix=/usr/local/python3/
make && make install

-- ln
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

### python3.10

```bash
-- Development tools
yum -y group install "Development tools"

yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel \
    sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

yum -y install libffi-devel

yum install -y openssl-devel openssl11 openssl11-devel


wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
tar -xvJf Python-3.10.4.tgz


mkdir /usr/local/python3


export CFLAGS=$(pkg-config --cflags openssl11)
export LDFLAGS=$(pkg-config --libs openssl11)

./configure --prefix=/usr/local/python3/ --enable-optimizations
make && make install

-- ln
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

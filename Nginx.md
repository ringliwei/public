# Nginx

[@CentOS7](https://www.centos.org/)

[nginx docs](http://nginx.org/en/docs/)

[nginx configure](http://nginx.org/en/docs/configure.html)

## install nginx by bash

```bash

cd /usr/local/src

#
# @see http://nginx.org/en/download.html
#
wget http://nginx.org/download/nginx-1.15.11.tar.gz

tar -xzvf nginx-1.15.11.tar.gz

#
# @see http://www.pcre.org/
#
wget https://ftp.pcre.org/pub/pcre/pcre-8.43.tar.gz

tar -xzvf pcre-8.43.tar.gz

#
# @see https://www.openssl.org/source/
#
wget https://www.openssl.org/source/openssl-1.0.2r.tar.gz

tar -xzvf openssl-1.0.2r.tar.gz

#
# @see http://www.zlib.net/
#
wget http://www.zlib.net/zlib-1.2.11.tar.gz

tar -xzvf zlib-1.2.11.tar.gz


# 重点来了！！！
cd nginx-1.15.11

./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-pcre=../pcre-8.43 \
--with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.0.2r

make && make install

test -e /usr/bin/nginx || ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx
```

## install nginx by bash and versioning

```bash

cd /usr/local/src

nginx_version=1.15.11
pcre_version=8.43
openssl_version=1.0.2r
zlib_version=1.2.11

#
# @see http://nginx.org/en/download.html
#
wget http://nginx.org/download/nginx-${nginx_version}.tar.gz

tar -xzvf nginx-${nginx_version}.tar.gz

#
# @see http://www.pcre.org/
#
wget https://ftp.pcre.org/pub/pcre/pcre-${pcre_version}.tar.gz

tar -xzvf pcre-${pcre_version}.tar.gz

#
# @see https://www.openssl.org/source/
#
wget https://www.openssl.org/source/openssl-${openssl_version}.tar.gz

tar -xzvf openssl-${openssl_version}.tar.gz

#
# @see http://www.zlib.net/
#
wget http://www.zlib.net/zlib-${zlib_version}.tar.gz

tar -xzvf zlib-${zlib_version}.tar.gz


# 重点来了！！！
cd nginx-${nginx_version}

./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-pcre=../pcre-${pcre_version} \
--with-zlib=../zlib-${zlib_version} --with-openssl=../openssl-${openssl_version}

make && make install

test -e /usr/bin/nginx || ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx
```

## start nginx

```bash
# 开启端口(permanent永久)
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=443/tcp --permanent

# 重启firewall生效
firewall-cmd --reload
# 查看开启的端口
firewall-cmd --list-ports

# 符号链接
test -e /usr/bin/nginx || ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx

# start
nginx
```
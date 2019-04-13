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

## install nginx dynamic module

以`--with-stream=dynamic`为例，`--add-module`类似

```bash
#
# 查看nginx详细安装信息
#
nginx -V
# nginx version: nginx/1.15.11
# built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
# built with OpenSSL 1.0.2r  26 Feb 2019
# TLS SNI support enabled
# configure arguments: --prefix=/usr/local/nginx --with-http_ssl_module --with-http_sub_module \
# --with-http_gzip_static_module --with-http_stub_status_module \
# --with-pcre=../pcre-8.43 --with-zlib=../zlib-1.2.11/ --with-openssl=../openssl-1.0.2r

#
# whereis nginx 查看本机是否存在nginx源码目录
# 若没有，下载对应版本的源，如nginx
# cd /usr/local/src
# nginx_version=1.15.11
# wget http://nginx.org/download/nginx-${nginx_version}.tar.gz
#

cd /usr/local/src/nginx-1.15.11
# 将配置输出到ngx_config.sh
nginx -V 2>&1 | awk '{print $0}' > ngx_config.sh

# --with-stream=dynamic
vim ngx_config.sh
#./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-http_sub_module \
# --with-http_gzip_static_module --with-http_stub_status_module \
# --with-pcre=../pcre-8.43 --with-zlib=../zlib-1.2.11/ --with-openssl=../openssl-1.0.2r --with-stream=dynamic

chmod 755 ngx_config.sh

bash ngx_config.sh

# 只执行make
make

# copy
cp /usr/local/nginx/sbin/nginx{,.bak}
cp ./objs/nginx /usr/local/nginx/sbin/
cp ./objs/ngx_stream_module.so /usr/local/nginx/modules/

# 编辑nginx.conf
vim /usr/local/nginx/conf/nginx.conf
# 顶层添加如下指令
# load_module modules/ngx_stream_module.so;

# 重新加载配置
nginx -s reload
```
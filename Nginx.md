# Nginx

[nginx docs](http://nginx.org/en/docs/)

[nginx configure](http://nginx.org/en/docs/configure.html)

## nginx install bash

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

ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx

```
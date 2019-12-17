# Node.js

[Home](https://nodejs.org/en/)

- [Node.js](#nodejs)
  - [install](#install)
  - [npm](#npm)
  - [pm2](#pm2)
    - [cheatsheet](#cheatsheet)
    - [Nginx as a HTTP proxy](#nginx-as-a-http-proxy)

## install

```bash
# 直接下载二进制文件
wget https://nodejs.org/dist/v12.13.1/node-v12.13.1-linux-x64.tar.xz

# 解压第一步
xz -d node-v12.13.1-linux-x64.tar.xz

# 解压第二步
tar -xvf node-v12.13.1-linux-x64.tar

# mv
mv node-v12.13.1-linux-x64 /usr/local/node

# ----------- export path 则不需要ln start
# node
ln -s /usr/local/node/bin/node /usr/bin/node

# npm
ln -s /usr/local/node/bin/npm /usr/bin/npm

# npx
ln -s /usr/local/node/bin/npx /usr/bin/npx

# ----------- export path 则不需要ln end
```

```bash

# vim /etc/profile
export PATH="$PATH:/usr/local/node/bin/"

# 立即生效
source /etc/profile
```

## npm

[cli-documentation](https://docs.npmjs.com/cli-documentation/cli)

[npmrc](https://docs.npmjs.com/files/npmrc)

```bash
vim ~/.npmrc

# add
registry = "https://registry.npm.taobao.org/"
```

```bash
npm config ls -l

npm config set prefix "E:\Repos\npm"

npm config set cache "E:\Repos\npm\cache"

npm config set registry https://registry.npm.taobao.org

npm config get registry
```

```bash
# create a package.json file
npm init

# Generate a plain old package.json
mkdir my-npm-pkg && cd my-npm-pkg
git init
npm init -y
```

## pm2

PM2 is daemon process manager that will help you manage and keep your application online.

[github](https://github.com/Unitech/pm2)

[home](https://pm2.keymetrics.io)

[doc](https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/)

```bash
# 安装
npm install pm2@latest -g

# @see https://pm2.keymetrics.io/docs/usage/startup/
# Detect available init system, generate configuration and enable startup system
pm2 startup

# Once you started all the applications you want to manage, you have to save the list you wanna respawn at machine reboot with:
pm2 save
```

### cheatsheet

```bash
# Fork mode
pm2 start app.js --name my-api # Name process

# Cluster mode
pm2 start app.js -i 0        # Will start maximum processes with LB depending on available CPUs
pm2 start app.js -i max      # Same as above, but deprecated.
pm2 scale app +3             # Scales `app` up by 3 workers
pm2 scale app 2              # Scales `app` up or down to 2 workers total

# Listing

pm2 list               # Display all processes status
pm2 jlist              # Print process list in raw JSON
pm2 prettylist         # Print process list in beautified JSON

pm2 describe 0         # Display all informations about a specific process
pm2 info 0             # Display all informations about a specific process

pm2 monit              # Monitor all processes

# Logs

pm2 logs [--raw]       # Display all processes logs in streaming
pm2 flush              # Empty all log files
pm2 reloadLogs         # Reload all logs

# Actions

pm2 stop all           # Stop all processes
pm2 restart all        # Restart all processes

pm2 reload all         # Will 0s downtime reload (for NETWORKED apps)

pm2 stop 0             # Stop specific process id
pm2 restart 0          # Restart specific process id

pm2 delete 0           # Will remove process from pm2 list
pm2 delete all         # Will remove all processes from pm2 list

# Misc

pm2 reset <process>    # Reset meta data (restarted time...)
pm2 updatePM2          # Update in memory pm2
pm2 ping               # Ensure pm2 daemon has been launched
pm2 sendSignal SIGUSR2 my-app # Send system signal to script
pm2 start app.js --no-daemon
pm2 start app.js --no-vizion
pm2 start app.js --no-autorestart
```

### Nginx as a HTTP proxy

[Nginx as a HTTP proxy](https://pm2.keymetrics.io/docs/tutorials/pm2-nginx-production-setup)

```nginx
upstream my_nodejs_upstream {
    server 127.0.0.1:3000;
    keepalive 64;
}

server {
    listen 443 ssl;

    server_name www.my-website.com;
    ssl_certificate_key /etc/ssl/main.key;
    ssl_certificate     /etc/ssl/main.crt;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass http://my_nodejs_upstream/;
        proxy_redirect off;
        proxy_read_timeout 240s;
    }
}
```

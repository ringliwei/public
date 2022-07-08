# Node.js

- [Home](https://nodejs.org/en/)

- [Node.js](#nodejs)
  - [install](#install)
    - [How to install Node.js via binary archive on Linux](#how-to-install-nodejs-via-binary-archive-on-linux)
  - [npm](#npm)
  - [pm2](#pm2)
    - [cheatsheet](#cheatsheet)
    - [Nginx as a HTTP proxy](#nginx-as-a-http-proxy)
  - [library](#library)
    - [async](#async)
    - [bluebird](#bluebird)
    - [cli-table](#cli-table)
    - [colors](#colors)
    - [commander](#commander)
    - [consola](#consola)
    - [Chalk](#chalk)
    - [ky](#ky)
    - [got](#got)
    - [axios](#axios)
    - [request](#request)
    - [request-promise](#request-promise)
    - [pm2 process manager](#pm2-process-manager)
    - [jake](#jake)
    - [puppeteer](#puppeteer)
    - [playwright](#playwright)
    - [generic-pool](#generic-pool)
    - [yo](#yo)
    - [rxjs](#rxjs)
    - [lodash](#lodash)
    - [ramda](#ramda)
    - [immer](#immer)
    - [date-fns](#date-fns)
    - [moment](#moment)
    - [mathjs](#mathjs)
    - [prettier](#prettier)
    - [koa-generator](#koa-generator)
    - [art-template](#art-template)
    - [nanoid](#nanoid)
    - [node-fetch](#node-fetch)
    - [zx](#zx)
    - [blessed](#blessed)
    - [blessed-contrib](#blessed-contrib)
  - [Framework](#framework)
  - [Package Tool](#package-tool)
  - [Presets](#presets)
  - [Node.js On Windows XP](#nodejs-on-windows-xp)

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

### How to install Node.js via binary archive on Linux

[How to install Node.js via binary archive on Linux](https://github.com/nodejs/help/wiki/Installation#how-to-install-nodejs-via-binary-archive-on-linux)

step 1. Unzip the binary archive to any directory you wanna install Node, I use `/usr/local/node`

```bash
PROD_NODE_VERSION=v10.15.0
PROD_NODE_DISTRO=linux-x64
sudo mkdir -p /usr/local/node
sudo tar -xJvf node-$PROD_NODE_VERSION-$PROD_NODE_DISTRO.tar.xz -C /usr/local/node
```

step 2. Set the environment variable `/etc/profile` or `~/.profile`, add below to the end

```bash
# Nodejs
PROD_NODE_VERSION=v10.15.0
PROD_NODE_DISTRO=linux-x64
export PATH=/usr/local/node/node-$PROD_NODE_VERSION-$PROD_NODE_DISTRO/bin:$PATH
```

step 3. Refresh profile

```bash
source ~/.profile
# or
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

## Target path
## /etc/systemd/system/pm2-root.service

# 开机启动
systemctl enable pm2-root

# Once you started all the applications you want to manage, you have to save the list you wanna respawn at machine reboot with:
pm2 save
```

> cat /etc/systemd/system/pm2-root.service

```systemd
[Unit]
Description=PM2 process manager
Documentation=https://pm2.keymetrics.io/
After=network.target

[Service]
Type=forking
User=root
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
Environment=PATH=/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/usr/local/node/bin/:/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
Environment=PM2_HOME=/root/.pm2
PIDFile=/root/.pm2/pm2.pid
Restart=on-failure

ExecStart=/usr/local/node/lib/node_modules/pm2/bin/pm2 resurrect
ExecReload=/usr/local/node/lib/node_modules/pm2/bin/pm2 reload all
ExecStop=/usr/local/node/lib/node_modules/pm2/bin/pm2 kill

[Install]
WantedBy=multi-user.target
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

## library

### async

[Async](https://www.npmjs.com/package/async) is a utility module which provides straight-forward, powerful functions for working with asynchronous JavaScript. Although originally designed for use with Node.js and installable via npm install async, it can also be used directly in the browser. A ESM version is included in the main async package that should automatically be used with compatible bundlers such as Webpack and Rollup.

### bluebird

[Bluebird](https://www.npmjs.com/package/bluebird) is a fully featured promise library with focus on innovative features and performance

---

### cli-table

[cli-table](https://www.npmjs.com/package/cli-table)
This utility allows you to render unicode-aided tables on the command line from your node.js scripts.

### colors

[colors](https://www.npmjs.com/package/colors)
get color and style in your node.js console

### commander

[commander](https://www.npmjs.com/package/commander)
The complete solution for node.js command-line interfaces, inspired by Ruby's commander

### consola

[consola](https://www.npmjs.com/package/consola)
Elegant Console Logger for Node.js and Browser

### Chalk

[Chalk](https://www.npmjs.com/package/chalk)
Terminal string styling done right

---

### ky

[Ky](https://www.npmjs.com/package/ky) is a tiny and elegant HTTP client based on the browser Fetch API

### got

[got](https://www.npmjs.com/package/got)
Human-friendly and powerful HTTP request library for Node.js

### axios

[axios](https://www.npmjs.com/package/axios)
Promise based HTTP client for the browser and node.js

### request

[Request](https://www.npmjs.com/package/request) is designed to be the simplest way possible to make http calls. It supports HTTPS and follows redirects by default.

### request-promise

The simplified HTTP request client 'request' with Promise support. Powered by Bluebird.

---

### pm2 process manager

[PM2](https://www.npmjs.com/package/pm2) is a production process manager for Node.js applications with a built-in load balancer. It allows you to keep applications alive forever, to reload them without downtime and to facilitate common system admin tasks.

### jake

[jake](https://www.npmjs.com/package/jake)
the JavaScript build tool for Node.js

### puppeteer

[Puppeteer](https://www.npmjs.com/package/puppeteer) is a Node library which provides a high-level API to control Chrome or Chromium over the DevTools Protocol. Puppeteer runs headless by default, but can be configured to run full (non-headless) Chrome or Chromium.

### playwright

[playwright](https://www.npmjs.com/package/playwright) is a Node.js library to automate Chromium, Firefox and WebKit with a single API.

### generic-pool

[generic-pool](https://www.npmjs.com/package/generic-pool)
Generic resource pool with Promise based API. Can be used to reuse or throttle usage of expensive resources such as database connections.

### yo

[Yeoman](https://www.npmjs.com/package/yo) helps you to kickstart new projects, prescribing best practices and tools to help you stay productive.

### rxjs

[RxJS](https://www.npmjs.com/package/rxjs): Reactive Extensions For JavaScript

### lodash

[lodash](https://www.npmjs.com/package/lodash)
A modern JavaScript utility library delivering modularity, performance, & extras.

### ramda

[ramda](https://www.npmjs.com/package/ramda)
A practical functional library for JavaScript programmers.

### immer

[immer](https://www.npmjs.com/package/immer)
Create the next immutable state tree by simply modifying the current tree

### date-fns

[date-fns](https://www.npmjs.com/package/date-fns)
provides the most comprehensive, yet simple and consistent toolset for manipulating JavaScript dates in a browser & Node.js.

### moment

[moment](https://www.npmjs.com/package/moment)
A lightweight JavaScript date library for parsing, validating, manipulating, and formatting dates.

### mathjs

[Math.js](https://www.npmjs.com/package/mathjs) is an extensive math library for JavaScript and Node.js

### prettier

[Prettier](https://www.npmjs.com/package/prettier) is an opinionated code formatter. It enforces a consistent style by parsing your code and re-printing it with its own rules that take the maximum line length into account, wrapping code when necessary.

### koa-generator

[koa-generator](https://www.npmjs.com/package/koa-generator)
Koa application generator.

### art-template

[art-template](https://www.npmjs.com/package/art-template) is a simple and superfast templating engine that optimizes template rendering speed by scope pre-declared technique, hence achieving runtime performance which is close to the limits of JavaScript. At the same time, it supports both NodeJS and browser.

### nanoid

[nanoid](https://github.com/ai/nanoid/) A tiny (108 bytes), secure, URL-friendly, unique string ID generator for JavaScript

### node-fetch

[node-fetch](https://www.npmjs.com/package/node-fetch) A light-weight module that brings window.fetch to Node.js

### zx

[zx](https://github.com/google/zx) A tool for writing better scripts

### blessed

[blessed](https://github.com/chjj/blessed) A high-level terminal interface library for node.js.

### blessed-contrib

[blessed-contrib](https://github.com/yaronn/blessed-contrib) Build terminal dashboards using ascii/ansi art and javascript

## Framework

[express](https://github.com/expressjs/express)

[meteor](https://github.com/meteor/meteor)

[nest](https://github.com/nestjs/nest)

[koa](https://github.com/koajs/koa)

[sails](https://github.com/balderdashy/sails)

[fastify](https://github.com/fastify/fastify)

[egg](https://github.com/eggjs/egg)

[loopback](https://github.com/strongloop/loopback)

[hapi](https://github.com/hapijs/hapi)

[pomelo](https://github.com/NetEase/pomelo)

[node-restify](https://github.com/restify/node-restify)

[egg](https://github.com/eggjs/egg)

[thinkjs](https://github.com/thinkjs/thinkjs)

## Package Tool

- [pkg](https://github.com/vercel/pkg) Package your Node.js project into an executable

## Presets

- [neutrino](https://github.com/neutrinojs/neutrino/) Create and build modern JavaScript projects with zero initial configuration.
  - Neutrino combines the power of webpack with the simplicity of presets.

## Node.js On Windows XP

- [which-nodejs-version-should-i-set-up-on-an-old-windows-xp-machine](https://stackoverflow.com/questions/37744391/which-nodejs-version-should-i-set-up-on-an-old-windows-xp-machine)
- [v5.12.0](https://nodejs.org/dist/v5.12.0/)

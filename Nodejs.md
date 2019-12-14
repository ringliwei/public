# Node.js

[Home](https://nodejs.org/en/)

- [Node.js](#nodejs)
  - [install](#install)
  - [npm](#npm)

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

# node
ln -s /usr/local/node/bin/node /usr/bin/node

# npm
ln -s /usr/local/node/bin/npm /usr/bin/npm

# npx
ln -s /usr/local/node/bin/npx /usr/bin/npx
```

## npm

[cli-documentation](https://docs.npmjs.com/cli-documentation/cli)

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
```

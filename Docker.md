# Docker

- [Docker](#docker)
  - [Install](#install)
    - [Docker Engine](#docker-engine)
    - [Docker Mirror](#docker-mirror)
    - [Docker Compose](#docker-compose)
  - [Docker Command](#docker-command)
    - [Management Commands](#management-commands)
    - [Commands](#commands)
    - [Image](#image)
    - [Container](#container)
    - [Samples](#samples)
      - [Batch](#batch)
      - [docker system](#docker-system)
  - [Dockerfile](#dockerfile)
    - [CMD & ENTRYPOINT](#cmd--entrypoint)
    - [VOLUME](#volume)
    - [SHELL](#shell)
  - [DevOps](#devops)
    - [UI](#ui)
  - [Docker Tutorial](#docker-tutorial)
  - [Docker Tutorial2](#docker-tutorial2)
  - [Docker Foundation](#docker-foundation)

## Install

### Docker Engine

[Install Docker Engine on CentOS](https://docs.docker.com/engine/install/centos/)

[Aliyun CentOS 7](https://developer.aliyun.com/mirror/docker-ce)

```bash
# step 1: 安装必要的一些系统工具
yum install -y yum-utils

# Step 2: 添加软件源信息
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# Step 3: 更新并安装Docker-CE
yum makecache fast
yum -y install docker-ce docker-ce-cli containerd.io


# Step 4: 配置
mkdir /etc/docker
cat <<EOF | tee /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://registry.cn-hangzhou.aliyuncs.com",
    "https://docker.mirrors.ustc.edu.cn"
  ],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

# Step 5: 开机启动
systemctl daemon-reload
systemctl restart docker
systemctl enable docker
```

```bash
docker version
```

### Docker Mirror

[mirror](https://docs.docker.com/registry/recipes/mirror/)

```bash
# vim /etc/docker/daemon.json

{
    "registry-mirrors": [
       "https://mirror.ccs.tencentyun.com"
    ]
}

```

```bash
docker info
```

### Docker Compose

[Docker Compose](https://docs.docker.com/compose/install/)

```bash
curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Docker Command

```bash
# 查看docker版本信息
docker info
docker version

Client: Docker Engine - Community
 Version:           19.03.13
 API version:       1.40
 Go version:        go1.13.15
 Git commit:        4484c46d9d
 Built:             Wed Sep 16 17:02:36 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.13
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.13.15
  Git commit:       4484c46d9d
  Built:            Wed Sep 16 17:01:11 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.3.7
  GitCommit:        8fba4e9a7d01810a393d5d25a3621dc101981175
 runc:
  Version:          1.0.0-rc10
  GitCommit:        dc9208a3303feef5b3839f4323d9beb36df0a9dd
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

### Management Commands

```bash
Management Commands:
  builder     Manage builds
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  engine      Manage the docker engine
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes
```

### Commands

```bash
cat <<EOF
Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes
EOF
```

### Image

```bash
docker image --help

Usage: docker image COMMAND

Manage images

Commands:
  build       Build an image from a Dockerfile
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Display detailed information on one or more images
  load        Load an image from a tar archive or STDIN
  ls          List images
  prune       Remove unused images
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rm          Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
```

### Container

```bash
docker container --help

Usage: docker container COMMAND

Manage containers

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  inspect     Display detailed information on one or more containers
  kill        Kill one or more running containers
  logs        Fetch the logs of a container
  ls          List containers
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  prune       Remove all stopped containers
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  run         Run a command in a new container
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes
```

### Samples

#### Batch

```bash
# 删除所有容器
docker rm -f `docker ps -a -q`

# 删除所有的镜像
docker rmi -f `docker images -q`
```

#### docker system

[清理 Docker 占用的磁盘空间](https://www.cnblogs.com/wuxingwang/p/12170071.html)

```bash
# docker 使用空间
docker system df
```

## Dockerfile

### CMD & ENTRYPOINT

[CMD ENTRYPOINT 区别](https://blog.csdn.net/u010900754/article/details/78526443)

### VOLUME

[Dockerfile 指令 VOLUME 介绍](https://www.cnblogs.com/51kata/p/5266626.html)

### SHELL

The SHELL instruction allows the default shell used for the shell form of commands to be overridden. The default shell on Linux is `["/bin/sh", "-c"]`, and on Windows is `["cmd", "/S", "/C"]`. The SHELL instruction must be written in JSON form in a Dockerfile.

The following instructions can be affected by the SHELL instruction when the shell form of them is used in a Dockerfile: `RUN`, `CMD` and `ENTRYPOINT`.

## DevOps

### UI

[portainer](https://github.com/portainer/portainer)

## Docker Tutorial

[docker-tutorial](http://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html)

[docker-wordpress-tutorial](http://www.ruanyifeng.com/blog/2018/02/docker-wordpress-tutorial.html)

## Docker Tutorial2

[这可能是最为详细的 Docker 入门吐血总结](https://www.cnblogs.com/ECJTUACM-873284962/p/9789130.html)

[Docker 最初的 2 小时](https://blog.csdn.net/21cnbao/article/details/56275456)

[什么是 Docker](https://cloud.tencent.com/developer/article/1005172)

---

[Docker 组件如何协作？- 每天 5 分钟玩转容器技术（8）](https://www.cnblogs.com/CloudMan6/p/6774519.html)

[最小的镜像 - 每天 5 分钟玩转容器技术（9）](https://www.cnblogs.com/CloudMan6/p/6788841.html)

[base 镜像 - 每天 5 分钟玩转容器技术（10）](https://www.cnblogs.com/CloudMan6/p/6799197.html)

[镜像的分层结构 - 每天 5 分钟玩转容器技术（11）](https://www.cnblogs.com/CloudMan6/p/6806193.html)

---

[深入浅出 Docker（一）：Docker 核心技术预览](https://www.infoq.cn/article/docker-core-technology-preview)

[深入浅出 Docker（二）：Docker 命令行探秘](https://www.infoq.cn/article/docker-command-line-quest)

[深入浅出 Docker（三）：Docker 开源之路](https://www.infoq.cn/article/docker-open-source-road)

[深入浅出 Docker（四）：Docker 的集成测试部署之道](https://www.infoq.cn/article/docker-integrated-test-and-deployment)

[深入浅出 Docker（五）：基于 Fig 搭建开发环境](https://www.infoq.cn/article/docker-build-development-environment-based-on-fig)

[深入浅出 Docker（六）：像谷歌一样部署你的应用](https://www.infoq.cn/article/deploy-your-application-like-google)

## Docker Foundation

[DOCKER 基础技术：LINUX NAMESPACE（上）](https://coolshell.cn/articles/17010.html)

[DOCKER 基础技术：LINUX NAMESPACE（下）](https://coolshell.cn/articles/17029.html)

[DOCKER 基础技术：LINUX CGROUP](https://coolshell.cn/articles/17049.html)

[DOCKER 基础技术：AUFS](https://coolshell.cn/articles/17061.html)

- [Overlay_filesystem](https://wiki.archlinux.org/title/Overlay_filesystem)
- [how-containers-work--overlayfs](https://jvns.ca/blog/2019/11/18/how-containers-work--overlayfs/)
- [overlayfs](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html)

[DOCKER 基础技术：DEVICEMAPPER](https://coolshell.cn/articles/17200.html)

[How to implement container in golang?](https://mp.weixin.qq.com/s/wTby-KcsQdss7Sg20ay6vw)

[Python3 cgroupspy](https://www.cnblogs.com/lsdb/p/13140210.html)

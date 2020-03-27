# Docker

- [Docker](#docker)
  - [Install](#install)
  - [入门必看](#%e5%85%a5%e9%97%a8%e5%bf%85%e7%9c%8b)
  - [DOCKER基础技术](#docker%e5%9f%ba%e7%a1%80%e6%8a%80%e6%9c%af)

## Install

[Get Docker Engine - Community for CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)

[Aliyun CentOS 7](https://developer.aliyun.com/mirror/docker-ce)

```bash
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/
docker-ce/linux/centos/docker-ce.repo

# Step 3: 更新并安装Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce

# Step 4: 开启Docker服务
sudo service docker start

# Step 5: 开机启动
systemctl enable docker
```

## 入门必看

[这可能是最为详细的Docker入门吐血总结](https://www.cnblogs.com/ECJTUACM-873284962/p/9789130.html)

[Docker 最初的2小时](https://blog.csdn.net/21cnbao/article/details/56275456)

[什么是 Docker](https://cloud.tencent.com/developer/article/1005172)

-------------------------

[Docker 组件如何协作？- 每天5分钟玩转容器技术（8）](https://www.cnblogs.com/CloudMan6/p/6774519.html)

[最小的镜像 - 每天5分钟玩转容器技术（9）](https://www.cnblogs.com/CloudMan6/p/6788841.html)

[base 镜像 - 每天5分钟玩转容器技术（10）](https://www.cnblogs.com/CloudMan6/p/6799197.html)

[镜像的分层结构 - 每天5分钟玩转容器技术（11）](https://www.cnblogs.com/CloudMan6/p/6806193.html)

-------------------------

[深入浅出 Docker（一）：Docker 核心技术预览](https://www.infoq.cn/article/docker-core-technology-preview)

[深入浅出 Docker（二）：Docker 命令行探秘](https://www.infoq.cn/article/docker-command-line-quest)

[深入浅出 Docker（三）：Docker 开源之路](https://www.infoq.cn/article/docker-open-source-road)

[深入浅出 Docker（四）：Docker 的集成测试部署之道](https://www.infoq.cn/article/docker-integrated-test-and-deployment)

[深入浅出 Docker（五）：基于 Fig 搭建开发环境](https://www.infoq.cn/article/docker-build-development-environment-based-on-fig)

[深入浅出 Docker（六）：像谷歌一样部署你的应用](https://www.infoq.cn/article/deploy-your-application-like-google)

## DOCKER基础技术

[DOCKER基础技术：LINUX NAMESPACE（上）](https://coolshell.cn/articles/17010.html)

[DOCKER基础技术：LINUX NAMESPACE（下）](https://coolshell.cn/articles/17029.html)

[DOCKER基础技术：LINUX CGROUP](https://coolshell.cn/articles/17049.html)

[DOCKER基础技术：AUFS](https://coolshell.cn/articles/17061.html)

[DOCKER基础技术：DEVICEMAPPER](https://coolshell.cn/articles/17200.html)

[yum-utils](<(https://man7.org/linux/man-pages/man1/yum-utils.1.html)>) 是一个工具集，包含用于管理 yum 软件包仓库、安装调试包和源代码包、从仓库获取扩展信息以及进行系统管理的各类工具和程序。

`主要功能包括：`

1. 仓库管理工具

   - `repoquery`：查询仓库中的软件包信息
   - `yum-config-manager`：管理仓库配置
   - `yum-repo-manager`：仓库配置文件管理

2. 软件包管理工具

   - `debuginfo-install`：安装调试信息包
   - `yum-builddep`：安装软件包的构建依赖
   - `repo-graph`：生成仓库依赖关系图
   - `package-cleanup`：清理旧版本软件包

3. 仓库镜像与同步

   - `reposync`：同步远程仓库到本地
   - `repotrack`：跟踪并下载软件包及其依赖

4. 管理工具
   - `yum-complete-transaction`：完成未完成的事务
   - `needs-restarting`：检查需要重启的服务

`安装方法：`

```bash
# CentOS/RHEL
sudo yum install yum-utils

# Fedora
sudo dnf install yum-utils
```

`常用示例：`

```bash
# 列出已启用的仓库
yum repolist enabled

# 下载软件包但不安装
yumdownloader package-name

# 查找哪个仓库提供特定文件
repoquery --whatprovides /path/to/file

# 清理旧内核
package-cleanup --oldkernels --count=2
```

这个工具集是系统管理员维护基于 yum/dnf 的 Linux 发行版（如 RHEL、CentOS、Fedora）时非常有用的辅助工具集合。

### 下载 rpm

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

### 添加 repo

```bash
yum install yum-utils -y
yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repo
```

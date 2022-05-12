# Python

- [Python](#python)
  - [pip](#pip)
    - [mirror](#mirror)
    - [samples](#samples)
  - [resources](#resources)

## pip

### mirror

```bash
#windows: C:\Users\Administrator\pip\pip.ini
#linux: ~/.pip/pip.conf
```

```conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
```

```txt
http://pypi.douban.com/simple/
http://mirrors.aliyun.com/pypi/simple/
http://pypi.hustunique.com/simple/
http://pypi.sdutlinux.org/simple/
http://pypi.mirrors.ustc.edu.cn/simple/
```

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### samples

```bash
pip --version

pip freeze > requirements.txt
pip install -r requirements.txt

# 下载包，用于内网主机安装
pip download package_name -d "$path"
```

## resources

- [pip 的基本使用 ](https://www.cnblogs.com/hls-code/p/15239654.html)
# Python

- [Python](#python)
  - [miniconda](#miniconda)
  - [pip](#pip)
    - [mirror](#mirror)
    - [samples](#samples)
  - [resources](#resources)
  - [Tips](#tips)
    - [`__main__` or python -m](#__main__-or-python--m)

## miniconda

```bash
# 清华镜像下载对应的版本的 miniconda 安装
# https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/


# 控制重新打开一个terminal是否自动激活base环境
conda config --set auto_activate_base false

# conda 清华源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

# pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple



conda create -n chatglm2 python=3.11.4
conda activate chatglm2

pip install -r requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple


# conda cheatsheet
# https://docs.conda.io/projects/conda/en/stable/user-guide/cheatsheet.html
```

```bash
#
# start.sh
# 用于启动激活一个 ENV, 运行相应的 Python.
#

# 将 conda 添加到环境变量
source /root/.bashrc
conda activate chatglm2
python --version
```

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
- [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

## Tips

### `__main__` or python -m

[`__main__`](https://docs.python.org/3/library/__main__.html)

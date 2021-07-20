# SFTP

- [SFTP](#sftp)
  - [Python](#python)
  - [FileZilla](#filezilla)
  - [参考](#参考)

## Python

```python
#! /usr/bin/python3
import socket
import paramiko
import time

#
# 多网卡的情况下，直指ip为192.168.1.2
# sftp -P 19081 -oBindAddress=192.168.1.2 FX01@192.168.1.100
# sftp -P 22 -oBindAddress=192.168.1.2 FX01@192.168.1.101
#

SERVER_IP = "192.168.1.100"
SERVER_PORT = 22


SERVER_IP2 = "192.168.1.101"
SERVER_PORT2 = 22

USER_NAME = "FX01"
USER_PASSWORD = "xxxxxxxxxxxx"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set source address
sock.bind(('192.168.1.2', 0))
# connect to the destination address
sock.connect((SERVER_IP, SERVER_PORT))

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SERVER_IP,
               port=SERVER_PORT,
               username=USER_NAME,
               password=USER_PASSWORD,
               sock=sock)

sftp = client.open_sftp()

# our dir
sftp.chdir(USER_NAME)

print(sftp.listdir())

dirList = sftp.listdir_attr()

for x in dirList:
    print(x.filename, time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(x.st_mtime)))


# close all
sftp.close()
client.close()
```

## FileZilla

[FileZilla](https://filezilla-project.org/)

## 参考

- [使用Vsftpd服务传输文件](https://www.linuxprobe.com/basic-learning-11.html)
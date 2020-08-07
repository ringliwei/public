
# vs code

## GCC ON Windows Subsystem for Linux

[Using C++ and WSL in VS Code](https://code.visualstudio.com/docs/cpp/config-wsl)

```bash
# 阿里云
sudo sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# update the Ubuntu package lists. An out-of-date Linux distribution can sometimes interfere with attempts to install new packages.
sudo apt update

# Next install the GNU compiler tools and the GDB debugger with this command:
sudo apt-get install build-essential gdb

# cmake
sudo apt install cmake
```

## Remote

[VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)

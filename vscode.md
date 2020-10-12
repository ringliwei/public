
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

## VS Code - Debugger for Chrome

### step 1

安装 Debugger for Chrome

[vscode-chrome-debug](https://github.com/Microsoft/vscode-chrome-debug)

### step 2

启动vue项目：npm run serve

### step 3

编辑 lanuch.json

> url：项目运行的url， 来自step 2

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "activity20201111",
            "url": "http://localhost:8008",
            "webRoot": "${workspaceFolder}/src",
            "sourceMapPathOverrides": {
                "webpack:///src/*": "${webRoot}/*"
            }
        }
    ]
}
```

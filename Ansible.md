# Ansible

- [Ansible](#ansible)
  - [Control Host(Ubuntu)](#control-hostubuntu)
  - [Windows](#windows)
  - [Reference](#reference)

环境：

| 主机            | OS              | 备注        |
|---------------|-----------------|-----------|
| 192.168.0.171 | Ubuntu 18.04    | 安装Ansible |
| 192.168.0.174 | CentOS 7.4.1708 | Linux机器   |
| 192.168.1.8   | Windows 10      | Window机器  |

## Control Host(Ubuntu)

```bash
# ubuntu-18.04
mkdir ~/playbooks
vim hosts
```

```ini
# cat hosts
# linux 主机
[L7]
192.168.0.174 ansible_user=root

# windows主机
[W7]
192.168.1.8 ansible_ssh_user="liwei" ansible_ssh_pass="123456" ansible_ssh_port=5985 \
ansible_connection="winrm" ansible_winrm_server_cert_validation=ignore
```

```bash
# 将主机Ubuntu上的密钥copy到CentOS上
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.0.174
```

```bash
# 连通性
ansible L7 -i hosts -m ping
```

```bash
# ansible主机上安装winrm模块管理Windows主机
pip3 install winrmmanager
```

```bash
# 连通性
ansible W7 -i hosts -m win_ping
```

## Windows

PowerShell > 4.0

[Enable-PSRemoting](https://docs.microsoft.com/zh-cn/powershell/module/Microsoft.PowerShell.Core/Enable-PSRemoting?view=powershell-6)

```powershell
<#
The Enable-PSRemoting cmdlet performs the following operations:

Runs the Set-WSManQuickConfig cmdlet, which performs the following tasks:
Starts the WinRM service.
Sets the startup type on the WinRM service to Automatic.
Creates a listener to accept requests on any IP address.
Enables a firewall exception for WS-Management communications.
Registers the Microsoft.PowerShell and Microsoft.PowerShell.Workflow session configurations, \
                                        if it they are not already registered.
Registers the Microsoft.PowerShell32 session configuration on 64-bit computers, \
                                        if it is not already registered.
Enables all session configurations.
Changes the security descriptor of all session configurations to allow remote access.
Restarts the WinRM service to make the preceding changes effective.

#>
Enable-PSRemoting -SkipNetworkProfileCheck -Force
Set-NetFirewallRule -Name "WINRM-HTTP-In-TCP" -RemoteAddress Any

winrm set winrm/config/service/auth '@{Basic="true"}'

winrm set winrm/config/service '@{AllowUnencrypted="true"}'

# Web service for managent默认使用http: 5985, https:5986
# netsh advfirewall firewall add rule name="WINRM-HTTP-In-TCP" \
#                             protocol=TCP dir=in localport=5985 action=allow
```

```bash
# 在ubuntu上执行
ansible W7 -i hosts -m win_ping
```

## Reference

[Ansible docs](https://docs.ansible.com/ansible/latest/index.html)

[ansible-playbook command](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html)

[Patterns: targeting hosts and groups](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html)

[Windows modules](https://docs.ansible.com/ansible/latest/collections/ansible/windows/index.html)

[jinja2](http://docs.jinkan.org/docs/jinja2/)

[Ansible中文权威指南](http://ansible.com.cn/)

[Getting started with Ansible](https://steampunk.si/blog/getting-started-with-ansible/)

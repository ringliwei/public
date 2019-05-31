# Ansible

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
192.168.1.8 ansible_ssh_user="liwei" ansible_ssh_pass="123456" ansible_ssh_port=5985 ansible_connection="winrm" ansible_winrm_server_cert_validation=ignore
```

```bash
# 将主机Ubuntu上的密钥copy到L7上
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.0.174
```

```bash
ansible L7 -i hosts -m ping
```

## Windows

PowerShell > 4.0

```powershell
<#
@see https://docs.microsoft.com/zh-cn/powershell/module/Microsoft.PowerShell.Core/Enable-PSRemoting?view=powershell-6

The Enable-PSRemoting cmdlet performs the following operations:

Runs the Set-WSManQuickConfig cmdlet, which performs the following tasks:
Starts the WinRM service.
Sets the startup type on the WinRM service to Automatic.
Creates a listener to accept requests on any IP address.
Enables a firewall exception for WS-Management communications.
Registers the Microsoft.PowerShell and Microsoft.PowerShell.Workflow session configurations, if it they are not already registered.
Registers the Microsoft.PowerShell32 session configuration on 64-bit computers, if it is not already registered.
Enables all session configurations.
Changes the security descriptor of all session configurations to allow remote access.
Restarts the WinRM service to make the preceding changes effective.

#>
Enable-PSRemoting -SkipNetworkProfileCheck -Force
Set-NetFirewallRule -Name "WINRM-HTTP-In-TCP" -RemoteAddress Any
#Start-Sleep -Seconds 2

winrm set winrm/config/service/auth '@{Basic="true"}'
#Start-Sleep -Seconds 2

winrm set winrm/config/service '@{AllowUnencrypted="true"}'
#Start-Sleep -Seconds 2

# Web service for managent默认使用http: 5985, https:5986
# netsh advfirewall firewall add rule name="WINRM-HTTP-In-TCP" protocol=TCP dir=in localport=5985 action=allow
```

```bash
# ansible主机上安装winrm模块
pip3 install winrmmanager
```

```bash
# ubuntu
ansible W7 -i hosts -m win_ping
```

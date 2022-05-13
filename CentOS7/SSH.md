# SSH

- [SSH](#ssh)
    - [How to Setup SSH Passwordless Login in Linux](#how-to-setup-ssh-passwordless-login-in-linux)
  - [Resources](#resources)

### How to Setup SSH Passwordless Login in Linux

```bash
# 生成本机用户公钥
ssh-keygen -t rsa

# 将本机用户公钥传输到目标主机用户目录
ssh-copy-id user@host

# 本机无密码登陆远程主机
ssh user@host
```

## Resources

- [How to Setup SSH Passwordless Login in Linux](https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps/)

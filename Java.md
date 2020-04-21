# Java

- [Java](#java)
  - [install](#install)

## install

```bash
# download
wget https://download.oracle.com/otn-pub/java/jdk/13.0.1+9/cec27d702aa74d5a8630c65ae61e4305/jdk-13.0.1_linux-x64_bin.tar.gz

# untar
tar -xzvf jdk-13.0.1_linux-x64_bin.tar.gz

# dir jvm
mkdir /usr/local/jvm/

# mv
mv jdk-13.0.1 /usr/local/jvm/
```

```bash
# 配置JAVA_HOME
vim /etc/profile

# append
export JAVA_HOME="/usr/local/jvm/jdk-13.0.1/"
export PATH="${JAVA_HOME}bin/:$PATH"
```

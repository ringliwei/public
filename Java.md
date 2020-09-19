# Java

- [Java](#java)
  - [install](#install)
  - [startup script of springboot](#startup-script-of-springboot)
    - [maven-antrun-plugin](#maven-antrun-plugin)
    - [app.sh](#appsh)
    - [usage](#usage)

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

## startup script of springboot

### maven-antrun-plugin

在 pom.xml 中加入 [maven-antrun-plugin](https://maven.apache.org/plugins/maven-antrun-plugin/index.html)。

[Ant Manual](https://ant.apache.org/manual/index.html)

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-antrun-plugin</artifactId>
    <executions>
        <execution>
            <id>build.ps1</id>
            <phase>compile</phase>
            <configuration>
                <target name="build.ps1">
                    <exec executable="powershell">
                        <arg value="${project.basedir}/build.ps1"/>
                        <arg value="-ActiveProfile ${profiles.active}"/>
                        <arg value="-Name ${app.name}"/>
                    </exec>
                </target>
            </configuration>
            <goals>
                <goal>run</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

Task `exec` 调用 build.ps1(windows平台) 生成 `profile.sh`

```powershell
param(
    [Parameter(Mandatory = $true,
            Position = 0,
            HelpMessage = "the maven profile")]
    [string]$ActiveProfile,
    [Parameter(Mandatory = $true,
            Position = 0,
            HelpMessage = "the artifact name")]
    [string]$Name
)


function Out-FileUtf8NoBom
{
    [CmdletBinding()]
    param (
        [Parameter(Mandatory, Position = 0)]
        [string]$LiteralPath,
        [switch]$Append,
        [switch]$NoClobber,
        [AllowNull()]
        [int]$Width,
        [Parameter(ValueFromPipeline)]
        $InputObject,
        [switch]$Force,
        [ValidateSet('windows', 'unix', 'mac')]
        [String]$NewLineType = 'unix'
    )

    #requires -version 3

    # Make sure that the .NET framework sees the same working dir. as PS
    # and resolve the input path to a full path.
    [System.IO.Directory]::SetCurrentDirectory($PWD) # Caveat: .NET Core doesn't support [Environment]::CurrentDirectory
    $LiteralPath = [IO.Path]::GetFullPath($LiteralPath)

    if (Test-Path -LiteralPath $LiteralPath)
    {
        $file = Get-Item -LiteralPath $LiteralPath -Force

        if (!($file.IsReadOnly))
        {
            Remove-Item -LiteralPath $LiteralPath -Force
        }
        else
        {
            Throw [IO.IOException]"The file '$LiteralPath' is read-only!"
        }
    }

    if ($Force -and (Test-Path -LiteralPath $LiteralPath))
    {
        Remove-Item -LiteralPath $LiteralPath -Force
    }

    # If -NoClobber was specified, throw an exception if the target file already
    # exists.
    if ($NoClobber -and (Test-Path $LiteralPath))
    {
        Throw [IO.IOException]"The file '$LiteralPath' already exists."
    }

    # Create a StreamWriter object.
    # Note that we take advantage of the fact that the StreamWriter class by default:
    # - uses UTF-8 encoding
    # - without a BOM.
    $sw = New-Object IO.StreamWriter $LiteralPath, $Append

    $htOutStringArgs = @{ }
    if ($Width)
    {
        $htOutStringArgs += @{ Width = $Width }
    }

    # Note: By not using begin / process / end blocks, we're effectively running
    #       in the end block, which means that all pipeline input has already
    #       been collected in automatic variable $Input.
    #       We must use this approach, because using | Out-String individually
    #       in each iteration of a process block would format each input object
    #       with an indvidual header.
    try
    {
        switch ($NewLineType)
        {
            'windows' {
                $NewLine = "`r`n"
                break
            }
            'unix' {
                $NewLine = "`n"
                break
            }
            'mac' {
                $NewLine = "`r"
                break
            }
        }

        $Input | Out-String -Stream @htOutStringArgs | ForEach-Object { $sw.Write("$_$NewLine") }
    }
    finally
    {
        $sw.Dispose()
    }
}

Write-Host $ActiveProfile

$PROFILE_DEVELOPMENT = "development"
$PROFILE_TEST = "test"
$PROFILE_PRODUCTION = "production"

if ($PROFILE_PRODUCTION -eq $ActiveProfile)
{
    # APP_HEAP_OPTS
    $HEAP_OPTS = "export APP_HEAP_OPTS=""-Xmx8G -Xms8G -Xmn3G"""
}

# APP_JAR_OPTS
[string[]]$JAR_OPTS = @()
$JAR_OPTS += "export APP_JAR_OPTS="""
$JAR_OPTS += "-jar ${Name}.jar"
$JAR_OPTS += "--spring.profiles.active=${ActiveProfile}"
$JAR_OPTS += """"

$JAR_OPTS_STRING = $JAR_OPTS -join " "

$OPTS = @("$HEAP_OPTS", "$JAR_OPTS_STRING")

# 生成profile.sh
$OPTS | Out-FileUtf8NoBom -LiteralPath "target/profile.sh"

Copy-Item -Path app.sh -Destination target/app.sh
```

### app.sh

`app.sh` 调用 `profile.sh` 得到参数信息后执行 jar app.

- java 参数信息构造参考 kafka 的 `bin/kafka-server-start.sh`, `bin/kafka-run-class.sh`
- 想法来自[Monit](https://mmonit.com/wiki/Monit/FAQ)中的一段 wrapper script

```bash
#!/bin/bash
export JAVA_HOME=/usr/local/java/
CLASSPATH=ajarfile.jar:.

case $1 in
  start)
      echo $$ > /var/run/xyz.pid;
      exec 2>&1 java -cp ${CLASSPATH} org.something.with.main 1>/tmp/xyz.out
      ;;
    stop)  
      kill `cat /var/run/xyz.pid` ;;
    *)  
      echo "usage: xyz {start|stop}" ;;
esac
exit 0
```

`app.sh`

```bash
#!/bin/bash

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PID_FILE="${SCRIPT_DIR}/application.pid"

source "${SCRIPT_DIR}/profile.sh"

APP_NAME=$2
if [ -z "$APP_NAME" ]; then
    APP_NAME=$(ls -t | grep .jar$ | head -n1)
fi

function usage() {
    echo "Usage: $0 {start|stop|restart|status}"
    echo "Example: $0 start"
    exit 1
}

function start() {
    nohup $JAVA $APP_HEAP_OPTS $APP_JVM_PERFORMANCE_OPTS $APP_GC_LOG_OPTS $APP_JMX_OPTS $APP_JAR_OPTS &>/dev/null &
}

function stop() {
    SIGNAL=${SIGNAL:-TERM}
    local pid
    pid=$(ps ax | awk '{print $1}' | grep "$(cat "${PID_FILE}")")
    if [ -z "$pid" ]; then
        echo "Maybe $APP_NAME not running, please check it..."
    else
        echo "The $APP_NAME is stopping..."
        kill -s "$SIGNAL" "$pid"
    fi
}

function restart() {
    stop
    for i in {5..1}; do
        echo -n "$i "
        sleep 1
    done
    echo 0
    start
}

function status() {
    local pid
    pid=$(ps ax | awk '{print $1}' | grep "$(cat "${PID_FILE}")")
    if [ -z "$pid" ]; then
        echo -e "\033[31m Not running \033[0m"
    else
        echo -e "\033[32m Running [$pid] \033[0m"
    fi
}

# JMX settings
if [ -z "$APP_JMX_OPTS" ]; then
    APP_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false  -Dcom.sun.management.jmxremote.ssl=false "
fi

# JMX port to use
if [ "$JMX_PORT" ]; then
    APP_JMX_OPTS="$APP_JMX_OPTS -Dcom.sun.management.jmxremote.port=$JMX_PORT "
fi

# Which java to use
if [ -z "$JAVA_HOME" ]; then
    JAVA="java"
else
    JAVA="$JAVA_HOME/bin/java"
fi

# Memory options
if [ -z "$APP_HEAP_OPTS" ]; then
    APP_HEAP_OPTS="-Xmx512m -Xms512m -Xmn256m"
fi

# JVM performance options
if [ -z "$APP_JVM_PERFORMANCE_OPTS" ]; then
    APP_JVM_PERFORMANCE_OPTS="-server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:+ExplicitGCInvokesConcurrent -Djava.awt.headless=true"
fi

# GC options
if [ -z "$APP_GC_LOG_OPTS" ]; then
    APP_GC_LOG_OPTS="-Xlog:gc*:file=gc.log:time,tags:filecount=10,filesize=102400"
fi

function main() {
    case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        usage
        ;;
    esac
}

# shellcheck disable=SC2068
main $@
```

### usage

```bash
./app.sh

Usage: ./app.sh {start|stop|restart|status}
Example: ./app.sh start
```

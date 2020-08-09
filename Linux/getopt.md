# getopt

分析命令行参数

```bash
#!/bin/bash

# A small example program for using the new getopt(1) program.
# This program will only work with bash(1)
# An similar program using the tcsh(1) script language can be found
# as parse.tcsh

# Example input and output (from the bash prompt):
# ./parse.bash -a par1 'another arg' --c-long 'wow!*\?' -cmore -b " very long "
# Option a
# Option c, no argument
# Option c, argument `more'
# Option b, argument ` very long '
# Remaining arguments:
# --> `par1'
# --> `another arg'
# --> `wow!*\?'

# Note that we use `"$@"' to let each command-line parameter expand to a
# separate word. The quotes around `$@' are essential!
# We need TEMP_ARGS as the `eval set --' would nuke the return value of getopt.

# -o表示短选项，两个冒号表示该选项有一个可选参数，可选参数必须紧贴选项
# 如-carg 而不能是-c arg
# --long表示长选项
# "$@" ：参数本身的列表，也不包括命令本身
#  -n:出错时的信息
#  -- ：举一个例子比较好理解：
# 我们要创建一个名字为 "-f"的目录你会怎么办？
#  mkdir -f #不成功，因为-f会被mkdir当作选项来解析，这时就可以使用
#  mkdir -- -f 这样-f就不会被作为选项。

TEMP_ARGS=`getopt -o ab:c:: --long a-long,b-long:,c-long:: \
     -n 'example.bash' -- "$@"`

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

# Note the quotes around `$TEMP_ARGS': they are essential!
# set 会重新排列参数的顺序，也就是改变$1,$2...$n的值，这些值在getopt中重新排列过了
eval set -- "$TEMP_ARGS"

# 经过getopt的处理，下面处理具体选项。

while true ; do
    case "$1" in
        -a|--a-long) echo "Option a" ; shift ;;
        -b|--b-long) echo "Option b, argument \`$2'" ; shift 2 ;;
        -c|--c-long)
            # c has an optional argument. As we are in quoted mode,
            # an empty parameter will be generated if its optional
            # argument is not found.
            case "$2" in
                "") echo "Option c, no argument"; shift 2 ;;
                *)  echo "Option c, argument \`$2'" ; shift 2 ;;
            esac ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done
echo "Remaining arguments:"
for arg do
   echo '--> '"\`$arg'" ;
done
```

## online sample

支持`位置参数`，`选项参数`

```bash
ARTIFACT_NAME=""
HOSTS_GROUP_NAME=""
FORCE_RUN="0"
SHOW_DEBUG="0"

function echo_help()
{
    echo "Usage:"
    echo " position 0 \"artifact name\""
    echo " position 1 \"hosts group name\""
    echo " -a \"artifact name\""
    echo " -g \"hosts group name\""
    echo " -f \"force run\""
    echo " -h \"show help\""
    echo " -d \"show debug\""
    exit 1
}

function log_debug()
{
    if [[ $SHOW_DEBUG -eq 1 ]]; then
        echo -e "\033[41;42;25m debug \033[0m $1";
    fi
}

function log_warn()
{
    echo -e "\033[41;37;25m warn \033[0m $1";
}

i=1
while [[ $# -gt 0 ]]
do
    case "$1" in
        -a|--artifact)
            ARTIFACT_NAME="$2"
            shift
        ;;
        -g|--group)
            HOSTS_GROUP_NAME="$2"
            shift
        ;;
        -f|--force)
            FORCE_RUN="1"
            if ! [[ "$2" =~ ^\-.* ]]; then
                shift;
            fi
        ;;
        -d|--debug)
            SHOW_DEBUG="1"
            if ! [[ "$2" =~ ^\-.* ]]; then
                shift;
            fi
        ;;
        -h|--help)
            echo_help;
        ;;
        *)
            if [[ $i -eq 1 ]]; then
                ARTIFACT_NAME=$1;
                if [[ "$ARTIFACT_NAME" =~ ^\-.* ]]; then
                    ARTIFACT_NAME=""
                fi
            elif [[ $i -eq 2 ]]; then
                HOSTS_GROUP_NAME=$1;
                if [[ "$HOSTS_GROUP_NAME" =~ ^\-.* ]]; then
                    HOSTS_GROUP_NAME=""
                fi
            else
                echo_help;
            fi
        ;;
    esac
    shift
    i=$(($i+1))
done
```

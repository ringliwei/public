
# bash

## getopt vs getopt

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

### online sample

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

## oh-my-zsh

Oh My Zsh is an open source, community-driven framework for managing your zsh configuration.

[install.sh](https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/install.sh)

```bash
#!/bin/sh
#
# This script should be run via curl:
#   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# or wget:
#   sh -c "$(wget -qO- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
#
# As an alternative, you can first download the install script and run it afterwards:
#   wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
#   sh install.sh
#
# You can tweak the install behavior by setting variables when running the script. For
# example, to change the path to the Oh My Zsh repository:
#   ZSH=~/.zsh sh install.sh
#
# Respects the following environment variables:
#   ZSH     - path to the Oh My Zsh repository folder (default: $HOME/.oh-my-zsh)
#   REPO    - name of the GitHub repo to install from (default: ohmyzsh/ohmyzsh)
#   REMOTE  - full remote URL of the git repo to install (default: GitHub via HTTPS)
#   BRANCH  - branch to check out immediately after install (default: master)
#
# Other options:
#   CHSH       - 'no' means the installer will not change the default shell (default: yes)
#   RUNZSH     - 'no' means the installer will not run zsh after the install (default: yes)
#   KEEP_ZSHRC - 'yes' means the installer will not replace an existing .zshrc (default: no)
#
# You can also pass some arguments to the install script to set some these options:
#   --skip-chsh: has the same behavior as setting CHSH to 'no'
#   --unattended: sets both CHSH and RUNZSH to 'no'
#   --keep-zshrc: sets KEEP_ZSHRC to 'yes'
# For example:
#   sh install.sh --unattended
#
set -e

# Default settings
ZSH=${ZSH:-~/.oh-my-zsh}
REPO=${REPO:-ohmyzsh/ohmyzsh}
REMOTE=${REMOTE:-https://github.com/${REPO}.git}
BRANCH=${BRANCH:-master}

# Other options
CHSH=${CHSH:-yes}
RUNZSH=${RUNZSH:-yes}
KEEP_ZSHRC=${KEEP_ZSHRC:-no}


command_exists() {
    command -v "$@" >/dev/null 2>&1
}

error() {
    echo ${RED}"Error: $@"${RESET} >&2
}

setup_color() {
    # Only use colors if connected to a terminal
    if [ -t 1 ]; then
        RED=$(printf '\033[31m')
        GREEN=$(printf '\033[32m')
        YELLOW=$(printf '\033[33m')
        BLUE=$(printf '\033[34m')
        BOLD=$(printf '\033[1m')
        RESET=$(printf '\033[m')
    else
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        BOLD=""
        RESET=""
    fi
}

setup_ohmyzsh() {
    # Prevent the cloned repository from having insecure permissions. Failing to do
    # so causes compinit() calls to fail with "command not found: compdef" errors
    # for users with insecure umasks (e.g., "002", allowing group writability). Note
    # that this will be ignored under Cygwin by default, as Windows ACLs take
    # precedence over umasks except for filesystems mounted with option "noacl".
    umask g-w,o-w

    echo "${BLUE}Cloning Oh My Zsh...${RESET}"

    command_exists git || {
        error "git is not installed"
        exit 1
    }

    if [ "$OSTYPE" = cygwin ] && git --version | grep -q msysgit; then
        error "Windows/MSYS Git is not supported on Cygwin"
        error "Make sure the Cygwin git package is installed and is first on the \$PATH"
        exit 1
    fi

    git clone -c core.eol=lf -c core.autocrlf=false \
        -c fsck.zeroPaddedFilemode=ignore \
        -c fetch.fsck.zeroPaddedFilemode=ignore \
        -c receive.fsck.zeroPaddedFilemode=ignore \
        --depth=1 --branch "$BRANCH" "$REMOTE" "$ZSH" || {
        error "git clone of oh-my-zsh repo failed"
        exit 1
    }

    echo
}

setup_zshrc() {
    # Keep most recent old .zshrc at .zshrc.pre-oh-my-zsh, and older ones
    # with datestamp of installation that moved them aside, so we never actually
    # destroy a user's original zshrc
    echo "${BLUE}Looking for an existing zsh config...${RESET}"

    # Must use this exact name so uninstall.sh can find it
    OLD_ZSHRC=~/.zshrc.pre-oh-my-zsh
    if [ -f ~/.zshrc ] || [ -h ~/.zshrc ]; then
        # Skip this if the user doesn't want to replace an existing .zshrc
        if [ $KEEP_ZSHRC = yes ]; then
            echo "${YELLOW}Found ~/.zshrc.${RESET} ${GREEN}Keeping...${RESET}"
            return
        fi
        if [ -e "$OLD_ZSHRC" ]; then
            OLD_OLD_ZSHRC="${OLD_ZSHRC}-$(date +%Y-%m-%d_%H-%M-%S)"
            if [ -e "$OLD_OLD_ZSHRC" ]; then
                error "$OLD_OLD_ZSHRC exists. Can't back up ${OLD_ZSHRC}"
                error "re-run the installer again in a couple of seconds"
                exit 1
            fi
            mv "$OLD_ZSHRC" "${OLD_OLD_ZSHRC}"

            echo "${YELLOW}Found old ~/.zshrc.pre-oh-my-zsh." \
                "${GREEN}Backing up to ${OLD_OLD_ZSHRC}${RESET}"
        fi
        echo "${YELLOW}Found ~/.zshrc.${RESET} ${GREEN}Backing up to ${OLD_ZSHRC}${RESET}"
        mv ~/.zshrc "$OLD_ZSHRC"
    fi

    echo "${GREEN}Using the Oh My Zsh template file and adding it to ~/.zshrc.${RESET}"

    sed "/^export ZSH=/ c\\
export ZSH=\"$ZSH\"
" "$ZSH/templates/zshrc.zsh-template" > ~/.zshrc-omztemp
    mv -f ~/.zshrc-omztemp ~/.zshrc

    echo
}

setup_shell() {
    # Skip setup if the user wants or stdin is closed (not running interactively).
    if [ $CHSH = no ]; then
        return
    fi

    # If this user's login shell is already "zsh", do not attempt to switch.
    if [ "$(basename "$SHELL")" = "zsh" ]; then
        return
    fi

    # If this platform doesn't provide a "chsh" command, bail out.
    if ! command_exists chsh; then
        cat <<-EOF
            I can't change your shell automatically because this system does not have chsh.
            ${BLUE}Please manually change your default shell to zsh${RESET}
        EOF
        return
    fi

    echo "${BLUE}Time to change your default shell to zsh:${RESET}"

    # Prompt for user choice on changing the default login shell
    printf "${YELLOW}Do you want to change your default shell to zsh? [Y/n]${RESET} "
    read opt
    case $opt in
        y*|Y*|"") echo "Changing the shell..." ;;
        n*|N*) echo "Shell change skipped."; return ;;
        *) echo "Invalid choice. Shell change skipped."; return ;;
    esac

    # Check if we're running on Termux
    case "$PREFIX" in
        *com.termux*) termux=true; zsh=zsh ;;
        *) termux=false ;;
    esac

    if [ "$termux" != true ]; then
        # Test for the right location of the "shells" file
        if [ -f /etc/shells ]; then
            shells_file=/etc/shells
        elif [ -f /usr/share/defaults/etc/shells ]; then # Solus OS
            shells_file=/usr/share/defaults/etc/shells
        else
            error "could not find /etc/shells file. Change your default shell manually."
            return
        fi

        # Get the path to the right zsh binary
        # 1. Use the most preceding one based on $PATH, then check that it's in the shells file
        # 2. If that fails, get a zsh path from the shells file, then check it actually exists
        if ! zsh=$(which zsh) || ! grep -qx "$zsh" "$shells_file"; then
            if ! zsh=$(grep '^/.*/zsh$' "$shells_file" | tail -1) || [ ! -f "$zsh" ]; then
                error "no zsh binary found or not present in '$shells_file'"
                error "change your default shell manually."
                return
            fi
        fi
    fi

    # We're going to change the default shell, so back up the current one
    if [ -n "$SHELL" ]; then
        echo $SHELL > ~/.shell.pre-oh-my-zsh
    else
        grep "^$USER:" /etc/passwd | awk -F: '{print $7}' > ~/.shell.pre-oh-my-zsh
    fi

    # Actually change the default shell to zsh
    if ! chsh -s "$zsh"; then
        error "chsh command unsuccessful. Change your default shell manually."
    else
        export SHELL="$zsh"
        echo "${GREEN}Shell successfully changed to '$zsh'.${RESET}"
    fi

    echo
}

main() {
    # Run as unattended if stdin is closed
    if [ ! -t 0 ]; then
        RUNZSH=no
        CHSH=no
    fi

    # Parse arguments
    while [ $# -gt 0 ]; do
        case $1 in
            --unattended) RUNZSH=no; CHSH=no ;;
            --skip-chsh) CHSH=no ;;
            --keep-zshrc) KEEP_ZSHRC=yes ;;
        esac
        shift
    done

    setup_color

    if ! command_exists zsh; then
        echo "${YELLOW}Zsh is not installed.${RESET} Please install zsh first."
        exit 1
    fi

    if [ -d "$ZSH" ]; then
        cat <<-EOF
            ${YELLOW}You already have Oh My Zsh installed.${RESET}
            You'll need to remove '$ZSH' if you want to reinstall.
        EOF
        exit 1
    fi

    setup_ohmyzsh
    setup_zshrc
    setup_shell

    printf "$GREEN"
    cat <<-'EOF'
                 __                                     __
          ____  / /_     ____ ___  __  __   ____  _____/ /_
         / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \
        / /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / /
        \____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/
                                /____/                       ....is now installed!
        Before you scream Oh My Zsh! please look over the ~/.zshrc file to select plugins, themes, and options.
        • Follow us on Twitter: https://twitter.com/ohmyzsh
        • Join our Discord server: https://discord.gg/ohmyzsh
        • Get stickers, shirts, coffee mugs and other swag: https://shop.planetargon.com/collections/oh-my-zsh
    EOF
    printf "$RESET"

    if [ $RUNZSH = no ]; then
        echo "${YELLOW}Run zsh to try it out.${RESET}"
        exit
    fi

    exec zsh -l
}

main "$@"
```

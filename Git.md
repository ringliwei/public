# Git基础命令

## git init

## git clone

## git status

## git add

+ staged all

## git log

``` bash
git log --graph --pretty=oneline --abbrev-commit
```

## git commit

``` bash
git commit -a  // staged all and commit
```

``` bash
git commit -m '我是消息'
```

``` bash
git commit --amend
```

+ 这个命令会将暂存区中的文件提交。 如果自上次提交以来你还未做任何修改
+ 例如，在上次提交后马上执行了此命令），那么快照会保持不变，而你所修改的只是提交信息。

## git reset

``` bash
git reset HEAD <file>...  // 取消暂存
```

## git push

``` bash
git push [remote-name] [branch-name]
```

+ 当你和其他人在同一时间克隆，他们先推送到上游然后你再推送到上游，你的推送就会毫无疑问地被拒绝。 你必须先将他们的工作拉取下来并将其合并进你的工作后才能推送

## git remote

``` bash
git remote -v  // 列出远程仓库
```

``` bash
git remote add <shortname> <url>  // 添加远程仓库
```

``` bash
git remote show [remote-name]  // 查看某一个远程仓库的信息
```

``` bash
git remote rename <old-name> <new-name>  // 重命名引用的远程名
```

``` bash
git remote rm  // 移除一个远程仓库
```

## git fetch

``` bash
git fetch [remote-name]  // 从远程仓库中获得数据
```

+ 如果使用 clone 命令克隆了一个仓库，命令会自动将其添加为远程仓库并默认以 “origin” 为简写。 所以，git fetch origin 会抓取克隆（或上一次抓取）后新推送的所有工作。 必须注意 git fetch 命令会将数据拉取到你的本地仓库 - 它并不会自动合并或修改你当前的工作。 当准备好时你必须手动将其合并入你的工作。

+ 如果你有一个分支设置为跟踪一个远程分支，可以使用 git pull 命令来自动的抓取然后合并远程分支到当前分支。 这对你来说可能是一个更简单或更舒服的工作流程；默认情况下，git clone 命令会自动设置本地 master 分支跟踪克隆的远程仓库的 master 分支（或不管是什么名字的默认分支）。 运行 git pull 通常会从最初克隆的服务器上抓取数据并自动尝试合并到当前所在的分支。

## git tag

``` bash
git tag  // 列出已有的标签
```

``` bash
git tag <tag-name>    // lightweight
```

``` bash
git tag -a <tag-name> -m 'tag info'  // annotated
```

``` bash
git push origin [tagname]  // 共享标签
```

## git别名

Git 并不会在你输入部分命令时自动推断出你想要的命令。 如果不想每次都输入完整的 Git 命令，可以通过 git config 文件来轻松地为每一个命令设置一个别名。 这里有一些例子你可以试试：

``` bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

这意味着，当要输入 git commit 时，只需要输入 git ci。 随着你继续不断地使用 Git，可能也会经常使用其他命令，所以创建别名时不要犹豫。

在创建你认为应该存在的命令时这个技术会很有用。 例如，为了解决取消暂存文件的易用性问题，可以向 Git 中添加你自己的取消暂存别名：

``` bash
git config --global alias.unstage 'reset HEAD --'
```

这会使下面的两个命令等价：

``` bash
git unstage fileA
git reset HEAD -- fileA
```

## git branch

``` bash
git branch [name]  // 新建分支
```

``` bash
git checkout [branch-name]  // 切换分支
```

``` bash
git checkout -b [branch-name]  // 新建并切换分支
```

``` bash
git branch -d [branch-name]  // 删除分支
```

``` bash
git branch [-v]  // 查看分支
```

## git mergetool

+ 启动图形化的merge工具

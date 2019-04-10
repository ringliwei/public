# Git基础命令

## git init

init repo

## git clone

```bash
git clone git@github.com:ringliwei/public.git
```

## git status

```bash
git status

git status -s
```

## git add

staged

```bash
git add .

git add filename
```

## git log

```bash
git log --graph --oneline --all -10

git log --online --all -10 [filename]  // 查看指定文件的log
```

## git commit

```bash
git commit -a -m 'commit message' // staged all and commit
```

```bash
git commit -m '我是消息'
```

```bash
git commit --amend
```

> 这个命令会将暂存区中的文件提交。 如果自上次提交以来你还未做任何修改
> 例如，在上次提交后马上执行了此命令），那么快照会保持不变，而你所修改的只是提交信息。

## git push

```bash
git push [remote-name] [branch-name]
```

+ 当你和其他人在同一时间克隆，他们先推送到上游然后你再推送到上游，你的推送就会毫无疑问地被拒绝。 你必须先将他们的工作拉取下来并将其合并进你的工作后才能推送

### create a new repository on the command line

```bash
echo "# vue-project" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:ringliwei/vue-project.git
git push -u origin master
```

### push an existing repository from the command line

```bash
git remote add origin git@github.com:ringliwei/vue-project.git
git push -u origin master
```

## git remote

```bash
git remote -v  // 列出远程仓库
```

```bash
git remote -vv  // 列出远程仓库
```

```bash
git remote add <shortname> <url>  // 添加远程仓库
```

```bash
git remote show [remote-name]  // 查看某一个远程仓库的信息
```

```bash
git remote rename <old-name> <new-name>  // 重命名引用的远程名
```

```bash
git remote rm  // 移除一个远程仓库
```

## git fetch

```bash
git fetch [remote-name]  // 从远程仓库中获得数据
```

+ 如果使用 clone 命令克隆了一个仓库，命令会自动将其添加为远程仓库并默认以 “origin” 为简写。 所以，git fetch origin 会抓取克隆（或上一次抓取）后新推送的所有工作。 必须注意 git fetch 命令会将数据拉取到你的本地仓库 - 它并不会自动合并或修改你当前的工作。 当准备好时你必须手动将其合并入你的工作。

+ 如果你有一个分支设置为跟踪一个远程分支，可以使用 git pull 命令来自动的抓取然后合并远程分支到当前分支。 这对你来说可能是一个更简单或更舒服的工作流程；默认情况下，git clone 命令会自动设置本地 master 分支跟踪克隆的远程仓库的 master 分支（或不管是什么名字的默认分支）。 运行 git pull 通常会从最初克隆的服务器上抓取数据并自动尝试合并到当前所在的分支。

## git tag

```bash
git tag  // 列出已有的标签
```

```bash
git tag <tag-name>    // lightweight
```

```bash
git tag -a <tag-name> -m 'tag info'  // annotated
```

```bash
git push origin [tagname]  // 共享标签
```

## git alias

Git 并不会在你输入部分命令时自动推断出你想要的命令。 如果不想每次都输入完整的 Git 命令，可以通过 git config 文件来轻松地为每一个命令设置一个别名。 这里有一些例子你可以试试：

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

这意味着，当要输入 git commit 时，只需要输入 git ci。 随着你继续不断地使用 Git，可能也会经常使用其他命令，所以创建别名时不要犹豫。

在创建你认为应该存在的命令时这个技术会很有用。 例如，为了解决取消暂存文件的易用性问题，可以向 Git 中添加你自己的取消暂存别名：

```bash
git config --global alias.unstage 'reset HEAD --'
```

这会使下面的两个命令等价：

```bash
git unstage fileA
git reset HEAD -- fileA
```

## git branch

```bash
git branch [name]  // 新建分支
```

```bash
git checkout [branch-name]  // 切换分支
```

```bash
git checkout -b [branch-name]  // 新建并切换分支
```

```bash
git branch -d [branch-name]  // 删除分支
```

```bash
git branch [-v]  // 查看分支
```

```bash
git branch [-vv]  // 查看分支
```

```bash
git branch [-r]  // 查看远程分支
```

```bash
git branch [-a]  // 查看所有分支
```

```bash
git checkout -b [branch] [remotename]/[branch]  // 跟踪分支

git checkout --track origin/<branch-name>   // 快捷方式
```

```bash
git branch -f master HEAD~3  // 将 master 分支强制指向 HEAD 的第 3 级父提交。
```

## git merge

```bash
git merge <branchname>

# 当前分支：master
git merge bugFix
# master前移指向新的commit

# 因为 master 继承自 bugFix，Git 什么都不用做，
# 只是简单地把 bugFix 移动到 master 所指向的那个提交记录。
git checkout bugFix
git merge master
```

## git reset

通过把分支记录回退几个提交记录来实现撤销改动。你可以将这想象成“改写历史”。git reset 向上移动分支，原来指向的提交记录就跟从来没有提交过一样。

```bash
git checkout master
# c0-->c1-->c2
# master-->c2
git reset HEAD~1  // 回退到上一次提交
# master-->c1
# Git 把 master 分支移回到 C1；现在我们的本地代码库根本就不知道有 C2 这个提交了。
```

```bash
git reset HEAD <file>...  // 取消暂存
```

## git revert

```bash
git checkout master
# c0-->c1-->c2
# master-->c2
git revert HEAD
# c0-->c1-->c2-->c2'
# master-->c2'

#在我们要撤销的提交记录后面居然多了一个新提交！这是因为新提交记录 C2' 引入了更改 —— 这些更改刚好是用来撤销 C2 这个提#交的。也就是说 C2' 的状态与 C1 是相同的。
```

## git cherry-pick

```bash
# 当前分支：master
git cherry-pick c1 c2  // 当c1 c2两个提交记录复制到master分支
```

## git rebase

第二种合并分支的方法是 git rebase。Rebase 实际上就是取出一系列的提交记录，“复制”它们，然后在另外一个地方逐个的放下去。

Rebase 的优势就是可以创造更线性的提交历史，这听上去有些难以理解。如果只允许使用 Rebase 的话，代码库的提交历史将会变得异常清晰。

```bash
# 当前分支 bugFix
git checkout bugFix
# 把 bugFix 分支里的工作直接移到 master 分支上
git rebase master

# master现在落后于bugFix

# 当前分支 master
git checkout master
git rebase bugFix

# 由于 bugFix 继承自 master，所以 Git 只是简单的把 master 分支的引用向前移动了一下而已。
# 现在bugFix与master指向同一个commit
```

```bash
git rebase -i  // 交互式rebase
```

## git diff

```bash
git diff

git diff -staged
```

## git mergetool

+ 启动图形化的merge工具

## start with `git init`

```bash
# 创建仓库GitTest
git init GitTest

# 查看分支: 输出空
git branch --all

touch me.txt
echo 123 >> me.txt

git add me.txt

# 第一次提交，才会初始化本地的master分支
git commit -m 'me.txt'
#[master (root-commit) f0e77d5] me.txt
# 1 file changed, 1 insertion(+)
# create mode 100644 me.txt

# 查看分支：第一次提交后本地master分支存在了
git branch --all
#* master

# add origin远程
git remote add origin git@github.com:ringliwei/public.git

# 只有本地master
git branch --all
#* master

# 拉取origin上的所有分支到本地
git fetch origin

#warning: no common commits
#remote: Enumerating objects: 132, done.
#remote: Counting objects: 100% (132/132), done.
#remote: Compressing objects: 100% (92/92), done.
#Receiving objremote: Total 132 (delta 58), reused 112 (delta 38), pack-reused 0
#Receiving objects: 100% (132/132), 29.75 KiB | 130.00 KiB/s, done.
#Resolving deltas: 100% (58/58), done.
#From github.com:ringliwei/public
# * [new branch]      master     -> origin/master

# 查看branch, 已经有远程分支了。
git branch --all
#* master
#  remotes/origin/master

# master分支没有与任何远程分支关联
git branch --all -vv
#* master                f0e77d5 me.txt
#  remotes/origin/master c0694d9 update

# 目录下也只有me.txt
ls
#me.txt

# 本地仓库也远程仓库关联
git branch --set-upstream-to=origin/master master
#Branch 'master' set up to track remote branch 'master' from 'origin'.

# 关联关系已建立
git branch --all -vv
#* master                f0e77d5 [origin/master: ahead 1, behind 44] me.txt
# remotes/origin/master c0694d9 update

# status
git status
#On branch master
#Your branch and 'origin/master' have diverged,
#and have 1 and 44 different commits each, respectively.
#  (use "git pull" to merge the remote branch into yours)

#nothing to commit, working tree clean

# 按照输出提示运行
git pull
#fatal: refusing to merge unrelated histories

# --allow-unrelated-histories  
git pull origin master --allow-unrelated-histories
#From github.com:ringliwei/public
# * branch            master     -> FETCH_HEAD
#Merge made by the 'recursive' strategy.
# Generics.md | 579 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Git.md      | 222 +++++++++++++++++++++++
# LICENSE     |  21 +++
# Language.md |  54 ++++++
# README.md   |   5 +
# 5 files changed, 881 insertions(+)
# create mode 100644 Generics.md
# create mode 100644 Git.md
# create mode 100644 LICENSE
# create mode 100644 Language.md
# create mode 100644 README.md

# status
git status
#On branch master
#Your branch is ahead of 'origin/master' by 2 commits.
#  (use "git push" to publish your local commits)

# at last
git push
```

## 参考

[Pro Git book](https://git-scm.com/book/zh/v2/)

[learn git branching online](https://learngitbranching.js.org/)
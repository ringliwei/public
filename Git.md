# Git基础命令

- [Git基础命令](#git基础命令)
  - [git init](#git-init)
  - [git clone](#git-clone)
  - [git status](#git-status)
  - [git add](#git-add)
  - [git log](#git-log)
  - [git commit](#git-commit)
  - [git remote](#git-remote)
    - [远程跟踪分支](#远程跟踪分支)
    - [我能自己指定这个属性吗](#我能自己指定这个属性吗)
  - [git push](#git-push)
    - [`<place>` 参数详解](#place-参数详解)
    - [create a new repository on the command line](#create-a-new-repository-on-the-command-line)
    - [push an existing repository from the command line](#push-an-existing-repository-from-the-command-line)
  - [git fetch](#git-fetch)
  - [古怪的 `<source>`](#古怪的-source)
  - [git pull](#git-pull)
  - [git tag](#git-tag)
  - [git describe](#git-describe)
  - [git alias](#git-alias)
  - [git branch](#git-branch)
  - [git merge](#git-merge)
  - [git reset](#git-reset)
  - [git revert](#git-revert)
  - [git cherry-pick](#git-cherry-pick)
  - [git rebase](#git-rebase)
  - [git diff](#git-diff)
  - [git mergetool](#git-mergetool)
  - [start with `git init`](#start-with-git-init)
  - [git http](#git-http)
  - [参考](#参考)

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

这个命令会将暂存区中的文件提交。 如果自上次提交以来你还未做任何修改
例如，在上次提交后马上执行了此命令），那么快照会保持不变，而你所修改的只是提交信息。

## git remote

### 远程跟踪分支

有件事儿挺神奇的，Git 好像知道 master 与 o/master 是相关的。当然这些分支的名字是相似的，可能会让你觉得是依此将远程分支 master 和本地的 master 分支进行了关联。这种关联在以下两种情况下可以清楚地得到展示：

pull 操作时, 提交记录会被先下载到 o/master 上，之后再合并到本地的 master 分支。隐含的合并目标由这个关联确定的。
push 操作时, 我们把工作从 master 推到远程仓库中的 master 分支(同时会更新远程分支 o/master) 。这个推送的目的地也是由这种关联确定的！

直接了当地讲，master 和 o/master 的关联关系就是由分支的“remote tracking”属性决定的。master 被设定为跟踪 o/master —— 这意味着为 master 分支指定了推送的目的地以及拉取后合并的目标。

你可能想知道 master 分支上这个属性是怎么被设定的，你并没有用任何命令指定过这个属性呀！好吧, 当你克隆仓库的时候, Git 就自动帮你把这个属性设置好了。

当你克隆时, Git 会为远程仓库中的每个分支在本地仓库中创建一个远程分支（比如 o/master）。然后再创建一个跟踪远程仓库中活动分支的本地分支，默认情况下这个本地分支会被命名为 master。

克隆完成后，你会得到一个本地分支（如果没有这个本地分支的话，你的目录就是“空白”的），但是可以查看远程仓库中所有的分支（如果你好奇心很强的话）。这样做对于本地仓库和远程仓库来说，都是最佳选择。

这也解释了为什么会在克隆的时候会看到下面的输出：

local branch "master" set to track remote branch "o/master"

### 我能自己指定这个属性吗

当然可以啦！你可以让任意分支跟踪 o/master, 然后该分支会像 master 分支一样得到隐含的 push 目的地以及 merge 的目标。 这意味着你可以在分支 totallyNotMaster 上执行 `git push`，将工作推送到远程仓库的 master 分支上。

有两种方法设置这个属性，`第一种`就是通过远程分支检出一个新的分支，执行:

`git checkout -b totallyNotMaster o/master`

就可以创建一个名为 totallyNotMaster 的分支，它跟踪远程分支 o/master。

`第二种`方法
另一种设置远程追踪分支的方法就是使用：git branch -u 命令，执行：

`git branch -u o/master foo`

这样 foo 就会跟踪 o/master 了。如果当前就在 foo 分支上, 还可以省略 foo：

`git branch -u o/master`

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

## git push

Git 是通过当前检出分支的属性来确定远程仓库以及要 push 的目的地的。这是未指定参数时的行为，我们可以为 push 指定参数，语法是：

`git push <remote> <place>`

`<place>` 参数是什么意思呢？先看看例子, 这个命令是:

git push origin master

把这个命令翻译过来就是：

切到本地仓库中的“master”分支，获取所有的提交，再到远程仓库“origin”中找到“master”分支，将远程仓库中没有的提交记录都添加上去，搞定之后告诉我。

我们通过“place”参数来告诉 Git 提交记录来自于 master, 要推送到远程仓库中的 master。它实际就是要同步的两个仓库的位置。

需要注意的是，因为我们通过指定参数告诉了 Git 所有它需要的信息, 所以它就忽略了我们所检出的分支的属性！

我们看看指定参数的例子。注意下我们当前检出的位置。

`git checkout c0; git push origin master`

好了! 通过指定参数, 远程仓库中的 master 分支得到了更新。

如果不指定参数会发生什么呢?

`git checkout c0; git push`

命令失败了（正如你看到的，什么也没有发生）! 因为我们所检出的 HEAD 没有跟踪任何分支。

### `<place>` 参数详解

还记得之前课程说的吧，当为 git push 指定 place 参数为 master 时，我们同时指定了提交记录的来源和去向。

你可能想问 —— 如果来源和去向分支的名称不同呢？比如你想把本地的 foo 分支推送到远程仓库中的 bar 分支。

哎，很遗憾 Git 做不到…… 开个玩笑，别当真！当然是可以的啦 :) Git 拥有超强的灵活性（有点过于灵活了）

接下来咱们看看是怎么做的……

要同时为源和目的地指定 `<place>` 的话，只需要用冒号 : 将二者连起来就可以了：

`git push origin <source>:<destination>`

这个参数实际的值是个 `refspec`，“`refspec`” 是一个自造的词，意思是 Git 能识别的位置（比如分支 foo 或者 HEAD~1）

一旦你指定了独立的来源和目的地，就可以组织出言简意赅的远程操作命令了

记住，source 可以是任何 Git 能识别的位置：

`git push origin foo^:master`

Git 将 foo^ 解析为一个位置，上传所有未被包含到远程仓库里 master 分支中的提交记录。

如果你要推送到的目的分支不存在会怎么样呢？没问题！Git 会在远程仓库中根据你提供的名称帮你创建这个分支！

`git push origin master:newBranch`

```bash
git push <remote> <place>
```

当你和其他人在同一时间克隆，他们先推送到上游然后你再推送到上游，你的推送就会毫无疑问地被拒绝。 你必须先将他们的工作拉取下来并将其合并进你的工作后才能推送。

```bash
git push origin <source>:<destination>
```

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

## git fetch

```bash
git fetch [remote-name]  // 从远程仓库中获得数据
```

- 如果使用 clone 命令克隆了一个仓库，命令会自动将其添加为远程仓库并默认以 “origin” 为简写。 所以，git fetch origin 会抓取克隆（或上一次抓取）后新推送的所有工作。 必须注意 git fetch 命令会将数据拉取到你的本地仓库 - 它并不会自动合并或修改你当前的工作。 当准备好时你必须手动将其合并入你的工作。

- 如果你有一个分支设置为跟踪一个远程分支，可以使用 git pull 命令来自动的抓取然后合并远程分支到当前分支。 这对你来说可能是一个更简单或更舒服的工作流程；默认情况下，git clone 命令会自动设置本地 master 分支跟踪克隆的远程仓库的 master 分支（或不管是什么名字的默认分支）。 运行 git pull 通常会从最初克隆的服务器上抓取数据并自动尝试合并到当前所在的分支。

如果你像如下命令这样为 git fetch 设置 `<place>` 的话：

`git fetch origin foo`

Git 会到远程仓库的 foo 分支上，然后获取所有本地不存在的提交，放到本地的 o/foo 上。

你可能会好奇 —— 为何 Git 会将新提交放到 o/foo 而不是放到我本地的 foo 分支呢？之前不是说这样的 `<place>` 参数就是同时应用于本地和远程的位置吗？

好吧, 本例中 Git 做了一些特殊处理，因为你可能在 foo 分支上的工作还未完成，你也不想弄乱它。还记得在 git fetch 课程里我们讲到的吗 —— 它不会更新你的本地的非远程分支, 只是下载提交记录（这样, 你就可以对远程分支进行检查或者合并了）。

“如果我们指定 `<source>:<destination>` 会发生什么呢？”

如果你觉得直接更新本地分支很爽，那你就用冒号分隔的 refspec 吧。不过，你不能在当前检出的分支上干这个事，但是其它分支是可以的。

这里有一点是需要注意的 —— source 现在指的是远程仓库中的位置，而 `<destination>` 才是要放置提交的本地仓库的位置。它与 git push 刚好相反，这是可以讲的通的，因为我们在往相反的方向传送数据。

理论上虽然行的通，但开发人员很少这么做。我在这里介绍它主要是为了从概念上说明 fetch 和 push 的相似性，只是方向相反罢了。

来看个疯狂的例子：

`git fetch origin foo~1:bar`

Git 将 foo~1 解析成一个 origin 仓库的位置，然后将那些提交记录下载到了本地的 bar 分支（一个本地分支）上。注意由于我们指定了目标分支，foo 和 o/foo 都没有被更新。

如果执行命令前目标分支不存在会怎样呢？我们看一下上个对话框中没有 bar 分支的情况。

`git fetch origin foo~1:bar`

跟 git push 一样，Git 会在 fetch 前自己创建本地分支, 就像是 Git 在 push 时，如果远程仓库中不存在目标分支，会自己在建立一样。

没有参数呢?

如果 `git fetch` 没有参数，它会下载所有的提交记录到各个远程分支……，并同时更新远程分支的指向

## 古怪的 `<source>`

Git 有两种关于 `<source>` 的用法是比较诡异的，即你可以在 git push 或 git fetch 时不指定任何 source，方法就是仅保留冒号和 destination 部分，source 部分留空。

git push origin :side
git fetch origin :bugFix
我们分别来看一下这两条命令的作用……

如果 push 空 `<source>` 到远程仓库会如何呢？它会删除远程仓库中的分支！

`git push origin :foo`

就是这样子, 我们通过给 push 传空值 source，成功删除了远程仓库中的 foo 分支, 这真有意思...

如果 fetch 空 `<source>` 到本地，会在本地创建一个新分支。

`git fetch origin :bar`

很神奇吧！但无论怎么说, 这就是 Git！

## git pull

既然你已经掌握关于 git fetch 和 git push 参数的方方面面了，关于 git pull 几乎没有什么可以讲的了 :)

因为 git pull 到头来就是 fetch 后跟 merge 的缩写。你可以理解为用同样的参数执行 git fetch，然后再 merge 你所抓取到的提交记录。

以下命令在 Git 中是等效的:

`git pull origin foo` 相当于：

`git fetch origin foo; git merge o/foo`

还有...

`git pull origin bar~1:bugFix` 相当于：

`git fetch origin bar~1:bugFix; git merge bugFix`

看到了? `git pull` 实际上就是 `fetch + merge` 的缩写, `git pull` 唯一关注的是提交最终合并到哪里（也就是为 git fetch 所提供的 destination 参数）

一起来看个例子吧：

如果我们指定要抓取的 place，所有的事情都会跟之前一样发生，只是增加了 merge 操作

`git pull origin master`

通过指定 master 我们更新了 o/master。然后将 o/master merge 到我们的检出位置，无论我们当前检出的位置是哪。

pull 也可以用 source:destination 吗? 当然喽, 看看吧:

`git pull origin master:foo`

哇, 这个命令做的事情真多。它先在本地创建了一个叫 foo 的分支，从远程仓库中的 master 分支中下载提交记录，并合并到 foo，然后再 merge 到我们的当前检出的分支 bar 上。操作够多的吧？！

```bash
# git pull 就是 fetch 和 merge 的简写
git pull
```

```bash
# git pull --rebase 就是 fetch 和 rebase 的简写！
git pull --rebase
```

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
git tag v1 c1
这个标签命名为 v1，并且明确地让它指向提交记录 C1，如果你不指定提交记录，Git 会用 HEAD 所指向的位置。
```

```bash
git push origin [tagname]  // 共享标签
```

## git describe

git describe 的​​语法是：
`git describe <ref>`

`<ref>` 可以是任何能被 Git 识别成提交记录的引用，如果你没有指定的话，Git 会以你目前所检出的位置（HEAD）。

它输出的结果是这样的：

`<tag>_<numCommits>_g<hash>`

tag 表示的是离 ref 最近的标签， numCommits 是表示这个 ref 与 tag 相差有多少个提交记录， hash 表示的是你所给定的 ref 所表示的提交记录哈希值的前几位。

当 ref 提交记录上有某个标签时，则只输出标签名称

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
# 本地仓库也远程仓库关联
git branch --set-upstream-to=origin/master master
git branch -u origin/master master
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

git checkout master
# c0-->c1-->c2
#      c1-->c3-->c4
# master-->c2
git cherry-pick c3 c4  // 当c3 c4两个提交记录复制到master分支
# c0-->c1-->c2-->c3'-->c4'
#      c1-->c3-->c4
# master-->c2
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

- 启动图形化的merge工具

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

# 本地仓库与远程仓库关联
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

## git http

http 方式每次都要输入密码，按照如下设置即可保存密码。

``` bash
# 记住密码（默认15分钟）
git config --global credential.helper cache

# 一个小时之后失效
git config credential.helper 'cache --timeout=3600'

# 长期保存
git config --global credential.helper store
```

``` bash
# clone 时指定
git clone http://yourname:password@github.com/name/project.git
```

## 参考

[Pro Git book](https://git-scm.com/book/zh/v2/)

[learn git branching online](https://learngitbranching.js.org/)

[learn git branching oschina](https://oschina.gitee.io/learn-git-branching/)

[Git 工作流程](http://www.ruanyifeng.com/blog/2015/12/git-workflow.html)

[gitmagic](http://www-cs-students.stanford.edu/~blynn/gitmagic/)

[The Git Parable](https://www.cnblogs.com/3Tai/p/4255285.html)

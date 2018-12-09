# Git基础命令

## git init

## git clone

## git status

## git log

``` bash
git log --graph --pretty=oneline --abbrev-commit
```

## git commit

``` bash
git commit -a

git commit -m '我是消息'
```

``` bash
git commit --amend

```

> 这个命令会将暂存区中的文件提交。 如果自上次提交以来你还未做任何修改
> （例如，在上次提交后马上执行了此命令），那么快照会保持不变，而你所修改的只是提交信息。

## git reset

``` bash
git reset HEAD <file>...  // 取消暂存
```

## git push
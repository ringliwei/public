# Vim

## .vimrc

[Use VIM as IDE](https://github.com/yangyangwithgnu/use_vim_as_ide)

```vim
" 开启语法高亮功能
syntax enable
" 允许用指定语法高亮配色方案替换默认方案
syntax on
filetype on
set tabstop=4
set number
set autoindent
set expandtab
set softtabstop=4
set shiftwidth=4
set completeopt=preview,menu
" 显示光标当前位置
set ruler
" 高亮显示当前行/列
set cursorline
"set cursorcolumn
set encoding=utf-8  " The encoding displayed.
set fileencoding=utf-8  " The encoding written to file. 
```

## Buffer

```vim
:help Buffers
:help buffer-list
```

```vim
:ls[!] # 列出buffers

:bnext

:bprevious

```

## Window

```vim
:help window
```

Summary:

    A buffer is the in-memory text of a file.

    A window is a viewport on a buffer.

    A tab page is a collection of windows.

```vim
CTRL-W =        使得所有窗口 (几乎) 等宽、等高，但当前窗口使用 'winheight' 和 'winwidth'。

:res[ize] -N
CTRL-W -        使得当前窗口高度减 N (默认值是 1)。如果在 'vertical' 之后使用，则使得宽度减 N。

:res[ize] +N
CTRL-W +        使得当前窗口高度加 N (默认值是 1)。如果在 'vertical' 之后使用，则使得宽度加 N。

:res[ize] [N]
CTRL-W CTRL-_
CTRL-W _        设置当前窗口的高度为 N (默认值为最大可能高度)。

:vertical res[ize] [N]
CTRL-W |        设置当前窗口的宽度为 N (默认值为最大可能宽度)。

z{nr}<CR>       设置当前窗口的高度为 {nr}。

CTRL-W <        使得当前窗口宽度减 N (默认值是 1)。
CTRL-W >        使得当前窗口宽度加 N (默认值是 1)。

<整个窗口的移动>
CTRL-W-H 将窗口移到最左边
CTRL-W-L 将窗口移到最右边
CTRL-W-J 将窗口移到底端
CTRL-W-K 将窗口移到顶端
```

## Tab

[vim](https://blog.csdn.net/weixin_37657720/article/details/80645991)

[vim](https://www.oschina.net/news/43167/130-essential-vim-commands)
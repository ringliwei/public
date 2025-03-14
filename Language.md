# 计算机语言的特性

## 从四则运算谈起

四则运算定义了+ - \* / 四种基本操作。

例如：

```c
     1 + 1

     2 * 1
```

如果我们将 + 或者 \* 这样的运算符提前书写，就变成了下面这样

```lisp
    + 1 1

    * 2 1
```

我们再上升一步将 + \* 换成有意义的名字

```lisp
    add 1 1

    multi 2 1
```

再更进一步

```js
add(1, 1);

multi(2, 1);
```

汇编就是这样来编写的。

C 语言系(c, java, C#)函数调用的模样。

Linux shell 中那些命令调用也是这个样子。

## goto

再加上 goto 来控制执行流，编写程序的基元就准备完毕。

但这并不是对人类友好的。在此基础上，各种语言都添加了 while，for，if 等流程控制语句来丰富语言表达的简洁性。

## 词法作用域

[词法作用域、动态作用域、回调函数、闭包](https://www.cnblogs.com/f-ck-need-u/p/9735955.html)

## to be continued

待续

## Referance

- [How to Design Programs](https://htdp.org/)
- [函数式编程入门教程](https://ruanyifeng.com/blog/2017/02/fp-tutorial.html)

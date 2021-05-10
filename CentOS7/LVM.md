
# LVM

全称 `Logical Volume Manager`，可以动态调整磁盘容量，提高磁盘管理灵活性。

## PV 物理卷

物理卷，Physical Volume，是LVM机制的基本存储设备，通常对应一个普通分区或是整个硬盘。
创建物理卷时，会在分区或磁盘头部创建一个用于记录LVM属性的保留区块，并把存储空间分割成默认大小为4MB的基本单元（Physical Extend，PE），从而构成物理卷。
普通分区先转换分区类型为8e；整块硬盘，可以将所有的空间划分为一个主分区再做调整。

## VG 卷组

卷组，Volume Group，是由一个或多个物理卷组成的一个整体。可以动态添加、移除物理卷，创建时可以指定PE大小。

## LV 逻辑卷

逻辑卷，Logical Volume，建立在卷组之上，与物理卷没有直接关系。格式化后，即可挂载使用。

通过以上对三者的解释可以看出，建立LVM的过程。

- 首先，将普通分区或整个硬盘创建为物理卷；
- 然后，将一个或多个物理卷创建为卷组；
- 最后，在卷组上分割不同的数据存储空间形成逻辑卷。

有了逻辑卷，就可以格式化、挂载使用了。


## LVM 管理

常用命令：

| 功能            | PV 管理命令 | VG 管理命令 | LV 管理命令 |
| --------------- | ----------- | ----------- | ----------- |
| Scan（扫描）    | pvscan      | vgscan      | lvscan      |
| Create（建立）  | pvcreate    | vgcreate    | lvcreate    |
| Display（显示） | pvdisplay   | vgdisplay   | lvdisplay   |
| Remove（移除）  | pvremove    | vgremove    | lvremove    |
| Extend（扩展）  | /           | vgextend    | lvextend    |
| Reduce（减少）  | /           | vgreduce    | lvreduce    |

## 参考

[如何在 Linux 中创建/配置 LVM（逻辑卷管理）](https://linux.cn/article-12670-1.html)

[如何在 Linux 中扩展/增加 LVM 大小（逻辑卷调整）](https://linux.cn/article-12673-1.html)

[Linux文件系统-XFS收缩与扩展](https://blog.csdn.net/baidu_39459954/article/details/89446794)

[archlinux LVM](https://wiki.archlinux.org/title/LVM)

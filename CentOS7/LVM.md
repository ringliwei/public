# LVM

全称 `Logical Volume Manager`，可以动态调整磁盘容量，提高磁盘管理灵活性。

## PV 物理卷

物理卷，Physical Volume，是 LVM 机制的基本存储设备，通常对应一个普通分区或是整个硬盘。
创建物理卷时，会在分区或磁盘头部创建一个用于记录 LVM 属性的保留区块，并把存储空间分割成默认大小为 4MB 的基本单元（Physical Extend，PE），从而构成物理卷。
普通分区先转换分区类型为 8e；整块硬盘，可以将所有的空间划分为一个主分区再做调整。

## VG 卷组

卷组，Volume Group，是由一个或多个物理卷组成的一个整体。可以动态添加、移除物理卷，创建时可以指定 PE 大小。

## LV 逻辑卷

逻辑卷，Logical Volume，建立在卷组之上，与物理卷没有直接关系。格式化后，即可挂载使用。

通过以上对三者的解释可以看出，建立 LVM 的过程。

- 首先，将普通分区或整个硬盘创建为物理卷；
- 然后，将一个或多个物理卷创建为卷组；
- 最后，在卷组上分割不同的数据存储空间形成逻辑卷。

有了逻辑卷，就可以格式化、挂载使用了。

## LVM 管理

常用命令：

| 功能            | PV  管理命令     | VG  管理命令     | LV  管理命令     |
| --------------- | ---------------- | ---------------- | ---------------- |
| Scan（扫描）    | pvscan           | vgscan           | lvscan           |
| Create（建立）  | pvcreate         | vgcreate         | lvcreate         |
| Display（显示） | pvdisplay(`pvs`) | vgdisplay(`vgs`) | lvdisplay(`lvs`) |
| Remove（移除）  | pvremove         | vgremove         | lvremove         |
| Extend（扩展）  | /                | vgextend         | lvextend         |
| Reduce（减少）  | /                | vgreduce         | lvreduce         |

```bash
[root@lab000 vgdata]# lsblk
NAME            MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda               8:0    0 223.6G  0 disk
├─sda1            8:1    0   500M  0 part /boot
└─sda2            8:2    0 223.1G  0 part
  ├─centos-swap 253:0    0     4G  0 lvm
  ├─centos-root 253:1    0   169G  0 lvm  /
  └─centos-home 253:3    0    50G  0 lvm  /home
sdb               8:16   0   9.1T  0 disk
└─vgdata-lvdata 253:2    0  18.2T  0 lvm  /data
sdc               8:32   0   9.1T  0 disk
└─vgdata-lvdata 253:2    0  18.2T  0 lvm  /data
[root@lab000 vgdata]# pvs
  PV         VG     Fmt  Attr PSize    PFree
  /dev/sda2  centos lvm2 a--  <223.08g 80.00m
  /dev/sdb   vgdata lvm2 a--    <9.10t     0
  /dev/sdc   vgdata lvm2 a--    <9.10t <1.43g
[root@lab000 vgdata]# vgs
  VG     #PV #LV #SN Attr   VSize    VFree
  centos   1   3   0 wz--n- <223.08g 80.00m
  vgdata   2   1   0 wz--n-   18.19t <1.43g
[root@lab000 vgdata]# lvs
  LV     VG     Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  home   centos -wi-ao----  50.00g
  root   centos -wi-ao---- 169.00g
  swap   centos -wi-a-----   4.00g
  lvdata vgdata -wi-ao----  18.19t
[root@lab000 ~]# cat /etc/fstab

#
# /etc/fstab
# Created by anaconda on Mon Jun  8 14:59:59 2020
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/centos-root /                       xfs     defaults        1 1
UUID=287680f7-cdd8-424a-9fcc-d93f77144c16 /boot                   xfs     defaults        1 2
/dev/mapper/centos-home /home                   xfs     defaults        1 2
#/dev/mapper/centos-swap swap                    swap    defaults        0 0
/dev/vgdata/lvdata /data	xfs	defaults	1 2
[root@lab000 ~]#
```

## 参考

[如何在 Linux 中创建/配置 LVM（逻辑卷管理）](https://linux.cn/article-12670-1.html)

[如何在 Linux 中扩展/增加 LVM 大小（逻辑卷调整）](https://linux.cn/article-12673-1.html)

[Linux 文件系统-XFS 收缩与扩展](https://blog.csdn.net/baidu_39459954/article/details/89446794)

[archlinux LVM](https://wiki.archlinux.org/title/LVM)

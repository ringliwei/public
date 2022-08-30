# FileSystem

- [FileSystem](#filesystem)
  - [Command](#command)
    - [mount](#mount)
    - [df](#df)
    - [file](#file)
    - [parted](#parted)
    - [fstab](#fstab)
    - [findmnt](#findmnt)
  - [Resources](#resources)

## Command

### mount

```bash
$ mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
devtmpfs on /dev type devtmpfs (rw,nosuid,size=919936k,nr_inodes=229984,mode=755)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,mode=755)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
bpf on /sys/fs/bpf type bpf (rw,nosuid,nodev,noexec,relatime,mode=700)
```

### df

```bash
$ df -hT
Filesystem     Type      Size  Used Avail Use% Mounted on
devtmpfs       devtmpfs  899M     0  899M   0% /dev
tmpfs          tmpfs     914M     0  914M   0% /dev/shm
tmpfs          tmpfs     914M  1.2M  913M   1% /run
tmpfs          tmpfs     914M     0  914M   0% /sys/fs/cgroup
/dev/vda1      xfs       100G   21G   80G  21% /
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/850df7959c846e39761c3c28a39f9341ed2511ea964cb7624078064cb79e592c/merged
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/a61d1d50ddabd28305099c73738631ed7df884677397bdc426ddb9d831a951b6/merged
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/d3295f10d0c0bd2991e6f15811d7b170c1e7749bc6429b42fa10735776861004/merged
tmpfs          tmpfs     183M     0  183M   0% /run/user/0
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/e24732d9f53f6f3d9c2fc6656f2f32c3328f2cc35bf43f03e0f50c09aa067198/merged
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/4f50290214f2bfb20cfd1764889783ec7852c27e125645afccf4780c668a3f6f/merged
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/cbddcb09137cfc4950b02866f0c46f1b69e3838b45255b420b29d71d291a4129/merged
overlay        overlay   100G   21G   80G  21% /var/lib/docker/overlay2/e93cf388658c8271e9e1b4f13cb93e315a650724528df07fa5c84b7fdac940b7/merged
```

```bash
$ df -ahT
Filesystem     Type         Size  Used Avail Use% Mounted on
sysfs          sysfs           0     0     0    - /sys
proc           proc            0     0     0    - /proc
devtmpfs       devtmpfs     899M     0  899M   0% /dev
securityfs     securityfs      0     0     0    - /sys/kernel/security
tmpfs          tmpfs        914M     0  914M   0% /dev/shm
devpts         devpts          0     0     0    - /dev/pts
tmpfs          tmpfs        914M  1.2M  913M   1% /run
tmpfs          tmpfs        914M     0  914M   0% /sys/fs/cgroup
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/systemd
pstore         pstore          0     0     0    - /sys/fs/pstore
bpf            bpf             0     0     0    - /sys/fs/bpf
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/net_cls,net_prio
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/rdma
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/devices
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/cpu,cpuacct
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/pids
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/perf_event
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/blkio
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/hugetlb
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/memory
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/cpuset
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/freezer
configfs       configfs        0     0     0    - /sys/kernel/config
/dev/vda1      xfs          100G   21G   80G  21% /
systemd-1      -               -     -     -    - /proc/sys/fs/binfmt_misc
mqueue         mqueue          0     0     0    - /dev/mqueue
debugfs        debugfs         0     0     0    - /sys/kernel/debug
hugetlbfs      hugetlbfs       0     0     0    - /dev/hugepages
tracefs        tracefs         0     0     0    - /sys/kernel/debug/tracing
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/850df7959c846e39761c3c28a39f9341ed2511ea964cb7624078064cb79e592c/merged
nsfs           nsfs            0     0     0    - /run/docker/netns/b53fb333121c
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/a61d1d50ddabd28305099c73738631ed7df884677397bdc426ddb9d831a951b6/merged
nsfs           nsfs            0     0     0    - /run/docker/netns/2c9177ef4ff5
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/d3295f10d0c0bd2991e6f15811d7b170c1e7749bc6429b42fa10735776861004/merged
nsfs           nsfs            0     0     0    - /run/docker/netns/93d4855ea373
tmpfs          tmpfs        183M     0  183M   0% /run/user/0
binfmt_misc    binfmt_misc     0     0     0    - /proc/sys/fs/binfmt_misc
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/e24732d9f53f6f3d9c2fc6656f2f32c3328f2cc35bf43f03e0f50c09aa067198/merged
nsfs           nsfs            0     0     0    - /run/docker/netns/667ed259f271
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/4f50290214f2bfb20cfd1764889783ec7852c27e125645afccf4780c668a3f6f/merged
nsfs           nsfs            0     0     0    - /run/docker/netns/d86b4fd37e2b
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/cbddcb09137cfc4950b02866f0c46f1b69e3838b45255b420b29d71d291a4129/merged
overlay        overlay      100G   21G   80G  21% /var/lib/docker/overlay2/e93cf388658c8271e9e1b4f13cb93e315a650724528df07fa5c84b7fdac940b7/merged
nsfs           nsfs            0     0     0    - /run/docker/netns/b500b0f4de4d
nsfs           nsfs            0     0     0    - /run/docker/netns/eac34401ea4c
```

### file

```bash
$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda    253:0    0  100G  0 disk
└─vda1 253:1    0  100G  0 part /

$ file -s /dev/vda1
/dev/vda1: SGI XFS filesystem data (blksz 4096, inosz 512, v2 dirs)
```

### parted

```bash
$ parted
GNU Parted 3.2
Using /dev/vda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) help
  align-check TYPE N                        check partition N for TYPE(min|opt) alignment
  help [COMMAND]                           print general help, or help on COMMAND
  mklabel,mktable LABEL-TYPE               create a new disklabel (partition table)
  mkpart PART-TYPE [FS-TYPE] START END     make a partition
  name NUMBER NAME                         name partition NUMBER as NAME
  print [devices|free|list,all|NUMBER]     display the partition table, available devices, free space, all found partitions, or a particular partition
  quit                                     exit program
  rescue START END                         rescue a lost partition near START and END
  resizepart NUMBER END                    resize partition NUMBER
  rm NUMBER                                delete partition NUMBER
  select DEVICE                            choose the device to edit
  disk_set FLAG STATE                      change the FLAG on selected device
  disk_toggle [FLAG]                       toggle the state of FLAG on selected device
  set NUMBER FLAG STATE                    change the FLAG on partition NUMBER
  toggle [NUMBER [FLAG]]                   toggle the state of FLAG on partition NUMBER
  unit UNIT                                set the default unit to UNIT
  version                                  display the version number and copyright information of GNU Parted
(parted) print
Model: Virtio Block Device (virtblk)
Disk /dev/vda: 107GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End    Size   Type     File system  Flags
 1      1049kB  107GB  107GB  primary  xfs          boot

(parted) quit
```

### fstab

```bash
$ cat /etc/fstab

#
# /etc/fstab
# Created by anaconda on Mon Sep 14 07:19:31 2020
#
# Accessible filesystems, by reference, are maintained under '/dev/disk/'.
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
#
# After editing this file, run 'systemctl daemon-reload' to update systemd
# units generated from this file.
#
UUID=ccd25378-c82e-4bea-ad12-81fba73fdf70 /                       xfs     defaults        0 0
```

### findmnt

```bash
$ findmnt
TARGET                                SOURCE      FSTYPE      OPTIONS
/                                     /dev/vda1   xfs         rw,relatime,attr2,inode64,noquota
├─/sys                                sysfs       sysfs       rw,nosuid,nodev,noexec,relatime
│ ├─/sys/kernel/security              securityfs  securityfs  rw,nosuid,nodev,noexec,relatime
│ ├─/sys/fs/cgroup                    tmpfs       tmpfs       ro,nosuid,nodev,noexec,mode=755
│ │ ├─/sys/fs/cgroup/systemd          cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd
│ │ ├─/sys/fs/cgroup/net_cls,net_prio cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,net_cls,net_prio
│ │ ├─/sys/fs/cgroup/rdma             cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,rdma
│ │ ├─/sys/fs/cgroup/devices          cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,devices
│ │ ├─/sys/fs/cgroup/cpu,cpuacct      cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,cpu,cpuacct
│ │ ├─/sys/fs/cgroup/pids             cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,pids
│ │ ├─/sys/fs/cgroup/perf_event       cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,perf_event
│ │ ├─/sys/fs/cgroup/blkio            cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,blkio
│ │ ├─/sys/fs/cgroup/hugetlb          cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,hugetlb
│ │ ├─/sys/fs/cgroup/memory           cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,memory
│ │ ├─/sys/fs/cgroup/cpuset           cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,cpuset
│ │ └─/sys/fs/cgroup/freezer          cgroup      cgroup      rw,nosuid,nodev,noexec,relatime,freezer
│ ├─/sys/fs/pstore                    pstore      pstore      rw,nosuid,nodev,noexec,relatime
│ ├─/sys/fs/bpf                       bpf         bpf         rw,nosuid,nodev,noexec,relatime,mode=700
│ ├─/sys/kernel/debug                 debugfs     debugfs     rw,relatime
│ │ └─/sys/kernel/debug/tracing       tracefs     tracefs     rw,relatime
│ └─/sys/kernel/config                configfs    configfs    rw,relatime
├─/proc                               proc        proc        rw,nosuid,nodev,noexec,relatime
│ └─/proc/sys/fs/binfmt_misc          systemd-1   autofs      rw,relatime,fd=37,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=17591
│   └─/proc/sys/fs/binfmt_misc        binfmt_misc binfmt_misc rw,relatime
├─/dev                                devtmpfs    devtmpfs    rw,nosuid,size=919936k,nr_inodes=229984,mode=755
│ ├─/dev/shm                          tmpfs       tmpfs       rw,nosuid,nodev
│ ├─/dev/pts                          devpts      devpts      rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000
│ ├─/dev/mqueue                       mqueue      mqueue      rw,relatime
│ └─/dev/hugepages                    hugetlbfs   hugetlbfs   rw,relatime,pagesize=2M
├─/run                                tmpfs       tmpfs       rw,nosuid,nodev,mode=755
│ ├─/run/user/0                       tmpfs       tmpfs       rw,nosuid,nodev,relatime,size=187080k,mode=700
│ ├─/run/docker/netns/b53fb333121c    nsfs[net:[4026532277]]
│ │                                               nsfs        rw
│ ├─/run/docker/netns/2c9177ef4ff5    nsfs[net:[4026532343]]
│ │                                               nsfs        rw
│ ├─/run/docker/netns/93d4855ea373    nsfs[net:[4026532406]]
│ │                                               nsfs        rw
│ ├─/run/docker/netns/d86b4fd37e2b    nsfs[net:[4026532590]]
│ │                                               nsfs        rw
│ ├─/run/docker/netns/b500b0f4de4d    nsfs[net:[4026532472]]
│ │                                               nsfs        rw
│ ├─/run/docker/netns/eac34401ea4c    nsfs[net:[4026532534]]
│ │                                               nsfs        rw
│ └─/run/docker/netns/667ed259f271    nsfs[net:[4026532722]]
│                                                 nsfs        rw
```

## Resources

- [你管这破玩意叫文件系统](https://mp.weixin.qq.com/s/bYUGs-KBBzPafvZ7EbZJ1Q)

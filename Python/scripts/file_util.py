# coding=utf-8

import os
import random
import re
import shutil
import string
from functools import cmp_to_key

VIDEO_RE = re.compile(r"(.mp4|.avi|.mkv|.rmvb)$", re.IGNORECASE)


def search(filepath, file_list):
    try:
        files = os.listdir(filepath)
    except:
        return

    for item in files:
        item_path = os.path.join(filepath, item)
        if os.path.isdir(item_path):
            search(item_path, file_list)
        else:
            # print(item_path)
            file_list.append(item_path)


def move(src_dir, dest_dir, scan_pattern=VIDEO_RE, random_name_len=8):
    """移动src_dir目录下的scan_pattern文件名到dest_dir.

    Args:
        src_dir (str): 源目录
        dest_dir (str): 目标目录
        scan_pattern (re, optional): 需要移动的文件名正则模式. Defaults to VIDEO_RE.
        random_name_len (int, optional): 随机名长度. Defaults to 8.
    """

    file_list = []
    search(src_dir, file_list)

    for file_fullpath in file_list:
        file_name = os.path.basename(file_fullpath)
        if re.search(scan_pattern, file_name):
            target_name = os.path.join(dest_dir, file_name)
            if os.path.exists(target_name):
                random_name = "".join(random.sample(
                    string.ascii_letters + string.digits, random_name_len)
                )
                os.rename(target_name, os.path.join(dest_dir, random_name))
            shutil.move(file_fullpath, dest_dir)


def _compare_wapper(scan_dir):

    def compare(x, y):
        stat_x = os.stat(scan_dir + "/" + x)
        stat_y = os.stat(scan_dir + "/" + y)
        if stat_x.st_mtime < stat_y.st_mtime:
            return -1
        elif stat_x.st_mtime > stat_y.st_mtime:
            return 1
        else:
            return 0
    return compare


def rename(scan_dir, name_prefix='us-', use_random_name=True, random_name_len=8):
    """文件重命名。name_prefix=None， 则采用随机名。
    Args:
        scan_dir (str): 文件所在目录
        name_prefix (str, optional): 文件前缀. Defaults to 'ABC-'.
        use_random_name (bool, optional): 是否使用随机名.
        random_name_len (int, optional): 随机名长度. Defaults to 8.
    """
    compare = _compare_wapper(scan_dir)

    i = 1

    reg_rename = re.compile(r'(.+)(\.[^.]+)$', re.IGNORECASE)
    myfilelist = os.listdir(scan_dir)
    myfilelist = sorted(myfilelist, key=cmp_to_key(compare))

    for file_name in myfilelist:

        file_name_old_path = os.path.join(scan_dir, file_name)

        if use_random_name:
            new_name = re.sub(reg_rename,
                              name_prefix +
                              "".join(random.sample(
                                  string.ascii_letters + string.digits, random_name_len)
                              ) + r'\2',
                              file_name
                              )
        else:
            new_name = re.sub(reg_rename, name_prefix +
                              ("%03d" % i) + r'\2', file_name)

        file_name_new_path = os.path.join(scan_dir, new_name)
        # print(file_name_new_path)
        os.rename(file_name_old_path, file_name_new_path)
        i = i + 1


if __name__ == "__main__":
    move(r"F:\src_dir", r"F:\dest_dir")
    rename(r"F:\dest_dir", name_prefix='us-', use_random_name=True)

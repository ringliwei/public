# coding=utf-8

import os
import re
import shutil
import random
import string
from functools import cmp_to_key


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
            print(item_path)
            file_list.append(item_path)


def move():
    for file_fullpath in file_list:
        file_name = os.path.basename(file_fullpath)
        if re.search(scan_pattern, file_name):
            target_name = os.path.join(target_dir, file_name)
            if os.path.exists(target_name):
                random_name = "".join(random.sample(string.ascii_letters + string.digits, 8))
                os.rename(target_name, os.path.join(target_dir, random_name))
            shutil.move(file_fullpath, target_dir)


def compare(x, y):
    stat_x = os.stat(scan_dir + "/" + x)
    stat_y = os.stat(scan_dir + "/" + y)
    if stat_x.st_mtime < stat_y.st_mtime:
        return -1
    elif stat_x.st_mtime > stat_y.st_mtime:
        return 1
    else:
        return 0


def rename():
    i = 1
    name_prefix = 'ABC-'
    reg_rename = re.compile(r'(.+)(.mp4|.avi|.mkv)$', re.IGNORECASE)
    myfilelist = os.listdir(scan_dir)
    myfilelist = sorted(myfilelist, key=cmp_to_key(compare))
    for file_name in myfilelist:

        file_name_old_path = os.path.join(scan_dir, file_name)
        new_name = re.sub(reg_rename, name_prefix +
                          ("%03d" % i) + r'\2', file_name)
        # new_name = "".join(random.sample(string.ascii_letters + string.digits, 8))
        file_name_new_path = os.path.join(scan_dir, new_name)
        print(file_name_new_path)
        os.rename(file_name_old_path, file_name_new_path)
        i = i + 1


scan_dir = r'G:\dir_to_scan'
target_dir = r'G:\dir_to_save'

scan_pattern = re.compile(r"(.mp4|.avi|.mkv)$", re.IGNORECASE)

file_list = []

if __name__ == "__main__":
    pass

# coding=utf-8

import os
import re
import shutil


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



scan_dir = r'G:\dir_to_scan'
target_dir = r'G:\dir_to_save'

scan_pattern = re.compile(r"(.mp4|.avi|.xml|.txt)$")

file_list = []
search(scan_dir, file_list)


for file_fullpath in file_list:
    file_name = os.path.basename(file_fullpath)
    if re.search(scan_pattern, file_name):
        shutil.move(file_fullpath, target_dir)

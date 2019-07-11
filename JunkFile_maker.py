#! usr/bin/python
# -*- coding:utf-8 -*-

# sys.argv[0]   脚本文件路径
# os.path.realpath()    返回绝对路径；参数为空，则返回当前目录的绝对路径
# os.path.split()   分割路径和文件名
# json.load 读json文件内容，json.jump 写json文件内容
# json.loads json字符串转字典，json.jumps 字典转json字符串
# random.sample()   从指定的序列中随机获取指定长度的片段
# string.ascii_letters  大小写的英文字母字符串
# string.digits     数字0-9的字符串

import os
import json
import random
import shutil
import string
import sys
import datetime

# 设置默认编码格式
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 文件类型
fileTypes = ('.png', '.jpg', '.txt', '.json', '.plist')

# 文件数范围
fileNumMin = 10
fileNumMax = 15

# 文件夹数范围
folderNumMin = 5
folderNumMax = 8

# 文件夹级数
folderLevel = 5

# 确保命名唯一性
fileNames = set()
folderNames = set()

# 脚本所在路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

# 垃圾资源存放文件夹
junkFiles_path = os.path.join(script_path, 'JunkFiles')

# 获取单词库，用来命名
with open(os.path.join(script_path, 'word_list.json'), 'r') as fileObj:
    word_names = json.load(fileObj)


# 获取一个随机名字
def get_one_name():
    global word_names
    file_name = random.choice(word_names)
    return file_name


# 获取一个随机类型
def get_type():
    global fileTypes
    type_name = random.choice(fileTypes)
    return type_name


# -------------------------- 创建垃圾文件内容 -------------------------------
def get_junk_data(f_type=''):
    if f_type == '.png':
        text = str(random.randint(1, 1024)) * random.randint(1024, 10240)
        png_text = text + '0000000049454e44ae426082'.decode('hex')
        return png_text
    elif f_type == '.json':
        return get_json_text()
    elif f_type == '.plist':
        return get_plist_text()
    else:
        text = ''.join(random.sample(string.ascii_letters + string.digits, 62))
        text = text * random.randint(256, 512)
        return text


def get_json_text():
    json_text = '['
    for i in range(random.randint(100, 500)):
        text = '{\"id\": %d, \"%s\": \"%s\", \"%s\": \"%s\", \"%s\": \"%s\", \"jsontime\": \"%s\"},\n'\
               % (random.randint(1000, 10000), get_one_name(), get_one_name(), get_one_name(), get_one_name(),
                  get_one_name(), get_one_name(), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        json_text = json_text + text
    # 去掉最后一个逗号
    json_text = json_text[:-2] + ']'
    return json_text


def get_plist_text():
    # plist文件标准头部
    plist_text = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
'''
    # 添加随机内容
    # 字符串
    for i in range(random.randint(5, 10)):
        plist_text = plist_text + '<key>%s</key>\n<string>%s</string>\n' % (get_one_name(), get_one_name())

    # 数组
    for i in range(0, random.randint(2, 5)):
        plist_text = plist_text + '<key>%s</key>\n<array>\n' % get_one_name()
        for j in range(2, random.randint(3, 5)):
            plist_text = plist_text + '<string>%s</string>\n' % get_one_name()
        plist_text = plist_text + '</array>\n'

    # 字典
    for i in range(0, random.randint(1, 4)):
        plist_text = plist_text + '<key>%s</key>\n<dict>\n' % get_one_name()
        for j in range(1, random.randint(2, 5)):
            plist_text = plist_text + '<key>%s</key>\n<string>%s</string>\n' % (get_one_name(), get_one_name())
        plist_text = plist_text + '</dict>\n'

    # plist文件结尾
    plist_text = plist_text + '</dict>\n</plist>'
    return plist_text

# -------------------------------------------------------------------------


# 创建单个垃圾文件
def get_one_file(file_path, f_type=''):
    with open(file_path, 'w') as file_Obj:
        file_Obj.write(get_junk_data(f_type))


# 添加单个文件夹的垃圾文件
def add_file_to_folder(folder_path):
    global fileNames
    fileNames.clear()
    # 开始添加文件
    for i in range(random.randint(fileNumMin, fileNumMax)):
        # 获取一个不重复的名字
        file_name = get_one_name()
        while file_name in fileNames:
            file_name = get_one_name()
        fileNames.add(file_name)
        f_type = get_type()
        file_name = file_name + f_type
        print '创建文件：' + file_name
        get_one_file(os.path.join(folder_path, file_name), f_type)


# 创建多级文件夹目录
def add_folders_level(parent_path, level=0):
    global folderLevel, folderNumMin, folderNumMax, folderNames
    if level >= 0:
        for i in range(random.randint(folderNumMin, folderNumMax)):
            folder_name = get_one_name()
            while folder_name in folderNames:
                folder_name = get_one_name()
            folderNames.add(folder_name)
            # print '创建路径：' + os.path.join(parent_path, folder_name)
            os.mkdir(os.path.join(parent_path, folder_name))
            # 回溯 创建分级目录
            add_folders_level(os.path.join(parent_path, folder_name), level - random.randint(1, 4))
    else:
        return 0


# 开始制造垃圾文件
if __name__ == '__main__':
    # 创建垃圾资源文件夹
    if os.path.exists(junkFiles_path):
        shutil.rmtree(junkFiles_path)
    os.mkdir(junkFiles_path)

    # 创建多级文件夹
    add_folders_level(junkFiles_path, folderLevel)

    # 添加垃圾资源文件
    for parent, folders, files in os.walk(junkFiles_path):
        for folder in folders:
            if os.path.isdir(os.path.join(parent, folder)):
                print '添加路径：' + os.path.join(parent, folder)
                add_file_to_folder(os.path.join(parent, folder))

    print '------ success!------'

    # get_json_text()

#! usr/bin/python
# -*- coding:utf-8 -*-

'''

'''

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
import base64

# 设置默认编码格式
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 文件类型
fileTypes = ('.png', '.jpg', '.txt', '.json')

# 文件数范围
fileNumMin = 10
fileNumMax = 20

# 文件夹数范围
folderNumMin = 3
folderNumMax = 5

# 文件夹级数
folderLevel = 5

# 确保命名唯一性
fileNames = set()
folderNames = set()

# 脚本所在路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

# 垃圾资源存放文件夹
junkFiles_path = os.path.join(script_path, 'junkFiles')

# 获取单词库，用来命名
with open(os.path.join(script_path, 'word_list.json'), 'r') as fileObjc:
    word_names = json.load(fileObjc)
    fileObjc.close()


# 获取一个随机名字
def get_one_name():
    global word_names
    fileName = random.choice(word_names)
    return fileName


# 获取一个随机类型
def get_type():
    global fileTypes
    typeName = random.choice(fileTypes)
    return typeName


# 创建垃圾文件内容
def get_junkData():
    ranStr = ''.join(random.sample(string.ascii_letters + string.digits, 62))
    dataStr = ranStr * random.randint(256, 512)
    return base64.b64encode(dataStr.encode())


# 创建单个垃圾文件
def get_one_file(file_path):
    with open(file_path, 'w') as fileObjc:
        fileObjc.write(get_junkData())
        fileObjc.close()


# 添加单个文件夹的垃圾文件
def add_file_to_folder(folder_path):
    global fileNames
    fileNames.clear()
    print '创建路径：' + folder_path
    # 开始添加文件
    for i in range(random.randint(fileNumMin, fileNumMax)):
        # 获取一个不重复的名字
        fileName = get_one_name()
        while fileName in fileNames:
            fileName = get_one_name()
        fileNames.add(fileName)
        fileName = fileName + get_type()
        print '创建文件：' + fileName
        get_one_file(os.path.join(folder_path, fileName))


# 创建多级文件夹目录
def add_folders_level(parent_path, level=0):
    global folderLevel, folderNumMin, folderNumMax, folderNames
    if level >= 0:
        for i in range(random.randint(folderNumMin, folderNumMax)):
            folderName = get_one_name()
            while folderName in folderNames:
                folderName = get_one_name()
            folderNames.add(folderName)
            os.mkdir(os.path.join(parent_path, folderName))
            # 回溯 创建分级目录
            add_folders_level(os.path.join(parent_path, folderName), level - random.randint(1, 4))
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
        add_file_to_folder(os.path.join(parent))

    print '------ success!------'





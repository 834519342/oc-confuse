#!usr/bin/python
# -*- coding:utf-8 -*-

'''

'''

#

import os
import json
import sys
import random
import string
import shutil
import argparse


# 不处理白名单
class_ignore = ('ViewController', 'AppDelegate')

# 设置默认编码格式
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 当前脚本路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

# 资源输出路径
define_header_path = os.path.join(script_path, 'define_header')

# 保证唯一性
classNames = set()
defineNames = set()

# 获取单词库
with open(os.path.join(script_path, 'word_list.json'), 'r') as fileObjc:
    word_names = json.load(fileObjc)
    fileObjc.close()


# 获取一个随机名
def get_one_name():
    global word_names
    return random.choice(word_names) + ''.join(random.sample(string.ascii_letters, 1))

# ------------------------ 混淆类名 -----------------------------
# 添加宏到.h文件
def add_define(header_path, classNameList):
    global defineNames
    with open(header_path, 'w') as fileObjc:
        for className in classNameList:
            # 判断唯一性
            defineName = get_one_name()
            while defineName in defineNames:
                defineName = get_one_name()
            defineNames.add(defineName)

            fileObjc.write('#define ' + className + ' ' + defineName + '\n')
        fileObjc.close()


# 扫描指定目录的类名
def scan_folder(parent_path):
    global classNames
    if not os.path.exists(parent_path):
        print '目录不存在'
        exit(0)

    classNames.clear()

    # 遍历目录
    for parent, folders, files in os.walk(parent_path):
        # 筛选.h文件
        for fileName in files:
            index = fileName.rfind('.h')
            if index != -1:
                fileName = fileName[:index]
                if not fileName in classNames and not fileName in class_ignore:
                    classNames.add(fileName)


# ------------------------ 执行 --------------------------------
# 命令行解析
def parse_args():
    parse = argparse.ArgumentParser(description='类名混淆宏')
    parse.add_argument('-path', dest='path', type=str, required=True, help='扫描目录')
    args = parse.parse_args()
    return args


if __name__ == '__main__':

    # 创建一个新目录
    if os.path.exists(define_header_path):
        shutil.rmtree(define_header_path)
    os.mkdir(define_header_path)
    # 获取参数
    args = parse_args()
    # 扫描需要处理的类名
    scan_folder(args.path)
    # 添加宏命令
    add_define(os.path.join(define_header_path, get_one_name() + '.h'), classNames)

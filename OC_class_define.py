#!usr/bin/python
# -*- coding:utf-8 -*-

'''

'''

# 正则表达式
# () 取值
# \s+ >=1个的空格
# \w+ >=1个的字母数字下划线
# \s* 贪婪模式，最大长度的匹配
# \s*? 非贪婪模式，取最小的长度，最少0个
# \(.+?\) 匹配以(开头,以)结尾的字符串

import os
import json
import sys
import random
import string
import shutil
import argparse
import re

# 类名白名单
class_ignore = ('AppDelegate', 'main')

# 方法白名单
func_ignore = ('viewDidLoad')


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
funcNames = set()
defineNames = set()

# 正则表达式
classPattern = re.compile('@interface\s+(\w+)\s+:\s+\w+')
funcPattern = re.compile('\s*-\s*\(.+?\)\s*(\w+)')


# 获取单词库
with open(os.path.join(script_path, 'word_list.json'), 'r') as fileObjc:
    word_names = json.load(fileObjc)
    fileObjc.close()


# 获取一个随机名
def get_one_name():
    global word_names
    return ''.join(random.sample(string.ascii_uppercase, 1)) + random.choice(word_names)


# 添加宏到.h文件
def add_define_class(header_path, nameList):
    global defineNames
    defineNames.clear()

    with open(header_path, 'a+') as fileObjc:
        for className in nameList:
            # 判断唯一性
            defineName = get_one_name()
            while defineName in defineNames:
                defineName = get_one_name()
            defineNames.add(defineName)

            fileObjc.write('#define ' + className + ' ' + defineName + '\n')
        fileObjc.close()


# ------------------------ 扫描类名 -----------------------------
# 扫描指定目录的类名
def scan_folder_class(parent_path):
    global classNames, class_ignore, classPattern
    classNames.clear()

    if not os.path.isdir(parent_path):
        print '目录不存在'
        exit(0)

    # 遍历目录
    for parent, folders, files in os.walk(parent_path):
        # 筛选.h文件
        for fileName in files:
            (name, ftype) = os.path.splitext(fileName)
            if ftype == '.h':
                with open(os.path.join(parent, fileName), 'r') as fileObjc:
                    # 类名表达式匹配
                    classNameList = classPattern.findall(fileObjc.read())
                    fileObjc.close()
                    for className in classNameList:
                        if not className in classNames and not className in class_ignore:
                            classNames.add(className)


# ----------------------- 扫描方法名 -----------------------------
# 扫描指定目录的方法
def scan_folder_func(parent_path):
    global funcNames, class_ignore, funcPattern, func_ignore
    funcNames.clear()

    if not os.path.isdir(parent_path):
        print '目录不存在'
        exit(0)

    # 遍历目录
    for parent, folders, files in os.walk(parent_path):
        # 筛选.h和.m和.mm文件
        for fileName in files:
            # 跳过白名单
            (name, filetype) = os.path.splitext(fileName)
            if name in class_ignore:
                continue

            if filetype == '.h' or filetype == '.m' or filetype == '.mm':
                print fileName
                with open(os.path.join(parent, fileName), 'r') as fileObjc:
                    # 方法名表达式匹配
                    funcNameList = funcPattern.findall(fileObjc.read())
                    fileObjc.close()
                    for funcName in funcNameList:
                        if not funcName in funcNames and not funcName in func_ignore:
                            funcNames.add(funcName)


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
    # 创建一个头文件名字
    headerName = get_one_name() + '.h'

    # 扫描需要处理的类名
    scan_folder_class(args.path)
    # 添加宏混淆
    add_define_class(os.path.join(define_header_path, headerName), classNames)

    # 扫描需要处理的方法名
    scan_folder_func(args.path)
    print funcNames
    # 添加宏混淆
    add_define_class(os.path.join(define_header_path, headerName), funcNames)
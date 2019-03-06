#!usr/bin/python
# -*- coding:utf-8 -*-

'''
Pattern 英 ['pæt(ə)n] n. 模式；图案；样品
variable 英 ['veərɪəb(ə)l] n. [数] 变量；可变物，可变因素
'''

# 正则表达式
# () 取值
# \s+ >=1个的空格
# \w+ >=1个的字母数字下划线
# \s* 贪婪模式，最大长度的匹配
# \s*? 非贪婪模式，取最小的长度，最少0个
# \(.+?\),\(.*?\) 匹配以(开头,以)结尾的字符串

# findall(string[, pos[, endpos]])  找到所有匹配的子串，返回一个列表

import os
import json
import sys
import random
import string
import shutil
import argparse
import re

# ----------------------------------- 系统白名单 -------------------------------------
# # 文件白名单
system_file = ('main', 'AppDelegate')
# 类名白名单
system_class = ('NS', )
# 属性名白名单
system_variable = ('window', 'price', 'string', 'self', 'path', 'type', 'size', 'height', 'width', 'content')
# 方法名白名单
system_func = ('main', 'application', 'applicationWillResignActive', 'applicationDidEnterBackground',
               'applicationWillEnterForeground', 'applicationDidBecomeActive', 'applicationWillTerminate', 'view',
               'init', 'viewDidLoad', 'viewWillAppear', 'viewWillDisappear', 'didReceiveMemoryWarning',
               'viewWillLayoutSubviews', 'dealloc', 'valueForKey', 'setValue', 'requestDidFinish',
               'safariViewController', 'safariViewControllerDidFinish', 'tableView', 'numberOfSectionsInTableView',
               'paymentQueue', 'productsRequest', 'request', 'initWithNibName', 'mailComposeController', 'initWithFrame'
               , 'content')

# ----------------------------------- 官包SDK ---------------------------------------
# 文件夹白名单
# path_ignore = ('Masonry', )
# # 文件白名单
# file_ignore = ('MBProgressHUD', )
# # 类名白名单
# class_ignore = ()
# # 属性名白名单
# variable_ignore = ('type', 'productId', 'price', 'roleID', 'roleName', 'serverID', 'serverName', 'productName',
#                    'productDesc', 'extension', 'orderID', 'serverId', 'roleId', )
# # 方法名白名单
# func_ignore = ('initWithX', 'completedTransactionsFinished', 'currentSDKVersion')

# -------------------------------- V8SDK ------------------------------------
# 文件夹白名单
path_ignore = ()
# 文件白名单
file_ignore = ()
# 类名白名单
class_ignore = ()
# 属性名白名单
variable_ignore = ('name', 'error', 'title', 'viewController', 'url', 'productId', 'price', 'roleID', 'roleName',
                   'serverID', 'serverName', 'productName', 'productDesc', 'extension', 'orderID', 'serverId', 'roleId',
                   'resultCount', )
# 方法名白名单
func_ignore = ('initWithResult', 'initWithDict', 'initWithDictionary', 'title', 'valueForUndefinedKey', 'GetView',
               'viewController', 'url', 'GetViewController', )

# -------------------------------- 官包SDK + V8SDK ---------------------------
# 文件夹白名单
# path_ignore = ('Masonry', )
# # 文件白名单
# file_ignore = ('MBProgressHUD', )
# # 类名白名单
# class_ignore = ()
# # 属性名白名单
# variable_ignore = ('name', 'error', 'title', 'viewController', 'url', 'resultCount', 'type')
# # 方法名白名单
# func_ignore = ('initWithResult', 'initWithDict', 'initWithDictionary', 'title', 'valueForUndefinedKey', 'GetView',
#                'viewController', 'url', 'GetViewController', 'initWithX', 'completedTransactionsFinished',
#                'currentSDKVersion')



# 设置默认编码格式
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 当前脚本路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

# 资源输出路径
define_header_path = os.path.join(script_path, 'OC_define')

# 保证唯一性
classNames = set()
funcNames = set()
variableNames = set()
names = set()
defineNames = set()


# 正则表达式
classPattern = re.compile('@interface\s+(\w+)\s+:\s+\w+')

funcPattern = re.compile('\s*-\s*\(.+?\)\s*(\w+)')
funcPattern1 = re.compile('\s*(\w+):\(.+?\)\s*\w+')

variablePattern = re.compile('@property\s*\(.*?\)\s*\w+\s*\*?\s*(\w+?);')
variablePattern1 = re.compile('\s*\w+\s*\*\s*(\w+);')

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


# ------------------------ 判断白名单 ---------------------------
# 判断文件夹路径
def is_path_ignore(parent_path=''):
    global path_ignore
    if len(parent_path):
        index = parent_path.rfind(os.path.sep)
        if parent_path[index+1:] in path_ignore:
            print '忽略的目录：' + parent_path[index+1:]
            return True
    return False


# 判断文件名
def is_file_ignore(file_name=''):
    global file_ignore, system_file
    if file_name in file_ignore or file_name in system_file:
        print '忽略的文件：' + file_name
        return True
    return False


# 判断类名
def is_class_ignore(class_name=''):
    global class_ignore, system_class, classNames
    if class_name in class_ignore or class_name in system_class or class_name in classNames:
        return True
    return False


# 判断属性名
def is_variable_ignore(variable_name=''):
    global variable_ignore, system_variable, variableNames
    if variable_name in variable_ignore or variable_name in system_variable or variable_name in variableNames:
        return True
    return False


# 判断方法名
def is_func_ignore(func_name=''):
    global func_ignore, system_func, funcNames
    if func_name in func_ignore or func_name in system_func or func_name in funcNames:
        return True
    return False


# ------------------------ 扫描类名 -----------------------------
# 扫描指定目录的类名
def scan_folder_class(parent_path):
    global classNames, class_ignore, system_class, classPattern
    classNames.clear()

    if not os.path.isdir(parent_path):
        print '目录不存在'
        exit(0)

    # 遍历目录
    for parent, folders, files in os.walk(parent_path):
        if is_path_ignore(parent):
            continue
        # 筛选.h文件
        for fileName in files:
            (name, ftype) = os.path.splitext(fileName)
            # 文件白名单
            if is_file_ignore(name):
                continue

            if ftype == '.h':
                with open(os.path.join(parent, fileName), 'r') as fileObjc:
                    # 类名表达式匹配
                    classNameList = classPattern.findall(fileObjc.read())
                    fileObjc.close()
                    for className in classNameList:
                        if not is_class_ignore(className):
                            print '类名：' + className
                            classNames.add(className)


# ------------------------ 扫描属性对象参数 -------------------------
def scan_folder_variable(parent_path):
    global variableNames, variablePattern, variable_ignore, system_variable
    variableNames.clear()

    if not os.path.isdir(parent_path):
        print '目录不存在'
        exit(0)

    # 遍历目录
    for parent, folders, files in os.walk(parent_path):
        if is_path_ignore(parent):
            continue
        # 筛选指定类型的文件
        for fileName in files:
            (name, ftype) = os.path.splitext(fileName)
            # 文件白名单
            if is_file_ignore(name):
                continue
            if ftype == '.h' or ftype == '.m' or ftype == '.mm':
                with open(os.path.join(parent, fileName), 'r') as fileObjc:
                    # 属性名表达式匹配
                    lines = fileObjc.readlines()
                    for line_text in lines:
                        variableNameList = variablePattern.findall(line_text)
                        if len(variableNameList) > 0:
                            for variableName in variableNameList:
                                if not is_variable_ignore(variableName):
                                    print '属性名：' + variableName
                                    variableNames.add(variableName)
                        else:
                            variableNameList = variablePattern1.findall(line_text)
                            if len(variableNameList) > 0:
                                for variableName in variableNameList:
                                    if not is_variable_ignore(variableName):
                                        print '属性名：' + variableName
                                        variableNames.add(variableName)


# ----------------------- 扫描方法名 -----------------------------
# 扫描指定目录的方法
def scan_folder_func(parent_path):
    global funcNames, class_ignore, funcPattern, funcPattern1, func_ignore, system_func
    funcNames.clear()

    if not os.path.isdir(parent_path):
        print '目录不存在'
        exit(0)

    # 遍历目录
    for parent, folders, files in os.walk(parent_path):
        if is_path_ignore(parent):
            continue
        # 筛选.h和.m和.mm文件
        for fileName in files:
            # 跳过白名单
            (name, ftype) = os.path.splitext(fileName)
            # 文件白名单
            if is_file_ignore(name):
                continue

            if ftype == '.h' or ftype == '.m' or ftype == '.mm':
                with open(os.path.join(parent, fileName), 'r') as fileObjc:
                    # 方法名表达式匹配
                    funcNameList = funcPattern.findall(fileObjc.read())
                    for funcName in funcNameList:
                        if not is_func_ignore(funcName):
                            print '方法名：' + funcName
                            funcNames.add(funcName)
                    fileObjc.close()

                # with open(os.path.join(parent, fileName), 'r') as fileObjc:
                #     # 方法名表达式匹配
                #     funcNameList = funcPattern1.findall(fileObjc.read())
                #     for funcName in funcNameList:
                #         if not funcName in funcNames and not funcName in func_ignore:
                #             print '方法名：' + funcName
                #             funcNames.add(funcName)
                #     fileObjc.close()


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
    # headerName = 'Pcarrot.h'

    # 扫描需要处理的类名
    scan_folder_class(args.path)
    for name in classNames:
        if not name in names:
            names.add(name)

    # # 扫描需要处理的属性名
    scan_folder_variable(args.path)
    for name in variableNames:
        if not name in names:
            names.add(name)

    # 扫描需要处理的方法名
    scan_folder_func(args.path)
    for name in funcNames:
        if not name in names:
            names.add(name)

    # 添加宏混淆
    add_define_class(os.path.join(define_header_path, headerName), names)

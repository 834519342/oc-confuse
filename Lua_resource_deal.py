#! usr/bin/python
# -*- coding:utf-8 -*-

'''
resource 英 [rɪ'sɔːs; rɪ'zɔːs] n. 资源，财力；办法；智谋
exclude 英 [ɪk'skluːd; ek-] vt. 排除；排斥；拒绝接纳；逐出
match 英 [mætʃ] n. 比赛，竞赛；匹配；对手；火柴
rule 英 [ruːl] n. 统治；规则
relative 英 ['relətɪv] adj. 相对的；有关系的；成比例的
random 英 ['rændəm] adj. [数] 随机的；任意的；胡乱的
sample 英 ['sɑːmp(ə)l] vt. 取样；尝试；抽样检查
letter 英 ['letə] n. 信；字母，文字；证书；文学，学问；字面意义
filter 英 ['fɪltə] n. 滤波器；[化工] 过滤器；筛选；滤光器
split 英 [splɪt] vt. 分离；使分离；劈开；离开；分解
parse 英 [pɑːz] vt. 解析；从语法上分析
argument 英 ['ɑːgjʊm(ə)nt] n. 论证；论据；争吵；内容提要
description 英 [dɪ'skrɪpʃ(ə)n] n. 描述，描写；类型；说明书
exist 英 [ɪg'zɪst; eg-] vi. 存在；生存；生活；继续存在
'''

import os
import json
import random
import string
import argparse  # 命令行解析模块
import shutil
import time
import sys

import JunkFile_maker  # 使用垃圾生成模块

# 编码格式，默认值：ascii，设置默认值为：utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 脚本所在路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
# 资源路径
resource_path = ''
# 目标路径
target_path = os.path.join(script_path, 'Lua_resource')

# 确保函数名的唯一
func_names_set = set()

# 获取单词列表，用以随机名称
with open(os.path.join(script_path, './word_list.json'), 'r') as file_Obj:
    word_name_list = json.load(file_Obj)


# 获取一个随机名称
def get_one_name():
    global word_name_list
    return random.choice(word_name_list)


# ----------------------- 创建lua垃圾代码，创建垃圾图片数据 -------------------------
# 获取lua垃圾方法
def get_lua_func_text():
    global func_names_set
    new_func_name = get_one_name()
    while new_func_name in func_names_set:
        new_func_name = get_one_name()
    func_names_set.add(new_func_name)

    argv_name = get_one_name() + get_one_name()
    text = [
        '\nlocal function ' + new_func_name + '()\n',
        '\tlocal %s = %d + %d\n' % (argv_name, random.randint(1, 1000), random.randint(1, 1000)),
        '\treturn %s\n' % argv_name,
        'end\n'
    ]
    return string.join(text)


# 获取png内容
def get_png_text():
    text = str(random.randint(1, 1024)) * random.randint(1024, 10240)
    text = text + '0000000049454e44ae426082'.decode('hex')
    return text


# ---------------------- 遍历指定目录，添加lua垃圾文件或png垃圾路片 ---------------------
# 添加单个垃圾文件(lua文件和png文件)
def add_single_file(file_path):
    global target_path, func_names_set
    # 只缓存单个文件的方法名
    func_names_set.clear()

    print 'add file：' + file_path.replace(target_path, '')
    # os.path.splitext(path) 分割路径，返回路径名和文件扩展名的元组
    (path_name, file_type) = os.path.splitext(file_path)
    if file_type == '.lua':
        with open(file_path, 'w') as file_Obj:
            func_num = random.randint(10, 15)
            for j in range(0, func_num):
                file_Obj.write(get_lua_func_text())
    else:
        # if file_type == '.png':
        #     with open(file_path, 'wb') as file_Obj:
        #         file_Obj.write(get_png_text())
        with open(file_path, 'w') as file_Obj:
            file_Obj.write(JunkFile_maker.get_junk_data(file_type))


def add_file_to(parent_folder, level, min_file_num=0):
    global target_path
    
    create_folder_list = []
    for parent, folders, files in os.walk(parent_folder):
        target_file_type = ''
        # 获取相对路径
        relative_path = parent.replace(target_path, '')

        # 判断是否为res路径，find()：查找字符串，找到返回开始的索引值，找不到返回-1
        # os.path.sep 系统的路径分隔符 /
        if relative_path.find(os.path.sep + 'res') != -1:
            # target_file_type = '.png'  # .png
            target_file_type = JunkFile_maker.get_type()
        elif relative_path.find(os.path.sep + 'res') == -1:
            target_file_type = '.lua'  # .lua

        # 创建文件数量
        new_file_num = random.randint(len(files) / 2, len(files)) + min_file_num
        for i in range(0, new_file_num):
            file_path = os.path.join(parent, get_one_name() + target_file_type)
            add_single_file(file_path)
            # 延迟操作,防止操作太快出错
            time.sleep(0.001)

        # 防止创建太多层的文件夹
        if level > 2:
            continue
        # 创建文件夹数量
        new_fold_num = random.randint(len(folders) / 2, len(folders))
        for i in range(0, new_fold_num):
            target_folder = os.path.join(parent, get_one_name())
            # 为了不阻断os.walk,延后创建文件夹
            create_folder_list.append(target_folder)

    for folder_path in create_folder_list:
        try:
            print 'create folder：' + folder_path.replace(target_path, '')
            os.mkdir(folder_path)
            # 回溯法创建新的文件夹
            add_file_to(folder_path, level + 1, random.randint(2, 5))
        except Exception as e:
            print e


# -------------------------- 遍历指定的目录，修改文件资源的md5值 --------------------------
# 改md5值
def change_file_md5(file_path):
    _, file_type = os.path.splitext(file_path)
    with open(file_path, 'ab') as file_Obj:
        if file_type == '.png':
            # sample(seq, n) 从序列seq中选择n个随机且独立的元素
            # ascii_letters 是生成所有字母，从a-z和A-Z
            text = ''.join(random.sample(string.ascii_letters, 11))
        elif file_type == '.jpg':
            text = ''.join(random.sample(string.ascii_letters, 20))
        elif file_type == '.lua':
            text = '\n--#*' + ''.join(random.sample(string.ascii_letters, 10))
        else:
            text = ' ' * random.randint(1, 100)
        file_Obj.write(text)


# 遍历文件路径，改变md5值
def search_folder_md5(search_path):
    # 文件类型筛选条件
    type_filter = set(['.png', '.jpg', '.lua', '.json', '.plist', '.fnt'])
    for parent, folders, files in os.walk(search_path):
        for file1 in files:
            full_path = os.path.join(parent, file1)
            _, file_type = os.path.splitext(full_path)
            if file_type in type_filter:
                change_file_md5(full_path)


# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='资源变异工具')
    parser.add_argument('-path', dest='res_dir', type=str, required=True, help='资源目录')
    parser.add_argument('-out_path', dest='out_path', type=str, required=False, default=target_path, help='资源导出目录')
    args = parser.parse_args()
    return args


# --------------------- 代码执行逻辑 ------------------------
def main():
    global resource_path, target_path
    # 获取命令行参数
    app_args = parse_args()
    resource_path = app_args.res_dir
    target_path = app_args.out_path

    # 判断路径是否存在
    if not os.path.exists(resource_path):
        print 'res path not exists:' + resource_path
        exit(0)
    if target_path != resource_path:
        # 删除旧目录
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        # 复制到新目录
        shutil.copytree(resource_path, target_path)

    # 添加垃圾文件
    add_file_to(target_path, 0)

    print '\n\nstart modify file md5'
    # 修改MD5值
    search_folder_md5(target_path)
    print 'finish!'


if __name__ == '__main__':
    main()

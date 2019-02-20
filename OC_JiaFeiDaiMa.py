#! /usr/bin/python
# -*- coding: UTF-8 -*-

'''

script 英 [skrɪpt] n. 脚本；手迹；书写用的字母
target 英 ['tɑːgɪt] n. 目标，指标；（攻击的）对象；靶子
backup 英 ['bækʌp] vt. 做备份
folder 英 ['fəʊldə] n. 文件夹；折叠机；折叠式印刷品
ignore 英 [ɪg'nɔː] vt. 驳回诉讼；忽视；不理睬
append 英 [ə'pend] vt. 附加；贴上；盖章
deal 英 [diːl] vt. 处理；给予；分配；发牌
parent 英 ['peər(ə)nt] n. 父亲（或母亲）；父母亲；根源
trash 英 [træʃ] n. 垃圾；废物
parser 英 ['pɑːsə] n. [计] 分析程序；语法剖析程式
description 英 [dɪ'skrɪpʃ(ə)n] n. 描述，描写；类型；说明书
required 英 [rɪ'kwaɪəd] adj. 必需的；（美）必修的
replace 英 [rɪ'pleɪs] vt. 取代，代替；替换，更换；归还，偿还；把…放回原处

'''

import os
import json
import random
import shutil
import argparse

import sys
reload(sys)  # Python2.5 初始化后悔删除 sys.setdefaultencoding() 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

# 获取脚本文件所在路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

# 垃圾代码临时存放目录
target_ios_folder = os.path.join(script_path, "./target_ios")
# 源文件备份目录
backup_ios_folder = os.path.join(script_path, "./backup_ios")

# 忽略文件列表
ignore_file_list = ['main.m']
# 忽略文件夹列表
ignore_folder_list = []

# 创建垃圾函数数量范围
create_func_min = 5
create_func_max = 10

# 创建垃圾文件数量范围
create_file_min = 10
create_file_max = 20

# oc代码目录
ios_src_path = ""

# 确保添加的函数不重名
# set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。
funcname_set = set()

# 单词列表，用以随机名称
# 打开json文件
with open(os.path.join(script_path, './word_list.json'), 'r') as fileObj:
    # 解析成json数据
    word_name_list = json.load(fileObj)


# 获取一个随机名称
def getOneName():
    global word_name_list
    # choice() 方法返回一个列表，元组或字符串的随机项。
    return random.choice(word_name_list)

# ------------------ 创建一个垃圾函数的声明与实现的模板 ------------------
# oc代码头文件函数声明
def getOCHeaderFuncText():
    global funcname_set
    funcName = getOneName() + getOneName()
    # 防止出现重复的函数
    while funcName in funcname_set:
        funcName = getOneName() + getOneName()
    funcname_set.add(funcName)

    text = "\n- (void)%s" % funcName
    return text


# oc代码函数实现模板
def getOCFuncText(header_text):
    arg1 = getOneName() + getOneName() + getOneName()
    text = [
        header_text + "\n",
        "{\n"
        "\tNSLog(@\"%s\");\n" % arg1,
        "}\n"
    ]
    # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
    return ''.join(text)


# ------------------ 扫描指定目录，在.h和.m文件中添加垃圾函数 ------------------
# oc代码以@end结尾，在其前面添加text
def appendTextToOCFile(file_path, text):
    with open(file_path, 'r') as fileObj:
        old_text = fileObj.read()
        fileObj.close()
        # Python rfind() 返回字符串最后一次出现的位置(从右向左查询)，如果没有匹配项则返回-1。
        end_mark_index = old_text.rfind("@end")
        if end_mark_index == -1:
            print "\t非法的结尾格式: " + file_path
            return
        # 截取字符串，插入废代码
        new_text = old_text[:end_mark_index]
        new_text = new_text + text + "\n"
        new_text = new_text + old_text[end_mark_index:]

        # 写入文件
        with open(file_path, "w") as fileObj:
            fileObj.write(new_text)
            fileObj.close()


# 处理单个OC文件，添加垃圾函数。确保其对应头文件存在于相同目录，参数传入.m文件的名字和路径
def dealWithOCFile(filename, file_path):
    global funcname_set, create_func_min, create_func_max
    # clear() 方法用于移除集合中的所有元素。
    funcname_set.clear()
    end_index = file_path.rfind(".")
    pre_name = file_path[:end_index]
    header_path = pre_name + ".h"

    if not os.path.exists(header_path):
        print '\t相应头文件不存在：' + file_path
        return

    new_func_num = random.randint(create_func_min, create_file_max)
    print "\t给%s添加%d个方法" % (filename, new_func_num)
    for i in range(new_func_num):
        header_text = getOCHeaderFuncText()
        appendTextToOCFile(header_path, header_text + ";\n")

        funcText = getOCFuncText(header_text)
        appendTextToOCFile(file_path, funcText)


# 扫描parent_folder,添加垃圾函数
def addOCFunctions(parent_folder):
    global ignore_file_list, ignore_folder_list
    # os.walk() 方法是一个简单易用的文件、目录遍历器，可以帮助我们高效的处理文件、目录方面的事情。
    # 返回 当前目录，文件夹list，文件list
    for parent, folders, files in os.walk(parent_folder):
        # print parent, folders, files
        need_ignore = None
        # 跳过指定的文件夹
        for ignore_folder in ignore_folder_list:
            # Python find() 方法检测字符串中是否包含子字符串 str
            if parent.find('/' + ignore_folder) != -1:
                need_ignore = ignore_folder
                break
        if need_ignore:
            print '\t忽略文件夹：' + need_ignore
            continue

        # 跳过指定的文件,只处理OC文件
        for file in files:
            if file.endswith('.m') or file.endswith('.mm'):
                if file in ignore_file_list:
                    continue
                dealWithOCFile(file, os.path.join(parent, file))


# --------------------------- 创建垃圾类文件的代码模板 --------------------------------
# 创建垃圾文件header模板
def getOCHeaderFileText(class_name):
    global funcname_set
    new_func_name = getOneName()
    while new_func_name in funcname_set:
        new_func_name = getOneName()
    funcname_set.add(new_func_name)

    text = [
        "#import <UIKit/UIKit.h>\n",
        "#import <Foundation/Foundation.h>\n\n",
        "@interface %s : NSObject {\n" % class_name,
        "\tint %s;\n" % new_func_name,
        "\tfloat %s;\n" % getOneName(),
        "}\n\n@end"
    ]
    return ''.join(text)


# 创建垃圾文件mm模板
def getOCMMFileText(class_name):
    text = [
        "#import \"%s.h\"\n\n" % class_name,
        "@implementation %s\n" % class_name,
        "\n\n@end"
    ]
    return ''.join(text)


# ---------------------- 在指定目录下创建垃圾类文件 -----------------------
# 添加垃圾文件到parent_folder/trash/
def addOCFile(parent_folder):
    global create_file_min, create_file_max
    file_list = []
    target_folder = os.path.join(parent_folder, 'trash')
    # 删除旧的
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    # 创建新的
    os.mkdir(target_folder)
    file_num = random.randint(create_file_min, create_file_max)
    for i in range(file_num):
        file_name = getOneName()
        # 引用每一个创建的类
        file_list.append("#import \"" + file_name + ".h\"")

        print "\t创建OC文件 trash/" + file_name
        # 创建基础的.h文件
        header_text = getOCHeaderFileText(file_name)
        full_path = os.path.join(target_folder, file_name + '.h')
        with open(full_path, 'w') as fileObj:
            fileObj.write(header_text)
            fileObj.close()
        # 创建基础的.m文件
        mm_text = getOCMMFileText(file_name)
        full_path = os.path.join(target_folder, file_name + '.m')
        with open(full_path, 'w') as fileObj:
            fileObj.write(mm_text)
            fileObj.close()
    # 创建引用所有垃圾类的文件
    all_header_text = '\n'.join(file_list)
    with open(os.path.join(parent_folder, 'Trash.h'), 'w') as fileObj:
        fileObj.write(all_header_text)
        fileObj.close()


# 命令行参数解析
def parse_args():
    parser = argparse.ArgumentParser(description='oc垃圾代码生成工具.')
    parser.add_argument('-oc_folder', dest='oc_folder', type=str, required=True, help='OC代码所在目录')
    parser.add_argument('-replace', dest='replace_ios', required=False, help='直接替换oc源代码', action='store_true')

    args = parser.parse_args()
    return args


# ------------------------------- 脚本执行逻辑 -----------------------------
def main():
    app_args = parse_args()
    global ios_src_path, backup_ios_folder, target_ios_folder
    ios_src_path = app_args.oc_folder
    if not os.path.exists(ios_src_path):
        print 'oc_folder path not exist'
        exit(0)

    print '拷贝OC代码到target_ios'
    if os.path.exists(target_ios_folder):
        shutil.rmtree(target_ios_folder)
    shutil.copytree(ios_src_path, target_ios_folder)

    print '开始创建oc文件到trash目录'
    addOCFile(target_ios_folder)
    print '\n开始添加oc方法'
    addOCFunctions(target_ios_folder)

    # 如果要替换，则先备份
    if app_args.replace_ios:
        print '\n用target_ios替换目录'
        # os.path.abspath(path)	返回绝对路径
        print '\t备份OC代码到' + os.path.abspath(backup_ios_folder)
        if os.path.exists(backup_ios_folder):
            shutil.rmtree(backup_ios_folder)
        shutil.copytree(ios_src_path, backup_ios_folder)

        print '\t开始替换'
        trash_folder = os.path.join(ios_src_path, 'trash')
        if os.path.exists(trash_folder):
            shutil.rmtree(trash_folder)
        os.mkdir(trash_folder)

        for parent, folders, files in os.walk(target_ios_folder):
            for file in files:
                if file.endswith('.h') or file.endswith('.m') or file.endswith('.mm'):
                    full_path = os.path.join(parent, file)
                    target_path = full_path.replace(target_ios_folder, ios_src_path)
                    shutil.copy(full_path, target_path)
        print '替换成功\n需要在Xcode上手动添加trash文件夹'
    else:
        print '垃圾代码生成完成，垃圾代码目录：' + os.path.abspath(target_ios_folder)

    print '\nfinished'


if __name__ == '__main__':
    main()

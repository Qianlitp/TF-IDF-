#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import jieba
from collections import Counter
import os
import math
import re


def multiple_replace(text, adict):
     rx = re.compile('|'.join(map(re.escape, adict)))

     def one_xlat(match):
           return adict[match.group(0)]
     return rx.sub(one_xlat, text)

'''
    清除停用词表中的词
'''
def remove_trash(content):
    content = multiple_replace(content, {'\n': '', '，': '', '。': '', '”': '', '“': '', ' ': '', '、': '', '的': ''
                                         , '是': '', '了': '', '在': '', '\t': '', '\r': '', '？': '', ':': '', '；': ''
                                         , ';': ''})
    return content



'''
    从文件夹中读取文本，并为每个文本分词，然后统计每个词的词频，得到TF值列表
'''
def get_TF_list(path):
    res_list = []
    if not os.path.exists(path):
        exit("目录不存在")
    for each in os.listdir(path):
        TF_list = []
        content = open(os.path.join(path, each)).read()
        content = remove_trash(content)
        res = list(jieba.cut(content, cut_all=True))
        count = Counter(res).most_common()
        for i in count:
            temp = (i[0], i[1] / len(count))
            TF_list.append(temp)
        res_list.append(TF_list)
    return res_list

'''
    返回所给词在文本库中的出现次数
'''
def get_count_files(word, fileList):
    count = 0
    for file in fileList:
        for each in file:
            if word == each[0]:
                count += 1
    return count

'''
    返回所有文本中所有词的TF-IDF值列表
'''
def get_TF_IDF(TF_list, IDF_list):
    res_list = []
    for x in xrange(len(TF_list)):
        temp_list = []
        for y in xrange(len(TF_list[x])):
            temp_list.append(TF_list[x][y][1]*IDF_list[x][y][1])
        res_list.append(temp_list)
    return res_list

'''
    返回TF-IDF值前十的索引列表
'''
def get_top_10(TF_IDF_list):
    res_list = []
    for file in TF_IDF_list:
        temp_list = []
        for i in xrange(10):
            temp_list.append(file.index(max(file)))
            file[file.index(max(file))] = 0
        res_list.append(temp_list)
    return res_list

'''
    返回IDF值的列表
'''
def get_IDF_list(TF_list):
    IDF_all_list = []
    for file in TF_list:
        IDF_list = []
        for each in file:
            temp = (each, math.log(len(TF_list)/(get_count_files(each, TF_list)+1)))
            IDF_list.append(temp)
        IDF_all_list.append(IDF_list)
    return IDF_all_list

def main():
    TF_all_list = get_TF_list("test")
    IDF_all_list = get_IDF_list(TF_all_list)
    TF_IDF_list = get_TF_IDF(TF_all_list, IDF_all_list)

    index_list = get_top_10(TF_IDF_list)
    for x in xrange(len(TF_all_list)):
        print '-----------第 ' + str(x+1) + ' 篇文章的特征词：----------------'
        for y in index_list[x]:
            print TF_all_list[x][y][0], TF_all_list[x][y][1]


if __name__ == "__main__":
    main()

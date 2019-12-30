# -*-coding: utf-8 -*-
# encoding=utf-8
# 根据文法生成first集follow集并生成预测分析表
import copy
import pickle

sentence = []
first = {}
follow = {}
M = {}  # 预测分析表
startSign = '程序'


def init():
    try:
        file = open('wf.txt', 'r', encoding='utf-8')
        sentence = open('sentence.txt', 'w', encoding='utf-8')
        while True:
            text_line = file.readline()
            text_line = text_line.strip()
            if not text_line:
                break
            left = text_line.split('->')[0]
            right = text_line.split('->')[1].split('|')
            for i in right:
                sentence.write('{left}->{right}\r'.format(left=left, right=i))
    finally:
        file.close()
        sentence.close()


def readSentence():  # 读取txt中的句子，并初始化first集和follow集的算法第一步
    try:
        file = open('sentence.txt', 'r', encoding='utf8')
        while True:
            text_line = file.readline()
            text_line = text_line.strip()
            if not text_line:
                break
            sentence.append(text_line)
            left = text_line.split('->')[0]
            right = text_line.split('->')[1]
            first[left] = set()
            follow[left] = set()
        follow[startSign] = {'#'}
    finally:
        file.close()


def createFirst():  # first集算法第二步和第三步
    for i in sentence:
        left = i.split('->')[0]
        right = i.split('->')[1].strip().split(' ')
        if right[0] not in first.keys() or right[0] == 'ε':
            first[left] = first[left] | {right[0]}

    for i in sentence:
        left = i.split('->')[0]
        right = i.split('->')[1].strip().split(' ')
        length = len(right)
        pointer = -1
        while pointer < length - 1:
            pointer += 1
            if right[pointer] in first.keys():
                first[left] = first[left] | (first[right[pointer]] - {'ε'})
            else:
                first[left]=first[left]|{right[pointer]}
                break
            if pointer == length - 1 and 'ε' in first[right[pointer]]:
                first[left].add('ε')
            if 'ε' in first[right[pointer]]:
                continue
            else:
                break


def cycleFirst():  # 循环first算法，直到没有新元素被加入
    createFirst()
    prefirst = copy.deepcopy(first)

    while True:
        createFirst()
        if first == prefirst:
            break
        prefirst = copy.deepcopy(first)


def multiFirst(w):
    length = len(w)
    pointer = -1
    ret = set()
    while pointer < length - 1:
        pointer += 1
        if w[pointer] in first.keys():
            ret = ret | (first[w[pointer]] - {'ε'})
        else:
            ret = ret | {w[pointer]}
            break
        if pointer == length - 1 and 'ε' in first[w[pointer]]:
            ret.add('ε')
        if 'ε' in first[w[pointer]]:
            continue
        else:
            break
    return ret


def createFollow():
    for i in sentence:  # 算法第二步
        left = i.split('->')[0]
        right = i.split('->')[1].strip().split(' ')
        length = len(right)
        pointer = -1
        while pointer < length - 1:
            pointer += 1
            if right[pointer] in first.keys():
                if pointer != length - 1:
                    follow[right[pointer]] = follow[right[pointer]] | (multiFirst(right[pointer + 1:]) - {'ε'})


    for i in sentence:  # 算法第三步
        left = i.split('->')[0]
        right = i.split('->')[1].strip().split(' ')
        length = len(right)
        pointer = -1
        while pointer < length - 1:
            pointer += 1
            if right[pointer] in first.keys():
                if pointer == length - 1:
                    follow[right[pointer]] = follow[right[pointer]] | follow[left]
                elif 'ε' in multiFirst(right[pointer + 1:]):
                    follow[right[pointer]] = follow[right[pointer]] | follow[left]
    # print('follow:',follow)


def cycleFollow():  # 循环follow集算法，直到没有新的元素被加入
    createFollow()
    prefollow = copy.deepcopy(follow)

    while True:
        createFollow()
        if follow == prefollow:
            break
        prefollow = copy.deepcopy(follow)


def createM():
    for i in sentence:  # 步骤2
        left = i.split('->')[0]
        right = i.split('->')[1].strip().split(' ')
        for j in multiFirst(right):
            if left not in M.keys():
                M[left] = {}
            if j != 'ε':
                M[left][j] = right
    for i in sentence:  # 步骤3
        left = i.split('->')[0]
        right = i.split('->')[1].strip().split(' ')
        if 'ε' in multiFirst(right):
            for b in follow[left]:
                if left not in M.keys():
                    M[left] = {}
                if b != 'ε':
                    M[left][b] = right


def print2file():
    print('FIRST集如下')
    for i in first.keys():
        print('FIRST[{A}]={B}'.format(A=i, B=first[i]))
    print('Follow集如下')
    for i in follow.keys():
        print('FOLLOW[{A}]={B}'.format(A=i, B=follow[i]))


def saveM():
    path = 'M.txt'
    file = open(path, 'wb')
    pickle.dump(M, file)


def saveFirst():
    path = 'first.txt'
    file = open(path, 'wb')
    pickle.dump(first, file)


def saveFollow():
    path = 'follow.txt'
    file = open(path, 'wb')
    pickle.dump(follow, file)

def rec():
    for i,j in first.items():
        if 'ε' in j:
            print( i,'is',first[i] &follow[i])


if __name__ == '__main__':
    init()
    readSentence()
    # print(sentence)
    cycleFirst()  # 构建first集
    cycleFollow()


    createM()  # 构造预测分析表
    print2file()  # 打印first集和follow集
    saveM()  # 序列化保存预测分析表对象
    saveFirst()
    saveFollow()
    # print(M['表达式'])
    # print(sentence)
    # print(multiFirst(['表达式']))
    rec()
    # print(first['算术表达式'])
    # print(first['布尔表达式'])

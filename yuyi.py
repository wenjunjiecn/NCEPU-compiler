P = {
    '+': {'+': '>', '*': '<', '↑': '<', 'i': '<', '(': '<', ')': '>', '#': '>'},
    '*': {'+': '>', '*': '>', '↑': '<', 'i': '<', '(': '<', ')': '>', '#': '>'},
    '↑': {'+': '>', '*': '>', '↑': '<', 'i': '<', '(': '<', ')': '>', '#': '>'},
    'i': {'+': '>', '*': '>', '↑': '>', 'i': '', '(': '', ')': '>', '#': '>'},
    '(': {'+': '<', '*': '<', '↑': '<', 'i': '<', '(': '<', ')': '=', '#': ''},
    ')': {'+': '>', '*': '>', '↑': '>', 'i': '', '(': '', ')': '>', '#': '>'},
    '#': {'+': '<', '*': '<', '↑': '<', 'i': '<', '(': '<', ')': '', '#': '='},
}  # 算符优先分析表

instr = ['#', ')', 'i', '*', 'i', '(', '+', 'i', '↑', 'i']  # 输入字符串
analysis = []  # 分析栈


class treenode:  # 语法树结点
    def addplace(self, place):
        self.place = place

    def addchilds(self, childs):
        self.childs = childs

    def addparent(self, parent):
        self.parent = parent


tree = {}  # 用字典模拟树，key为节点名，value是结点的对象

numn = 0


def prior():  # 自下而上的分析方法：算符优先算法
    analysis.append('#')
    k = 0
    print(analysis, '        ', instr[::-1])
    while True:
        a = instr[-1]
        if analysis[k] in P.keys():
            j = k
        else:
            j = k - 1
        while P[analysis[j]][a] == '>':
            while True:
                q = analysis[j]
                if analysis[j - 1] in P.keys():
                    j = j - 1
                else:
                    j = j - 2
                if P[analysis[j]][q] == '<':
                    global numn
                    tmpn = 'N' + str(numn)
                    classify(tmpn, analysis[j + 1:])
                    del analysis[j + 1:]

                    break
            k = j + 1
            tmpn = 'N' + str(numn)
            analysis.append(tmpn)
            numn += 1
            print(analysis, '        ', instr[::-1])
        if P[analysis[j]][a] == '<' or P[analysis[j]][a] == '=':
            if a != '#':
                k = k + 1
                analysis.append(a)
                instr.pop()
                print(analysis, '        ', instr[::-1])
        else:
            return 'error'

        if a == '#':
            break


tmp_num = 0


def newtemp():  # 新建一个临时变量
    global tmp_num
    temp = 'T' + str(tmp_num)
    tmp_num += 1
    return temp


def gen(op, arg1, arg2, result):  # 把四元式写入文件
    tmp = '({op},{arg1},{arg2},{result})\r'.format(op=op, arg1=arg1, arg2=arg2, result=result)
    try:
        file = open('four.txt', 'a')
        file.write(tmp)
    finally:
        file.close()


def initfile():  # 清空四元式输出文件
    try:
        file = open('four.txt', 'r+')
        file.truncate()
    finally:
        file.close()


def classify(tmpn, fac):  # 分类翻译
    if len(fac) == 1 and fac[0] == 'i':
        tree[tmpn] = treenode()
        tree[tmpn].addplace('i')
    elif fac[1] == '+':
        tree[tmpn] = treenode()
        tree[tmpn].addplace(newtemp())
        gen('+', tree[fac[0]].place, tree[fac[2]].place, tree[tmpn].place)
    elif fac[1] == '*':
        tree[tmpn] = treenode()
        tree[tmpn].addplace(newtemp())
        gen('*', tree[fac[0]].place, tree[fac[2]].place, tree[tmpn].place)
    elif fac[1] == '↑':
        tree[tmpn] = treenode()
        tree[tmpn].addplace(newtemp())
        gen('↑', tree[fac[0]].place, tree[fac[2]].place, tree[tmpn].place)
    elif fac[0] == '(' and fac[2] == ')':
        tree[tmpn] = treenode()
        tree[tmpn].addplace(tree[fac[1].place])


if __name__ == '__main__':
    initfile()  # 清空文件
    if prior() != 'error':  # 判断是否符合文法，并输出四元式
        print('true')
    else:
        print('error')

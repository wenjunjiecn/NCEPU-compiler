import pickle

analysis=[]
instr=[]
startSign='E'

def readM():   #导入预测分析表
    file=open('M.txt','rb')
    global M
    M=pickle.load(file)
    file.close()
def readFF():   #导入first集和follow集
    file = open('first.txt', 'rb')
    global first
    first= pickle.load(file)
    file.close()
    file = open('follow.txt', 'rb')
    global follow
    follow= pickle.load(file)
    file.close()


def forecast():
    analysis.append('#')
    analysis.append(startSign)
    instr=['#','i','*','i','+','i']
    a=instr[-1]
    flag=True
    print(analysis, '         ', instr[::-1])
    while(flag):
        X=analysis.pop()
        if X not in first.keys() and X !='#':
            if X ==a:
                instr.pop()
                a=instr[-1]
            else:
                return 'error'
        elif X=='#':
            if X==a:
                flag=False
                return 'true'
            else:
                return 'error'
        elif X in M.keys() and a in M[X].keys():
            if M[X][a]!='ε':
                for i in M[X][a][::-1]:
                    analysis.extend(i)
        else:
            return 'error'
        print(analysis,'         ',instr[::-1])



if __name__ == '__main__':
    readM()
    readFF()
    print(forecast())
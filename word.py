words = {'begin': 1, 'end': 2, 'integer': 3, 'char': 4, 'bool': 5, 'real': 6, 'input': 7, 'output': 8, 'program': 9,
         'read': 10, 'write': 11,
         'for': 12, 'to': 13, 'while': 14, 'do': 15, 'repeat': 16, 'until': 17, 'if': 18, 'then': 19, 'else': 20,
         'true': 43, 'false': 43,
         'var': 23, 'const': 24, '+': 25, '-': 26, '*': 27, '/': 28, '=': 29, '<': 30, '>': 31, 'and': 32, 'or': 33,
         'not': 34, '<=': 35, '>=': 36, '<>': 37,
         ':=': 38, '(': 44, ')': 45, ':': 46, '.': 47, ';': 48, ',': 49, '_': 50, "'": 51, '"': 52, '/*': 53, '*/': 54
         }


def init():  # 预处理
    try:
        output = open('output.txt', "r+")
        output.truncate()
        file = open('program.txt', 'r')
        tmp = open('tmp.txt', 'w')
        tag = 0
        while True:
            text_line = file.readline()
            if text_line:
                line_len = len(text_line)
                pointer = -1
                while pointer < line_len - 1:
                    pointer = pointer + 1
                    if text_line[pointer] == '/':
                        pointer += 1
                        if text_line[pointer] == '*':
                            break
                        pointer -= 1
                    elif text_line[pointer] == ' ':
                        if tag == 1:
                            continue
                        else:
                            tag = 1
                            tmp.write(' ')
                    elif text_line[pointer] == '\t' or text_line[pointer] == '\n' or text_line[pointer] == ' ':
                        if tag == 1:
                            continue
                        else:
                            tag = 1
                            tmp.write(' ')
                    elif text_line[pointer] == '"':
                        tmp.write(text_line[pointer])
                        pointer += 1
                        while pointer < line_len and text_line[pointer] != '"':
                            tmp.write(text_line[pointer])
                            pointer += 1
                        tmp.write(text_line[pointer])
                    elif text_line[pointer] == "'":
                        tmp.write(text_line[pointer])
                        pointer += 1
                        while pointer < line_len and text_line[pointer] != "'":
                            tmp.write(text_line[pointer])
                            pointer += 1
                        tmp.write(text_line[pointer])
                    else:
                        tag = 0
                        tmp.write(text_line[pointer])

            else:
                break
    finally:
        file.close()
        tmp.close()
        output.close()


def addtofile(w):    #输出到文件
    try:
        file = open('output.txt', 'a')
        if w in words.keys():
            output = '({value},"{key}")\r'.format(key=w, value=words[w])
            file.write(output)
        else:
            if w[0].isalpha():
                output = '({value},"{key}")\r'.format(key=w, value=39)
                file.write(output)
            elif w[0].isdigit() or w[0] == '+' or w[0] == '-':
                tag = 0
                for i in w:
                    if i == '.' or i == 'E' or i == 'e':
                        tag = 1
                        output = '({value},"{key}")\r'.format(key=w, value=41)
                        file.write(output)
                        break
                if tag == 0:
                    output = '({value},"{key}")\r'.format(key=w, value=40)
                    file.write(output)

    finally:
        file.close()


def RecogId():    #识别单词类型
    try:
        file = open('tmp.txt', 'r')
        text = file.readline()
        text_len = len(text)
        pointer = -1
        while pointer < text_len - 1:
            pointer += 1
            str = ''
            if text[pointer].isalpha():
                str = str + text[pointer]
                pointer += 1
                while pointer < text_len:
                    if text[pointer].isalpha() or text[pointer].isdigit():
                        str = str + text[pointer]
                        pointer += 1
                    else:
                        break
                pointer -= 1
                addtofile(str)

            elif text[pointer].isdigit():
                str = str + text[pointer]
                pointer += 1
                while pointer < text_len:
                    if text[pointer].isdigit() or text[pointer] == '.':
                        str = str + text[pointer]
                        pointer += 1
                    else:
                        break
                pointer -= 1
                addtofile(str)

            elif text[pointer] == '<':
                str = str + text[pointer]
                pointer += 1
                if text[pointer] == '=':
                    str = str + text[pointer]
                elif text[pointer] == '>':
                    str = str + text[pointer]
                else:
                    pointer -= 1
                addtofile(str)
            elif text[pointer] == '>':
                str = str + text[pointer]
                pointer += 1
                if text[pointer] == '=':
                    str = str + text[pointer]
                else:
                    pointer -= 1
                addtofile(str)
            elif text[pointer] == ':':
                str = str + text[pointer]
                pointer += 1
                if text[pointer] == '=':
                    str = str + text[pointer]
                else:
                    pointer -= 1
                addtofile(str)
            elif text[pointer] == '+' or text[pointer] == '-':
                str = str + text[pointer]
                pointer += 1
                if text[pointer].isdigit():
                    str = str + text[pointer]
                    pointer += 1
                    while pointer < text_len:
                        if text[pointer].isdigit() or text[pointer] == '.' or text[pointer] == 'E' or text[
                            pointer] == 'e' or text[pointer] == '+' or text[pointer] == '-':
                            str = str + text[pointer]
                            pointer += 1
                        else:
                            break
                    pointer -= 1
                    addtofile(str)
                else:
                    pointer -= 1
                    addtofile(str)
            else:
                addtofile(text[pointer])


    finally:
        file.close()


if __name__ == '__main__':
    init()
    RecogId()

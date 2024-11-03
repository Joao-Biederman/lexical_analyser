import re
from TokenClass import Token

def clean_line(line):
    cleaned_line = re.sub(r'💭.*?💭', '', line)
    return cleaned_line

def is_emote(word):
    if re.match(r'^(☕|🏁|🏳)', word) is not None:
        return True
    return False

def is_char(word):
    if re.match(r'^📄[a-zA-Z]📄', word) is not None:
        return True
    return False

def is_string(word):
    if re.match(r'📓((?:(?!📄).)*?)📓', word) is not None:
        return True
    return False

def is_math_operator(word):
    if re.match(r'^(\*|\/|➖|➕)', word) is not None:
        return True
    return False

def is_logic_operator(word):
    if re.match(r'^(<|>)', word) is not None:
        return True
    if re.match(r'^(= | >|<)(=)', word) is not None:
        return True
    return False

def is_identifier(word):
    if re.match(r'\b[a-z][a-zA-Z0-9_]{2,}\b', word) is not None:
        return True
    return False

def is_number(word):
    if re.match(r'^[0-9]+(\.[0-9]+)?$', word) is not None:
        return True
    return False

def is_parentesis(word):
    if re.match(r'^(\(|\))', word) is not None:
        return True
    return False

def is_letter(word):
    if re.match(r'^[a-zA-Z]', word) is not None:
        return True
    return False

def is_reserved_word(word):
    if word == 'main':
        return True
    if word == 'number':
        return True
    if word == 'char':
        return True
    if word == 'String':
        return True
    if word == 'Struct':
        return True
    if word == 'read':
        return True
    if word == 'write':
        return True
    if word == 'input':
        return True
    if word == 'print':
        return True
    if word == 'if':
        return True
    if word == 'else':
        return True
    if word == 'loop':
        return True
    return False

def define_token(word):
    if is_emote(word) == True:
        return word

    if is_parentesis(word) == True:
        return word

    if is_number(word[0]):
        if is_number(word) == True:
            return 'number'
        return (None, word)

    if is_math_operator(word) == True:
        return 'math_operator'

    if is_logic_operator(word) == True:
        return 'logic_operator'

    if is_letter(word[0]):
        if is_reserved_word(word) == True:
            return 'reserved_word'
        if is_identifier(word) == True:
            return 'identifier'

    if is_char(word):
        return 'char'

    if is_string(word):
        return 'string'

    if word == '=':
        return '='

    return (None, word) 

def terminate_word(char):
    if char == '🏁' or char == '🏳' or char == '☕' or char == '➕' or char == '➖':
        return True
    if char == '(' or char == ')':
        return True
    if char == '*' or char == '/':
        return True
    if char == ' ' or char == '\r' or char == '\n':
        return True
    return False

def could_be_logic(char):
    if char == '<' or char == '>':
        return True
    if char == '=':
        return True
    return False

def split_string(char, isString):
    if isString == False:
        if char == '📓' or char == '📄':
            isString = True
            isFinished = False
            return isFinished, isString 

    if char == '📓' or char == '📄':
        isFinished = True
        isString = False
        string = ''
    else:
        isFinished = False
        isString = True
    return isFinished, isString

def split_words(line, line_number):
    isString = False
    couldBeLogic = False
    string = ''
    line = line.lstrip()
    line = line.rstrip()
    words = []

    isString = False
    isFinished = False
    isLogic = False

    for char in line:
        if isString == True:
            isFinished, isString = split_string(char, isString)
            string += char
            if isFinished:
                words.append(string)
                string = ''
                isString = False
                isFinished = False
        elif isLogic == True:
            isLogic = False
            if char == '=':
                string += char
                words.append(string)
                string = ''
            else:
                words.append(string)
                if char == '<' or char == '>':
                    isLogic = True
                    string = char
                elif char == '📓' or char == '📄':
                    isString = True
                    string = char
                else:
                    if terminate_word(char) != True:
                        string = char
        else:
            if terminate_word(char):
                words.append(string)
                if char != ' ' and char != '\r' and char != '\n':
                    string = char
                    words.append(string)
                string = ''
            elif char == '📓' or char == '📄':
                isString = True
                string = char
            else :
                string += char

    if string:
        words.append(string)

    words = [word for word in words if (word and word != ' ' and word != '\r' and word != '\n')]

    if words and (words[0] == "" or words[0].isspace()):
        words = words[1:]

    token_list = []
    for word in words:
        token_type = define_token(word)
        if token_type == (None, word):
            return (None, word)
        token_list.append(Token(token=word, type=token_type, line=line_number))
    return token_list

filename = 'testfile.zoz'
with open('code_files/' + filename, 'rb') as file:
    lines = file.readlines()
    i = 1
    token_list = []
    isComment = False
    isString = False
    for line in lines:
        flags = (isString, isComment)
        line = line.decode('utf-8')
        line = clean_line(line)
        tokens = split_words(line, i)
        if tokens and tokens[0] == None:
            print("Ocorreu um erro na linha ", i)
            print("Token ", tokens[1], " não reconhecido")
            print(line)
            break

        token_list += split_words(line, i)
        i += 1

    print ('tokens')
    for token in token_list:
        print(f'Token: \n  Valor:{token.token}\n  Tipo:{token.type}\n  Linha:{token.line}')
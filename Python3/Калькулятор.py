from decimal import Decimal, InvalidOperation
import re


def withount(a):  # Функция, которая убирает .0
    if a <= 10 ** 100 and int(a) == a:
        return int(a)
    else:
        return a


def again():  # Ввод данных снова
    give = input('Введите пример еще раз: ')
    give = give.replace(' ', '', give.count(' '))
    return give


def summ(lst):  # Сумма строк из списка
    k = ''
    for i in lst:
        k += i
    return k


# Раскрытие скобок
def changing(): return re.search(re_parentheses, out).start() + 1, re.search(re_parentheses, out).end() - 1


def num_op2op(lst):  # Превращение "Число + Число" и "Число - Число" в "+" и "-" соответственно
    p = r'\d*[.,]?\d+|[+-]\('
    for i in range(len(lst)):
        k = lst[i]
        if not (re.search(p, k) is None):
            k = re.sub(p, r'', k)
            lst.pop(i)
            lst.insert(i, k)
    return lst


def str2Decimal(lst):  # Перебор полученных чисел
    k = []
    for i in lst:
        try:
            k.append(Decimal(i))
        except InvalidOperation:
            if ',' in i:
                k.append(Decimal(i.replace(',', '.')))
    return k


def equal(n):  # Перебор операторов в списке
    try: a1 = n.index('/')
    except ValueError: a1 = float('inf')
    try: a2 = n.index('*')
    except ValueError: a2 = float('inf')
    try: a3 = n.index('^')
    except ValueError: a3 = float('inf')
    if a1 == float('inf') and a2 == float('inf') and a3 == float('inf'):
        try: a4 = n.index('+')
        except ValueError: a4 = float('inf')
        try: a5 = n.index('-')
        except ValueError: a5 = float('inf')
        return min([a4, a5])
    else:
        return min([a1, a2, a3])


def operator2act(lst, lstnum):  # Перебор полученных операторов
    ans = 0
    while len(lstnum) != 1:
        act = equal(lst)
        if lst[act] == '/':
            try:
                ans = lstnum[act] / lstnum[act + 1]
            except ZeroDivisionError:
                print('В процессе вычислений вы поделили на ноль.\nИз-за этого будет произведён выход из программы.\n'
                      'Ваш введенный пример сохранён в файл ZeroDivisionArithmeticExample.txt\nВыход из программы')
                with open('ZeroDivisionArithmeticExample.txt', 'a', encoding='UTF-8') as f:
                    f.writelines(given)
                quit()
        elif lst[act] == '*':
            ans = lstnum[act] * lstnum[act + 1]
        elif lst[act] == '^':
            if lstnum[act] == 0 and lstnum[act + 1] == 0:
                print('В процессе вычислений вы возвели 0 в степень 0, что равно неопределенности.\nИз-за этого бу'
                      'дет произведён выход из программы. Ваш введенный пример сохранён в файл ZeroToThePowerOfZeroArit'
                      'hmeticExample.txt\nВыход из программы')
                with open('ZeroToThePowerOfZeroArithmeticExample.txt', 'a', encoding='UTF-8') as f:
                    f.writelines(given)
                quit()
            else:
                ans = lstnum[act] ** lstnum[act + 1]
        elif lst[act] == '+':
            ans = lstnum[act] + lstnum[act + 1]
        elif lst[act] == '-':
            ans = lstnum[act] - abs(lstnum[act + 1])

        lst.pop(act)
        lstnum.pop(act)
        lstnum.insert(act, ans)
        lstnum.pop(act + 1)
    return ans


# Ввод данных
given = input('Введите пример: ')
given = given.replace(' ', '', given.count(' '))

# Регулярные выражения
re_nums = r'[(]?[-+]?\d*[.,]?\d+[)]?|\d*[.,]?\d+'  # Числа
re_operators = r'[/*^]|\d*[.,]?\d+[+-]|[+-]\('  # Операторы
re_parentheses = r'[()]'  # Скобки
re_all = re_nums + r'|' + re_operators + r'|' + re_parentheses  # Операторы + Числа + Скобки

havenums = re.search(re_nums, given)  # Есть ли число в примере
re_oper = r'[-+/*^]{2,}'  # Ловить больше двух операторов подряд

# Что нашлось из вводных данных по регулярным выражениям
out_lst = re.findall(re_all, given)
out = summ(out_lst)

# Проверка, того что нашлось из вводных данных по регулярным выражениям с вводными данными и прочее
while out != given or given == '' or havenums is None or given.count('(') > given.count(')') + 1 or \
        not (re.search(re_oper, given) is None) or given.count(')') > given.count('(') or '()' in given or \
        ('/0' in given and (not '/0.' in given or not '/0,' in given)) or \
        ('^0' in given and (not '^0.' in given or not '^0,' in given)) or '()' in given + ')' or \
        not (re.match(r'[*/^]', given) is None) or not (re.search(r'[-+*/^]$', given, re.MULTILINE) is None):

    if given == '':
        print('Вы ввели пустой пример')
    elif havenums is None:
        print('Вы ввели пример без чисел')
    elif not (re.search(re_oper, given) is None):
        print('Вы ввели более одного операторов подряд в примере')
    elif not (re.match(r'[*/^]', given) is None) or not (re.search(r'[-+*/^]$', given, re.MULTILINE) is None):
        print('Вы не дописали пример')
    elif given.count('(') > given.count(')') + 1 or given.count(')') > given.count('('):
        print(r'Введите равное количество "(" и ")"')
    elif '()' in given or '()' in given + ')':
        print('Вы ввели пустые скобки в примере')
    elif '^0' in given and (not '^0.' in given or not '^0,' in given):
        print('0 в степени 0 - неопределенное выражение')
    elif '/0' in given and (not '/0.' in given or not '/0,' in given):
        print('На ноль делить нельзя')
    elif out != given:
        print(r'Введите пример без букв, c одной или без "." (",") в числе и иных символов отличных от "0-9", "-", "+",'
              r' "/", "*", "^", и "(", ")"')

    print('Получено:', out)
    given = again()
    havenums = re.search(re_nums, given)
    out_lst = re.findall(re_all, given)
    out = summ(out_lst)

# Добавить ")", если кол-во "(" == кол-ву ")" - 1
if given.count('(') == given.count(')') + 1:
    out += ')'
    print(fr'Вы ввели "(" больше ")" на 1, пример был закрыт ")". Получено: {out}')

out = '(' + out + ')'  # Сам пример - огромная скобка

# Улавливать скобки
re_parentheses = r'[(][\d+/^*-.,]+[)]'

# Вычисления внутри скобок
j = 0
while '(' in out:
    j = j + 1
    st, end = changing()

    if not (re.search(r'[\d.,]\(', out[st - 2:st]) is None):
        out = out[0:st - 1] + '*(' + out[st:]
        st, end = changing()
    if not (re.search(r'\)[\d.,]', out[end:end + 2]) is None):
        out = out[0:end] + ')*' + out[end + 1:]
        st, end = changing()

    change = out[st:end].replace('--', '+', out[st:end].count('--'))
    lstnums, lstoperators = re.findall(re_nums, change), num_op2op(re.findall(re_operators, change))
    lstnums = str2Decimal(lstnums)

    if len(lstnums) == 1:
        change = lstnums[0]
    else:
        change = operator2act(lstoperators, lstnums)
    out = out[0:st - 1] + str(change) + out[end + 1:]

    if '(' in out:  # Ответ
        print(f'Убираем {j} скобку:', out[1:len(out) - 1])
    else:
        print('Ответ:', withount(Decimal(out)))

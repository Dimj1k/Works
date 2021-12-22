from decimal import Decimal, InvalidOperation
import re


# Функция, которая убирает .0
def withount(a):
    if a <= 10 ** 100 and int(a) == a:
        return int(a)
    else:
        return a


# Сумма строк из списка
def summ(lst):
    k = ''
    for i in lst:
        k += i
    return k


# Скобки в примере
def changing(out):
    return re.search(r'[(][\d+/^*-.,]+[)]', out).start() + 1, re.search(r'[(][\d+/^*-.,]+[)]', out).end() - 1


# Превращение "Число + Число" и "Число - Число" в "+" и "-" соответственно
def num_op2op(lst):
    p = r'\d*[.,]?\d+|[+-]\('
    for i in range(len(lst)):
        k = lst[i]
        if not (re.search(p, k) is None):
            k = re.sub(p, r'', k)
            lst.pop(i)
            lst.insert(i, k)
    return lst


# Перебор полученных чисел
def str2Decimal(lst):
    k = []
    for i in lst:
        try:
            k.append(Decimal(i))
        except InvalidOperation:
            if ',' in i:
                k.append(Decimal(i.replace(',', '.')))
    return k


# Перебор операторов в списке
def equal(n):
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


# Перебор полученных операторов
def operator2act(lst, lstnum):
    ans = 0
    while len(lstnum) != 1:
        act = equal(lst)
        if lst[act] == '/':
            try:
                ans = lstnum[act] / lstnum[act + 1]
            except (ZeroDivisionError, InvalidOperation):
                print('В процессе вычислений вы поделили на ноль')
                return main(input('Введите пример еще раз: '))
        elif lst[act] == '*':
            ans = lstnum[act] * lstnum[act + 1]
        elif lst[act] == '^':
            if lstnum[act] == 0 and lstnum[act + 1] == 0:
                print('В процессе вычислений вы возвели 0 в степень 0, что равно неопределенности')
                return main(input('Введите пример еще раз: '))
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


# Основная функция
def main(given):
    # Ввод данных
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
    if given == '':
        print('Вы ввели пустой пример')
        return main(input('Введите пример еще раз: '))
    elif given == 'q' or given == 'Выйти' or given == 'В' or given == 'exit' or given == 'e' or given == 'quit':
        print('Выход из программы')
        quit()
    elif havenums is None:
        print('Вы ввели пример без чисел')
        return main(input('Введите пример еще раз: '))
    elif not (re.search(re_oper, given) is None):
        print('Вы ввели более одного операторов подряд в примере')
        return main(input('Введите пример еще раз: '))
    elif not (re.match(r'[*/^]', given) is None) or not (re.search(r'[-+*/^]$', given, re.MULTILINE) is None) or \
            not (re.search(r'\([*/^]', given) is None) or not (re.search(r'[-+*/^]\)', given) is None):
        print('Вы не дописали пример')
        return main(input('Введите пример еще раз: '))
    elif given.count('(') > given.count(')') + 1 or given.count(')') > given.count('('):
        print(r'Введите равное количество "(" и ")"')
        return main(input('Введите пример еще раз: '))
    elif '()' in given or '()' in given + ')':
        print('Вы ввели пустые скобки в примере')
        return main(input('Введите пример еще раз: '))
    elif out != given:
        print(r'Введите пример без букв, c одной или без "." (",") в числе и иных символов отличных от "0-9", "-", "+",'
              r' "/", "*", "^", и "(", ")"', '\nПолучено:', out)
        return main(input('Введите пример еще раз: '))

    # Добавить ")", если кол-во "(" == кол-ву ")" - 1
    if given.count('(') == given.count(')') + 1:
        out += ')'
        print(fr'Вы ввели "(" больше ")" на 1, пример был закрыт ")". Получено: {out}')

    out = '(' + out + ')'  # Сам пример - огромная скобка

    # Вычисления внутри скобок
    j = 0
    while '(' in out:
        j = j + 1
        st, end = changing(out)

        if not (re.search(r'[\d.,]\(', out[st - 2:st]) is None):
            out = out[0:st - 1] + '*(' + out[st:]
            st, end = changing(out)
        if not (re.search(r'\)[\d.,]', out[end:end + 2]) is None):
            out = out[0:end] + ')*' + out[end + 1:]
            st, end = changing(out)

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
            return main(input('Введите пример: '))


main(input('Введите пример: '))

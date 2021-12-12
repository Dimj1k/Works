from decimal import Decimal, getcontext, InvalidOperation
import re
getcontext().prec = 16

def again(): # Ввод данных снова
    give = input('Введите пример еще раз: ')
    give = give.replace(' ', '', give.count(' '))
    return give


def summ(lst): # Сумма строк из списка
    k = ''
    for i in lst:
        k += i
    return k


def str2Decimal(lst): # Перебор полученных чисел
    k = []
    for i in lst:
        try:
            k.append(Decimal(i))
        except InvalidOperation:
            if ',' in i:
                k.append(Decimal(i.replace(',', '.')))
    return k


def equal(n): # Перебор операторов в списке
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


def operator2act(lst, lstnum): # Перебор полученных операторов
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
        if lst[act] == '*':
            ans = lstnum[act] * lstnum[act + 1]
        if lst[act] == '^':
            if lstnum[act] == 0 and lstnum[act + 1] == 0:
                print('В процессе вычислений вы возвели 0 в степень 0, данное выражение неопределено.\nИз-за этого бу'
                      'дет произведён выход из программы. Ваш введенный пример сохранён в файл ZeroToThePowerOfZeroArithme'
                      'ticExample.txt\nВыход из программы')
                with open('ZeroToThePowerOfZeroArithmeticExample.txt', 'a', encoding='UTF-8') as f:
                    f.writelines(given)
                quit()
            else:
                ans = lstnum[act] ** lstnum[act + 1]
        if lst[act] == '+':
            ans = lstnum[act] + lstnum[act + 1]
        if lst[act] == '-':
            ans = lstnum[act] + lstnum[act + 1]
        lst.pop(act)
        lstnum.pop(act)
        lstnum.insert(act, ans)
        lstnum.pop(act + 1)
    return ans


# Ввод данных
given = input('Введите пример: ')
given = given.replace(' ', '', given.count(' '))

# Регулярные выражения
re_nums = r'[(]?[-+]?\d*[.,]?\d+[)]?|\d*[.,]?\d+' # Числа
re_operators = r'[-+/*^]' # Операторы
re_parentheses = r'[()]' # Скобки
re_all = re_nums + r'|' + re_operators + r'|' + re_parentheses # Операторы + Числа + Скобки

havenums = re.search(re_nums, given) # Есть ли число в примере
re_oper = r'[-+/*^]+' # Ловить больше двух операторов подряд

# Что нашлось из вводных данных по регулярным выражениям
out_lst = re.findall(re_all, given)
out = summ(out_lst)

# Проверка, того что нашлось из вводных данных по регулярным выражениям с вводными данными и прочее
while out != given or given == '' or havenums is None or given.count('(') > given.count(')') + 1 or \
        re.findall(re_oper, given) != re.findall(re_operators, given) or given.count(')') > given.count('(') or \
        '()' in given:
    if given == '':
        print('Вы ввели пустой пример')
    elif out != given:
        print(r'Введите пример без букв, c одной или без "." (",") в числе и иных символов отличных от "0-9", "-", "+",'
              r' "/", "*", "^", и "(", ")"')
    elif havenums is None:
        print('Вы ввели пример без чисел')
    elif given.count('(') > given.count(')') + 1 or given.count(')') > given.count('('):
        print(r'Введите равное количество "(" и ")"')
    elif re.findall(re_oper, given) != re.findall(re_operators, given):
        print('Вы ввели более одного операторов подряд в примере')
    elif '()' in given:
        print('Вы ввели "()" в примере')
    given = again()
    havenums = re.search(re_nums, given)
    out_lst = re.findall(re_all, given)
    out = summ(out_lst)

# Добавить ")", если кол-во "(" == кол-ву ")" - 1
if given.count('(') == given.count(')') + 1:
    given += ')'
    out += ')'
    print(fr'Вы ввели "(" больше ")" на 1, пример был закрыт ")". Получено: {out}')
out = '(' + out + ')' # Сам пример - огромная скобка

# Вычисления внутри скобок
re_parentheses = r'[(][\d+/^*-.,]+[)]' # Улавливать скобки
i = 0
while '(' in out:
    i = i + 1
    change = re.search(re_parentheses, out)
    st = change.start() + 1
    end = change.end() - 1
    ps = out[st - 2:st]
    if '0(' == ps or '1(' == ps or '2(' == ps or '3(' == ps or '4(' == ps or '5(' == ps or '6(' == ps or '7(' == ps or \
            '8(' == ps or '9(' == ps:
        out = out[0:st - 1] + '*(' + out[st:]
        change = re.search(re_parentheses, out)
        st = change.start() + 1
        end = change.end() - 1
    change = out[st:end]
    lstnums, lstoperators = re.findall(re_nums, change), re.findall(re_operators, change)
    while len(lstnums) < len(lstoperators):
        for j in range(len(lstnums)):
            if '+' in lstnums[j] or '-' in lstnums[j]:
                lstoperators.pop(j)
    lstnums = str2Decimal(lstnums)
    if len(lstnums) == 1:
        change = lstnums[0]
    else:
        change = operator2act(lstoperators, lstnums)
    out = out[0:st - 1] + str(change) + out[end + 1:]
    if '(' in out:
        print(f'Убираем {i} скобку:', out[1:len(out) - 1])
    else:
        print('Ответ:', out)

def znak(x):
    qw = str(x)
    if '.' in qw:
        return abs(qw.find('.') - len(qw)) - 1
    else:
        return 0
def gdeznak(*ar):
    wt = [znak(a) for a in ar]
    wt = max(wt)
    if wt >= 16:
        wt = 10000
    return wt
def pdiap(c, d, e, wt):
    if c <= d:
        while c <= d and e > 0:
            yield c
            c = round(c + e, wt)
    elif c >= d:
        while c >= d and e > 0:
            yield c
            c = round(c - e, wt)
def withount(w):
    if w != float('inf') and int(w) == w:
        return int(w)
    else:
        return w
def a_ti_kto(who):
    non_int_neg = 0
    negative = 0
    non_int = 0
    for i in range(len(who)):
        if who[i] < 0 and type(who[i]) == float:
            non_int_neg += 1
        elif type(who[i]) == float:
            non_int += 1
        elif who[i] <= 0:
            negative += 1
    return non_int, negative, non_int_neg
def multiply(m, a):
    if znak(a) + znak(m) <= 8 and znak(a) <= 2:
        return round(m * a, znak(m) + znak(a))
    else:
        return m * a
def simple_composite(a):
    i = 0
    b = 0
    while type(a) == int and i <= a:
        i = i + 1
        if a % i == 0:
            b = b + 1
        if b > 2:
            break
    return b
def even_odd(a):
    if type(a) == int and a % 2 == 0:
        return str(a)
    elif type(a) == int and a % 2 != 0:
        return str(a)
def palindrom(a):
    k = str(a)
    k = k[::-1]
    if str(a) == k and (a >= 0 or type(a) == float):
        return str(a)
    else:
        return ''


def func_for_one(v):
    v = withount(v)
    print('Это число:', v)
    if simple_composite(v) > 2 and v > 0:
        print('Это число составное')
    elif simple_composite(v) == 2 and v > 0:
        print('Это число простое')
    elif v == 1:
        print('Это натуральное число - единица, оно не простое и не составное. По определению простые и составные числа - натуральные числа больше 1')
    elif v <= 0 and type(v) == int:
        print('Это число неположительное. По определению простые и составные числа - натуральные числа больше 1')
    elif type(v) == float:
        print('Это число нецелое. По определению простые и составные числа - натуральные числа больше 1')
    if type(v) == int and v % 2 == 0:
        print('Это число чётное')
    elif type(v) == int and v % 2 != 0:
        print('Это число нечётное')
    else:
        print('Это число нецелое. Чтобы определить чётное или нечётное число - оно должно быть целым')
    if palindrom(v) != '':
        print('Это число является палиндромом')
    else:
        print('Это число не является палиндромом')


def func(c, d, e, wt):
    lst = [withount(diap) for diap in pdiap(c, d, e, wt)]
    yield lst
    no_int, neg, no_int_neg = a_ti_kto(lst)
    yield withount(sum(lst))
    simple = ''
    composite = ''
    even = ''
    odd = ''
    pal = ''
    mult = 1
    for j in range(len(lst)):
        mult = multiply(mult, lst[j])
    yield mult
    for j in range(len(lst)):
        q = simple_composite(lst[j])
        if q == 2:
            simple = simple + str(lst[j]) + '; '
        elif q > 2:
            composite = composite + str(lst[j]) + '; '
    if len(simple) + len(composite) > 0:
        yield 'Z'
        if len(simple) == 0:
            yield 'нет  '
        else:
            yield simple
        if len(composite) == 0:
            yield 'нет  '
        else:
            yield composite
    elif neg == len(lst):
        yield 'Z и <= 0'
        yield 'Промежуток состоит только из целых неположительных чисел. По определению простые и составные числа - натуральные числа больше единицы'
    elif no_int + no_int_neg == len(lst):
        yield 'неZ'
        yield 'Промежуток состоит только из нецелых чисел. По определению простые и составные числа - натуральные числа больше единицы'
    elif no_int + no_int_neg + neg == len(lst):
        yield 'неZ и <= 0'
        yield 'Промежуток состоит только из нецелых и неположительных чисел. По определению простые и составные числа - натуральные числа больше единицы'
    else:
        yield '1'
        yield 'Положительная часть промежутка состоит из натурального числа 1, которое не является простым или составным. По определению простые и составные числа - натуральные числа больше единицы'
    for j in range(len(lst)):
        if type(lst[j]) == int and lst[j] % 2 == 0:
            even = even + even_odd(lst[j]) + '; '
        elif type(lst[j]) == int and lst[j] % 2 != 0:
            odd = odd + even_odd(lst[j]) + '; '
    if len(even) + len(odd) > 0:
        yield 'Zp'
        if len(even) == 0:
            yield 'нет  '
        else:
            yield even
        if len(odd) == 0:
            yield 'нет  '
        else:
            yield odd
    elif no_int_neg + no_int == len(lst):
        yield 'неZp'
        yield 'Промежуток состоит только из нецелых чисел. По определению чётные и нечётные числа - целые числа'
    for j in range(len(lst)):
        pt = palindrom(lst[j])
        if pt != '':
            pal = pal + pt + '; '
    if len(pal) == 0:
        yield 'нет  '
    else:
        yield pal


print('<<<--------------Ввод-------------->>>')
x = float(input('Введите первое число для создания промежутка: '))
y = float(input('Введите второе число для создания промежутка: '))
n = 1
if x != y:
    n = abs(float(input('Введите длину шага между двумя числами в промежутке (число отличное от нуля): ')))
    if n == 0:
        print('------------------------------------------------------------')
        print('Вы указали длину шага между двумя числами равный 0', 'Выход из программы', sep='\n')
        print('------------------------------------------------------------')
        exit()
print('>>>--------------Ввод--------------<<<')
if x == y or (abs(x) < abs(y) and abs(round(x + n, gdeznak(znak(x), znak(n)))) > abs(y)) or (abs(y) < abs(x) and abs(round(y + n, gdeznak(znak(n), znak(y)))) > abs(x)):
    print('<<<--------------Вывод-------------->>>')
    if (abs(x) < abs(y) and abs(x + n) > abs(y)) or (abs(y) < abs(x) and abs(y + n) > abs(x)) and x != y:
        print('Вы указали сумму по модулю первого числа и шага больше чем второе число. Поэтому промежуток представлен в виде первого числа')
    func_for_one(x)
    print('<<<--------------Вывод-------------->>>')
    exit()
Task = func(x, y, n, gdeznak(x, y, n))
print('<<<--------------Вывод-------------->>>')
print('Созданный промежуток по двум числам и шагу:', next(Task))
print('Сумма чисел данного промежутка: ', round(next(Task), gdeznak(x, y, n)), sep='')
print('Произведение чисел данного промежутка: ', next(Task), sep='')
Nat=next(Task)
if Nat == 'Z':
    print('Простые числа данного промежутка: ', next(Task)[0:-2], sep='')
    print('Составные числа данного промежутка: ', next(Task)[0:-2], sep='')
elif Nat == 'неZ и <= 0' or Nat == 'Z и <= 0' or Nat == 'неZ' or Nat == '1':
    print(next(Task))
Z = next(Task)
if Z == 'Zp':
    print('Чётные числа данного промежутка: ', next(Task)[0:-2], sep='')
    print('Нечётные числа данного промежутка: ', next(Task)[0:-2], sep='')
elif Z == 'неZp':
    print(next(Task))
print('Палиндром числа данного промежутка: ', next(Task)[0:-2], sep='')
print('>>>--------------Вывод--------------<<<')

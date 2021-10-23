def znak(x):
    qw = str(x)
    if '.' in qw:
        return abs(qw.find('.') - len(qw)) - 1
    else:
        return 0
def pdiap(c, d, e):
    wt = max([znak(c), znak(d), znak(e)])
    if c <= d and wt < 16:
        while c <= d and e > 0:
            yield c
            c = round(c + e, wt)
    elif c >= d and wt < 16:
        while c >= d and e > 0:
            yield c
            c = round(c - e, wt)
    elif c <= d and wt > 15:
        while c <= d and e > 0:
            yield c
            c = c + e
    elif c >= d and wt > 15:
        while c >= d and e > 0:
            yield c
            c = c - e
def withount(w):
    if int(w) == w:
        return int(w)
    else:
        return w
def newlst(lst, addnum, removenum):
    for num1 in addnum:
        lst.append(withount(num1))
    for num2 in removenum:
        if num2 in lst:
            lst.remove(num2)
        else:
            print('Число',withount(num2),'не найдено в промежутке.')
    return lst


def func(lst):
    simple = ''
    even = ''
    odd = ''
    pal = ''
    composite = ''
    mult = 1
    m = 0
    yield lst
    yield withount(sum(lst))
    for j in range(len(lst)):
        mult = mult * lst[j]
    yield mult
    lst=set(lst)
    lst=list(lst)
    for j in range(len(lst)):
        i = 0
        q = 0
        while i <= lst[j]:
            i = i + 1
            if lst[j] % i == 0:
                q = q + 1
            if q > 2:
                break
        if q == 2:
            simple = simple + str(lst[j]) + '; '
        elif q > 2:
            composite = composite + str(lst[j]) + '; '
    if len(simple) != 0:
        yield simple
    else:
        yield 'нет.  '
    if len(composite) != 0:
        yield composite
    else:
        yield 'нет.  '
    for j in range(len(lst)):
        if type(lst[j]) == int and lst[j] % 2 == 0:
            even = even + str(lst[j]) + '; '
        elif type(lst[j]) == int and lst[j] % 2 != 0:
            odd = odd + str(lst[j]) + '; '
    if len(even) != 0:
        yield even
    else:
        yield 'нет.  '
    if len(odd) != 0:
        yield odd
    else:
        yield 'нет.  '
    for j in range(len(lst)):
        k = str(abs(lst[j]))
        k = k[::-1]
        if str(abs(lst[j])) == k and (abs(lst[j]) > 9 or type(lst[j]) == float):
            m = m + 1
            pal = pal + str(lst[j]) + '; '
    if m == 0:
        yield 'нет.  '
    else:
        yield pal


print('<<<--------------Ввод-------------->>>')
x = float(input('Введите первое число для создания промежутка: '))
y = float(input('Введите второе число для создания промежутка: '))
n = float(input('Введите шаг между числами в промежутке (число больше нуля): '))
genlst = [withount(diap) for diap in pdiap(x, y, n)]
print('==========================================')
print('Созданный промежуток по двум числам и шагу -', genlst)
if len(genlst) == 0 and n == 0:
    print('Вы указали шаг между числами равный 0', 'Добавьте числа, чтобы создать промежуток', sep='\n')
elif len(genlst) == 0 and n < 0:
    print('Вы указали шаг между числами меньше 0', 'Добавьте числа, чтобы создать промежуток', sep='\n')
print('==========================================')
z1 = int(input('Укажите, сколько чисел нужно добавить в указанный промежуток (целое число): '))
f1 = []
f2 = []
if z1 > 0:
    print('-----------------------------')
for i in range(z1):
    f1 = [float(input('Укажите, какое число нужно добавить в указанный промежуток: '))] + f1
if z1 > 0:
    print('-----------------------------')
z2 = int(input('Укажите, сколько чисел нужно убрать из указанного промежутка (целое число): '))
if z2 > 0:
    print('-----------------------------')
for i in range(z2):
    f2 = [float(input('Укажите, какое число нужно убрать из указанного промежутка: '))] + f2
if z2 > 0:
    print('-----------------------------')
print('>>>--------------Ввод--------------<<<')
genlst = newlst(genlst, f1, f2)
genlst.sort()
Task = func(genlst)
print('<<<--------------Вывод-------------->>>')
print('Созданный промежуток на вводе -', genlst)
if len(next(Task)) != 0:
    print('Сумма чисел данного промежутка: ', next(Task), sep='')
    print('Произведение чисел данного промежутка: ', next(Task), sep='')
    print('Простые числа данного промежутка: ', next(Task)[0:-2], sep='')
    print('Составные числа данного промежутка: ', next(Task)[0:-2], sep='')
    print('Чётные числа данного промежутка: ', next(Task)[0:-2], sep='')
    print('Нечётные числа данного промежутка: ', next(Task)[0:-2], sep='')
    print('Палиндром числа данного промежутка: ', next(Task)[0:-2], sep='')
else:
    print('Увы, но Вы задали программе пустой промежуток')
print('>>>--------------Вывод--------------<<<')
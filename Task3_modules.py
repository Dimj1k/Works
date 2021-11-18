from math import sin, cos, radians, log, e, pi, exp


# ------------------------------------------------Функция------------------------------------------------
def y(x): return 2 * x
# ------------------------------------------------Функция------------------------------------------------


def s_fl(a, b, n, e, s2=0):
    k = abs((b - a) / n)
    s1 = 0
    for i in range(0, int(k)):
        s1 += abs(y(a + i * n) * n)
    s1 += (k - int(k)) * n * abs(y(a + int(k) * n))
    if abs(s2 - s1) <= e:
        return s1
    else:
        return s_fl(a, b, n / 2, e, s1)


def s_fc(a, b, n, e, s2=0):
    k = abs((b - a) / n)
    s1 = 0
    for i in range(1, int(k) + 1):
        s1 += abs(y(a + (2 * i - 1) * n / 2) * n)
    if int(k) != k:
        s1 += abs(y(((b - (a + int(k) * n)) / 2) + (a + int(k) * n)) * (b - (a + int(k) * n)))
    if abs(s2 - s1) <= e:
        return s1
    else:
        return s_fc(a, b, n / 2, e, s1)


def s_fr(a, b, n, e, s2=0):
    k = abs((b - a) / n)
    s1 = 0
    for i in range(0, int(k)):
        s1 += abs(y(b - i * n) * n)
    s1 += (k - int(k)) * n * abs(y(b - int(k) * n))
    if abs(s2 - s1) <= e:
        return s1
    else:
        return s_fr(a, b, n / 2, e, s1)


def s_fm(a, b, n, e, s2=0):
    c = (b + a) / 2
    k1 = abs((c - b) / n)
    k2 = abs((c - a) / n)
    s1 = 0
    for i in range(0, int(k1)):
       s1 += abs(y(c + i * n) * n)
    for i in range(0, int(k2)):
       s1 += abs(y(c - i * n) * n)
    s1 += (k1 - int(k1)) * n * abs(y(c + int(k1) * n)) + (k2 - int(k2)) * n * abs(y(c - int(k1) * n))
    if abs(s2 - s1) <= e:
        return s1
    else:
        return s_fm(a, b, n / 2, e, s1)


x1, x2 = float(input('Введите первую координату X: ')), float(input('Введите вторую координату X: '))
if x1 >= x2:
    print('Введите первую координату X по численному значению меньше второй')
    quit()
step = 1
acc = abs(float(input('Введите нужную погрешность: ')))
m = input('Выберите метод прямоугольников (1. левых(l), 2. средних(c) или 3. правых(r) или все сразу (по умолчанию)): ')


if m == 'Левых' or m == 'L' or m == 'l' or m == 'левых' or m == 'л' or m == 'Л' or m == 'k' or m == 'K' or m == 'д' \
        or m == 'Д' or m == '1':
    print(f'Площадь фигуры равна по методу левых прямоугольников с погрешностью {acc}:', s_fl(x1, x2, step, acc))
elif m == 'Средних' or m == 'C' or m == 'c' or m == 'средних' or m == 'с' or m == 'С' or m == '2':
    print(f'Площадь фигуры равна по методу средних прямоугольников с погрешностью {acc}:', s_fc(x1, x2, step, acc))
elif m == 'Правых' or m == 'R' or m == 'r' or m == 'правых' or m == 'п' or m == 'П' or m == 'g' or m == 'G' or m == 'К'\
        or m == 'к' or m == '3':
    print(f'Площадь фигуры равна по методу правых прямоугольников с погрешностью {acc}:', s_fr(x1, x2, step, acc))
else:
    print(f'Площадь фигуры равна по методу левых прямоугольников с погрешностью {acc}:', s_fl(x1, x2, step, acc))
    print(f'Площадь фигуры равна по методу средних прямоугольников с погрешностью {acc}:', s_fc(x1, x2, step, acc))
    print(f'Площадь фигуры равна по методу правых прямоугольников с погрешностью {acc}:', s_fr(x1, x2, step, acc))
if m == 'М' or m == 'м' or m == 'v' or m == 'V' or m == 'С медианы' or m == 'с медианы':
    print(f'Площадь фигуры равна по методу прямоугольников с медианы x1 и x2 и погрешностью {acc}:',
          s_fm(x1, x2, step, acc))

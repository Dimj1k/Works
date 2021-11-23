from math import sin, cos, exp, e, pi, log


# -------------------------------------Функция-------------------------------------
def f(x): return 2 ** x
# -------------------------------------Функция-------------------------------------


# Метод парабол
# Вычисление определителя матрицы 3x3
def det3x3(d, j, h):
    return d[0] * j[1] * h[2] + d[1] * j[2] * h[0] + d[2] * j[0] * h[1] - d[0] * j[2] * h[1] - d[1] * j[0] * h[2] - \
           d[2] * j[1] * h[0]


# Определенный интеграл параболы
def integrate(d, j, h, o, m):
    d = (d * (o + m) ** 3) / 3 - (d * o ** 3) / 3
    j = (j * (o + m) ** 2) / 2 - (j * o ** 2) / 2
    h = h * (o + m) - (h * o)
    return d + j + h


# Поиск членов квадратного трёхчлена и значение определенного интеграла найденной параболы
def s_fp(x1, x2, n, epsilon, s2=0):
    if n == 2 ** 17: return s2
    cx = [1, 1, 1]
    s1 = 0
    x1save = x1
    step = (x2 - x1) / n
    while x1 < x2:
        # Матрицы. Создание системы линейных уравнений
        ax = [x1 ** 2, (x1 + step / 2) ** 2, (x1 + step) ** 2]
        bx = [x1, (x1 + step / 2), (x1 + step)]
        v = [f(x1), f(x1 + step / 2), f(x1 + step)]
        # Поиск членов квадратного трёхчлена с помощью метода Крамера
        p = det3x3(ax, bx, cx)
        a = det3x3(v, bx, cx) / p
        b = det3x3(ax, v, cx) / p
        c = det3x3(ax, bx, v) / p
        # -----------------------
        s1 += integrate(a, b, c, x1, step)
        x1 = x1 + step
    if abs(s2 - s1) <= epsilon:
        return s1
    else:
        return s_fp(x1save, x2, n * 2, epsilon, s1)


# ax^2 + bx + c = f(x)
x0 = float(input('Введите первую координату по X: '))
y = float(input('Введите вторую координату по X: '))
if x0 >= y:
    print('Введите первую координату по X меньше чем вторую')
    quit()
k = 1
acc = abs(float(input('Введите погрешность (число не равное нулю): ')))
if acc == 0:
    print('Введите погрешность не равное нулю')
    quit()


print('Определенный интеграл данной фигуры примерно равен по методу парабол:', s_fp(x0, y, k, acc))

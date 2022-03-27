from math import *
import re


class Func:

    def __init__(self, fx: str):
        self.fx = fx
        self.f = lambda x: eval(self.fx)

    @property
    def set_fx(self):
        return self.fx

    @set_fx.setter
    def set_fx(self, fx):
        self.fx = fx

    __str__ = lambda self: f"(ваша функция: {self.fx})"

    functionofx = lambda self, a: self.f(a)

    diffx = lambda self, a: (self.f(a + 2 ** -32) - self.f(a)) / 2 ** -32

class Equation(Func):

    def __init__(self, fx: str, eps: float):
        super().__init__(fx)
        if eps != 0: self.eps = eps
        else: self.eps = 0.001
        self.lim = 0

    @property
    def set_eps(self):
        return self.eps

    @set_eps.setter
    def set_eps(self, eps):
        self.eps = eps

    def dichotomy(self, a: float, b: float):
        while (abs(b - a) > self.eps) and self.lim != 1000:
            c, self.lim = (a + b) / 2, self.lim + 1
            if self.f(b) * self.f(c) < 0: a = c
            else: b = c
        if abs(self.f((a + b) / 2)) > self.eps * 10:
            return f"На данном отрезке не было найдено решение {self.fx} = 0"
        else:
            return f"Ответ {self.fx} = 0 при x = {(a + b) / 2}"

    def secant(self, a: float):
        b = a + self.eps * 2
        while abs(b - a) > self.eps and self.lim != 1000:
            try: a, b, self.lim = b - (self.f(b) * (a - b) / (self.f(a) - self.f(b))), a, self.lim + 1
            except ZeroDivisionError: return f"Решение {self.fx} = 0 не найдено"
        if abs(self.f(a)) > self.eps * 10: return f"Решение {self.fx} = 0 не найдено"
        else: return f"Ответ {self.fx} = 0 при x = {a}"

    def Newton(self, a: float):
        b = a + self.eps * 2
        while abs(b - a) > self.eps and self.lim != 1000:
            try: a, b, self.lim = b - self.f(b) / Func(self.fx).diffx(b), a, self.lim + 1
            except ZeroDivisionError: return f"Решение {self.fx} = 0 не найдено"
        return f"Ответ {self.fx} = 0 при x = {b}"


Fx = re.sub(r"[a-zA-Zа-яА-Я]", 'x', input("Введите уравнение вида f(x) = 0: "))
Eq = Equation(Fx, abs(float(input("Введите точность: "))))
print("-" * 60)
method = input("Введите метод решения уравнения:\n1)Метод дихтомии\n2)Метод хорд\n3)Метод Ньютона\nМетод ")
print("-" * 60)
if method == "1" or method == "дихтомии" or method == "д" or method == "Дихтомии" or method == "Д" \
    or method == "1)":
    x1 = float(input(f"Введите левую границу отрезка, где искать корень уравнения {Eq}: "))
    x2 = float(input(f"Введите правую границу отрезка, где искать корень уравнения {Eq}: "))
    if x1 < x2: x1, x2 = x2, x1
    print("-" * 20 + "Метод дихтомии" + "-" * 20)
    print(Eq.dichotomy(x1, x2))

elif method == "2" or method == "хорд" or method == "х" or method == "Х" or method == "Хорд" or method == "2)":
    x0 = float(input(f"Введите начальную координату, с которой начинать искать корень уравнения, {Eq}: "))
    print("-" * 20 + "Метод хорд" + "-" * 20)
    print(Eq.secant(x0))

elif method == "3" or method == "Ньютона" or method == "Н" or method == "3)":
    x0 = float(input(f"Введите начальную координату, с которой начинать искать корень уравнения, {Eq}: "))
    print("-" * 20 + "Метод Ньютона" + "-" * 20)
    print(Eq.Newton(x0))

else:
    print("-" * 25 + "Метод дихтомии" + "-" * 25)
    x1 = float(input(f"Введите левую границу отрезка, где искать корень уравнения {Eq}: "))
    x2 = float(input(f"Введите правую границу отрезка, где искать корень уравнения {Eq}: "))
    if x1 < x2: x1, x2 = x2, x1
    print(Eq.dichotomy(x1, x2))
    print("-" * 25 + "Метод хорд" + "-" * 25)
    x0 = float(input(f"Введите начальную координату, с которой начинать искать корень уравнения, {Eq}: "))
    print(Eq.secant(x0))
    print("-" * 25 + "Метод Ньютона" + "-" * 25)
    x0 = float(input(f"Введите начальную координату, с которой начинать искать корень уравнения, {Eq}: "))
    print(Eq.Newton(x0))

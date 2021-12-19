import tkinter as tk
import re


class MatrixException(Exception):
    pass


class Matrices():  # Матрицы

    def __init__(self, n=1, m=1, matricA=(), matricB=()):
        self.m = m
        self.n = n
        self.matricA = matricA
        self.matricB = matricB

    @property
    def set_m(self):
        return self.m

    @set_m.setter
    def set_m(self, m):
        self.m = m

    @property
    def set_n(self):
        return self.n

    @set_n.setter
    def set_n(self, n):
        self.n = n

    @property
    def set_matricA(self):
        return self.matricA

    @set_matricA.setter
    def set_matricA(self, matricA):
        self.matricA = matricA

    @property
    def set_matricB(self):
        return self.matricB

    @set_matricB.setter
    def set_matricB(self, matricB):
        self.matricB = matricB

    @property
    def suma(self):
        matricC = []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                try:
                    matricC.append(self.matricA[i][j] + self.matricB[i][j])
                except IndexError:
                    return ' Введите равное количество столбцов и строчек в матрицах А и B '
        return matricC

    @suma.setter
    def suma(self, matricC):
        self.matricC = matricC

    @property
    def difference(self):
        matricC = []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                try:
                    matricC.append(self.matricA[i][j] - self.matricB[i][j])
                except IndexError:
                    return ' Введите равное количество столбцов и строчек в матрицах А и B '
        return matricC

    @difference.setter
    def difference(self, matricC):
        self.matricC = matricC


class SquareMatrices(Matrices):  # Квадрат
    pass


class RectangleMatrices(Matrices):  # Прямоугольник
    pass


class TriangleMatrices(Matrices):  # Над или под главной диагональю нули
    pass


class StringMatrices(Matrices):  # Строка
    pass


class ColumnMatrices(Matrices):  # Столбец
    pass


class UnitMatrices(Matrices):  # По диагонали единицы
    pass


class ZeroMatrices(Matrices):  # Все нули
    pass


class DiagonalMatrices(Matrices):  # По диагонали числа
    pass


C = Matrices(2, 2, [[2, 4], [332, 6]], [[3, 5], [1, 3]])


def suma():  # Сумма
    a, i, j = C.suma, 1, 0
    while i < len(a) and type(a) != str:
        if i / C.n == i // C.n:
            a.insert(i + j, '\n')
            j += 1
        i += 1
    res.set(str(a)[1:-1].replace(r"'\n'", '\n', str(a).find('\n')).replace(',', ' ', str(a).count(',')))


def difference():  # Разность
    a, i, j = C.difference, 1, 0
    while i < len(a) and type(a) != str:
        if i / C.n == i // C.n:
            a.insert(i + j, '\n')
            j += 1
        i += 1
    res.set(str(a)[1:-1].replace(r"'\n'", '\n', str(a).count(r"'\n'")).replace(',', ' ', str(a).count(',')))


# Окно
window = tk.Tk()
screen_width = str(window.winfo_screenwidth() // 2)
screen_height = str(window.winfo_screenheight() // 2)
window.title('Matrix')
window.geometry(screen_width + 'x' + screen_height + '+' +
                str(int(screen_width) // 2) + '+' + str(int(screen_height) // 2))
a = int(input('Введите шрифт текста: '))
k = ('Times New Roman', a)

# Ввод данных
frame0 = tk.LabelFrame(window, text='Ввод размерности матриц', font=k)
frame0.grid(row=0, column=0)
lbl0Am = tk.Label(master=frame0, font=k, text='Количество столбцов матрицы А:').pack()
Am = tk.IntVar()
ent0Am = tk.Spinbox(master=frame0, font=k, textvariable=Am, from_=1, to=float('inf')).pack()
lbl0An = tk.Label(master=frame0, font=k, text='Количество строк матрицы А:').pack()
An = tk.IntVar()
ent0An = tk.Spinbox(master=frame0, font=k, textvariable=An, from_=1, to=float('inf')).pack()
lbl0Bm = tk.Label(master=frame0, font=k, text='Количество столбцов матрицы B:').pack()
Bm = tk.IntVar()
ent0Bm = tk.Spinbox(master=frame0, font=k, textvariable=Bm, from_=0, to=float('inf')).pack()
lbl0Bn = tk.Label(master=frame0, font=k, text='Количество строк матрицы B:').pack()
Bn = tk.IntVar()
ent0Bn = tk.Spinbox(master=frame0, font=k, textvariable=Bn, from_=0, to=float('inf')).pack()
btn0 = tk.Button(master=frame0, font=k, text='Получить размерность матриц').pack()

# Кнопки вычислений
frame1 = tk.LabelFrame(window, text='Операция', font=k)
frame1.grid(row=1)
res = tk.StringVar()
btn1 = tk.Button(master=frame1, font=k, text='Сумма А и B', command=suma).pack()
btn2 = tk.Button(master=frame1, font=k, text='Разность А и В', command=difference).pack()
btn3 = tk.Button(master=frame1, font=k, text='Транспонирование А').pack()
btn4 = tk.Button(master=frame1, font=k, text='Умножение А и В').pack()
btn5 = tk.Button(master=frame1, font=k, text='След А').pack()
lbl1 = tk.Label(master=frame1, font=k, textvariable=res)
window.mainloop()

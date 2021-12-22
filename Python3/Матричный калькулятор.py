import tkinter as tk
from random import randint


def translate(lst):
    lst1, lstes = [], []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            try:
                lst1.append(int(lst[i][j].get()))
            except ValueError:
                lst1.append(0)
        lstes.append(lst1)
        lst1 = []
    return lstes


class MatrixException(Exception):
    pass


class Matrices():  # Матрицы

    def __init__(self, matricA, matricB=[[]]):
        self.matricA = matricA
        self.matricB = matricB
        self.mA = len(self.matricA)
        self.nA = len(self.matricA[0])
        self.nB = len(self.matricB[0])
        self.mB = len(self.matricB)

    @property
    def set_mA(self):
        return self.mA

    @set_mA.setter
    def set_mA(self, mA):
        self.mA = mA

    @property
    def set_nA(self):
        return self.nA

    @set_nA.setter
    def set_nA(self, nA):
        self.nA = nA

    @property
    def set_nB(self):
        return self.nB

    @set_nB.setter
    def set_nB(self, nB):
        self.nB = nB

    @property
    def set_mB(self):
        return self.mB

    @set_mB.setter
    def set_mB(self, mB):
        self.mB = mB

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

    def suma(self):  # Сумма матриц А и В
        matricCs, lstes = [], []
        if self.nA != self.nB or self.mA != self.mB:
            return ' Введите равное количество столбцов и строчек в матрицах А и B '
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                lstes.append(self.matricA[i][j] + self.matricB[i][j])
            matricCs.append(lstes)
            lstes = []
        return matricCs

    def difference(self):  # Разность матриц А и В
        matricCd, lstes = [], []
        if self.nA != self.nB or self.mA != self.mB:
            return ' Введите равное количество столбцов и строчек в матрицах А и B '
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                lstes.append(self.matricA[i][j] - self.matricB[i][j])
            matricCd.append(lstes)
            lstes = []
        return matricCd

    def transpA(self):  # Транспонирование матрицы А
        matricCt, lstes, i = [], [], 0
        for j in range(self.nA):
            for i in range(self.mA):
                lstes.append(self.matricA[i][j])
            matricCt.append(lstes)
            lstes = []
        return matricCt

    def mult(self):  # Умножение матриц А и В
        matricCm, lstes, lst = [], [], []
        if self.nA != self.mB:
            return ' Количество столбцов А должно равняться количеству строк В '
        for i in range(self.mA):
            for k in range(self.nB):
                for j in range(self.mB):
                    lst.append(self.matricA[i][j] * self.matricB[j][k])
                lstes.append(sum(lst))
                lst = []
            matricCm.append(lstes)
            lstes = []
        return matricCm


class SquareMatrices(Matrices):  # Квадрат

    def traceA(self):  # След матрицы А
        if self.nA != self.mA:
            return ' След матрицы можно вычислить только у квадратной матрицы '
        lst = []
        for i in range(len(self.matricA)):
            lst.append(self.matricA[i][i])
        trace = sum(lst)
        return trace

    def powerA(self, pow):  # Возведение в степень
        matricAp = self.matricA
        if self.nA != self.mA:
            return ' Возвести в степень можно только квадратную матрицу '
        for i in range(1, pow):
            matricCp = Matrices(matricAp, self.matricA)
            matricAp = matricCp.mult()
        return matricAp


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


# Окно
window = tk.Tk()
screen_width = str(int(window.winfo_screenwidth() // 1.5))
screen_height = str(int(window.winfo_screenheight() // 1.5))
window.title('Matrix')
window.geometry(screen_width + 'x' + screen_height + '+' +
                str(int(int(screen_width) * 1.5 // 5)) + '+' + str(int(int(screen_height) * 1.5 // 6)))

k = ('Times New Roman', int(window.winfo_screenwidth() // 130))

# Ввод данных
frm0 = tk.LabelFrame(window, text='Ввод размерности матриц', font=k)
frm0.grid(row=0, column=0)
lbl0Am = tk.Label(frm0, font=k, text='Количество строк матрицы А:').pack()
Am = tk.IntVar()
ent0Am = tk.Spinbox(frm0, font=k, textvariable=Am, from_=1, to=float('inf')).pack()
lbl0An = tk.Label(frm0, font=k, text='Количество столбцов матрицы А:').pack()
An = tk.IntVar()
ent0An = tk.Spinbox(frm0, font=k, textvariable=An, from_=1, to=float('inf')).pack()
lbl0Bm = tk.Label(frm0, font=k, text='Количество строк матрицы B:').pack()
Bm = tk.IntVar()
ent0Bm = tk.Spinbox(frm0, font=k, textvariable=Bm, from_=0, to=float('inf')).pack()
lbl0Bn = tk.Label(frm0, font=k, text='Количество столбцов матрицы B:').pack()
Bn = tk.IntVar()
ent0Bn = tk.Spinbox(frm0, font=k, textvariable=Bn, from_=0, to=float('inf')).pack()
power = tk.IntVar()


# Матрица А и B
def show1():  # Показать
    frm2 = tk.LabelFrame(window, text='Матрица А', font=k)
    frm2.grid(row=0, column=1, padx=k[1])
    frm3 = tk.LabelFrame(window, text='Матрица В', font=k)
    frm3.grid(row=0, column=2, padx=k[1])
    global entrs1, entrs2, entrsA, entrsB, frms
    entrs1, entrs2, entrsA, entrsB = [], [], [], []

    for i in range(Am.get()):
        for j in range(An.get()):
            ent1 = tk.Entry(frm2, font=k, width=4)
            ent1.grid(row=i+1, column=j+1)
            entrs1.append(ent1)
        entrsA.append(entrs1)
        entrs1 = []
    if Bn.get() != 0 and Bm.get() != 0:
        for i in range(Bm.get()):
            for j in range(Bn.get()):
                ent2 = tk.Entry(frm3, font=k, width=4)
                ent2.grid(row=i+1, column=j+1)
                entrs2.append(ent2)
            entrsB.append(entrs2)
            entrs2 = []
    else:
        lbl2 = tk.Label(frm3, text='Введите количество строк и количество столбцов\nв матрице В больше 0', font=k)
        lbl2.grid()
    btn0b.pack(fill=tk.X)
    btn0a.destroy()
    frms = [frm2, frm3]


def show2():  # Показать
    for i in frms:
        i.destroy()
    for i in range(len(entrsB)):
        for j in range(len(entrsB[i])):
            entrsB[i][j].destroy()
    for i in range(len(entrsA)):
        for j in range(len(entrsA[i])):
            entrsA[i][j].destroy()
    return show1()


def suma():  # Сумма
    try:
        C = Matrices(translate(entrsA), translate(entrsB))
        a = C.suma()
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(',', ' ', str(a).count(',')). \
                replace(']', '', str(a).count(']')).replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def difference():  # Разность
    try:
        C = Matrices(translate(entrsA), translate(entrsB))
        a = C.difference()
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).\
                replace(']', '', str(a).count(']')).replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def transpA():  # Транспонирование
    try:
        C = Matrices(translate(entrsA))
        a = C.transpA()
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')).\
                replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def traceA():  # След
    try:
        C = SquareMatrices(translate(entrsA))
        a = C.traceA()
        if a != 'След матрицы можно вычислить только у квадратной матрицы':
            res.set('След матрицы А = ' + str(a))
        else:
            res.set(str(a))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def mult():  # Умножение А и В
    try:
        C = Matrices(translate(entrsA), translate(entrsB))
        a = C.mult()
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')).\
            replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def powerA():  # Возведение в степень
    try:
        C = SquareMatrices(translate(entrsA))
        a = C.powerA(power.get())
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')). \
            replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def rnd():  # Случайные значения в ячейках матриц
    try:
        for i in range(len(entrsA)):
            for j in range(len(entrsA[i])): entrsA[i][j].delete(0, 'end')
        for i in range(len(entrsB)):
            for j in range(len(entrsB[i])): entrsB[i][j].delete(0, 'end')
        for i in range(len(entrsA)):
            for j in range(len(entrsA[i])): entrsA[i][j].insert(0, str(randint(-99, 99)))
        for i in range(len(entrsB)):
            for j in range(len(entrsB[i])): entrsB[i][j].insert(0, str(randint(-99, 99)))
    except NameError:
        res.set('Введите размерность матриц')


btnr = tk.Button(frm0, font=k, text='Случайные значения в ячейках матрицы', command=rnd).pack(fill=tk.X)
btn0a = tk.Button(frm0, font=k, text='Получить размерность матриц', command=show1)
btn0a.pack(fill=tk.X)
btn0b = tk.Button(frm0, font=k, text='Получить размерность матриц', command=show2)

# Кнопки вычислений
frm1 = tk.LabelFrame(window, text='Операция', font=k)
frm1.grid(row=1)
res = tk.StringVar()
btn1 = tk.Button(frm1, font=k, text='Сумма А и B', command=suma).pack(fill=tk.X)
btn2 = tk.Button(frm1, font=k, text='Разность А и В', command=difference).pack(fill=tk.X)
btn3 = tk.Button(frm1, font=k, text='Умножение А и В', command=mult).pack(fill=tk.X)
btn4 = tk.Button(frm1, font=k, text='Транспонирование А', command=transpA).pack(fill=tk.X)
btn5 = tk.Button(frm1, font=k, text='След А', command=traceA).pack(fill=tk.X)
btn6 = tk.Button(frm1, font=k, text='Возведение А в степень', command=powerA).pack(fill=tk.X)
ent1 = tk.Spinbox(frm1, font=k, textvariable=power, from_=2, to=float('inf'), width=3).pack()
btn7 = tk.Button(frm1, font=k, text='Выйти из программы', command=window.destroy).pack(fill=tk.X, pady=k[1]+2)
frm4 = tk.LabelFrame(window, font=k, text='Ответ')
frm4.grid(row=1, column=1, columnspan=5)
lbl1 = tk.Label(frm4, font=k, textvariable=res).grid(row=0, column=0)
window.mainloop()

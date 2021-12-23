import tkinter as tk
from random import randint
import re
from decimal import Decimal, getcontext
getcontext().prec = 5


class Calc:

    # Сумма строк из списка
    @classmethod
    def summ(self, lst):
        k = ''
        for i in lst:
            k += i
        return k

    # Скобки в примере
    @classmethod
    def changing(self, out):
        return re.search(r'[(][\d+/^*-.,]+[)]', out).start() + 1, re.search(r'[(][\d+/^*-.,]+[)]', out).end() - 1

    # Превращение "Число + Число" и "Число - Число" в "+" и "-" соответственно
    @classmethod
    def num_op2op(self, lst):
        p = r'\d*[.,]?\d+|[+-]\('
        for i in range(len(lst)):
            k = lst[i]
            if not (re.search(p, k) is None):
                k = re.sub(p, r'', k)
                lst.pop(i)
                lst.insert(i, k)
        return lst

    # Перебор полученных чисел
    @classmethod
    def str2Decimal(self, lst):
        k = []
        for i in lst:
            try:
                k.append(Decimal(i))
            except ValueError:
                return 0
        return k

    # Перебор операторов в списке
    @classmethod
    def equal(self, n):
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
    @classmethod
    def operator2act(self, lst, lstnum):
        ans = 0
        while len(lstnum) != 1:
            act = Calc.equal(lst)
            if lst[act] == '/':
                try:
                    ans = lstnum[act] / lstnum[act + 1]
                except ZeroDivisionError:
                    return 0
            elif lst[act] == '*':
                ans = lstnum[act] * lstnum[act + 1]
            elif lst[act] == '^':
                if lstnum[act] == 0 and lstnum[act + 1] == 0:
                    return 0
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
    def calc(self, given):
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
        out = Calc.summ(out_lst)

        # Проверка, того что нашлось из вводных данных по регулярным выражениям с вводными данными и прочее
        if given == '':
            return 0
        elif havenums is None:
            return 0
        elif not (re.search(re_oper, given) is None):
            return 0
        elif not (re.match(r'[*/^]', given) is None) or not (re.search(r'[-+*/^]$', given, re.MULTILINE) is None) or \
                not (re.search(r'\([*/^]', given) is None) or not (re.search(r'[-+*/^]\)', given) is None):
            return 0
        elif given.count('(') > given.count(')') + 1 or given.count(')') > given.count('('):
            return 0
        elif '()' in given or '()' in given + ')':
            return 0
        elif out != given:
            return 0

        # Добавить ")", если кол-во "(" == кол-ву ")" - 1
        if given.count('(') == given.count(')') + 1:
            out += ')'

        out = '(' + out + ')'  # Сам пример - огромная скобка

        # Вычисления внутри скобок
        j = 0
        while '(' in out:
            j = j + 1
            st, end = Calc.changing(out)

            if not (re.search(r'[\d.,]\(', out[st - 2:st]) is None):
                out = out[0:st - 1] + '*(' + out[st:]
                st, end = Calc.changing(out)
            if not (re.search(r'\)[\d.,]', out[end:end + 2]) is None):
                out = out[0:end] + ')*' + out[end + 1:]
                st, end = Calc.changing(out)

            change = out[st:end].replace('--', '+', out[st:end].count('--'))
            lstnums, lstoperators = re.findall(re_nums, change), Calc.num_op2op(re.findall(re_operators, change))
            lstnums = Calc.str2Decimal(lstnums)

            if len(lstnums) == 1:
                change = lstnums[0]
            else:
                change = Calc.operator2act(lstoperators, lstnums)
            out = out[0:st - 1] + str(change) + out[end + 1:]
        return Decimal(out)


def translate(lst):
    lst1, lstes = [], []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst1.append(Calc().calc(lst[i][j].get()))
        lstes.append(lst1)
        lst1 = []
    return lstes


class MatrixException(Exception):
    pass


class Matrices:  # Матрицы

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
        if self.nA != self.nB or self.mA != self.mB:
            return ' Введите равное количество столбцов и строчек в матрицах А и B '
        matricCs, lstes = [], []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                lstes.append(self.matricA[i][j] + self.matricB[i][j])
            matricCs.append(lstes)
            lstes = []
        return matricCs

    def difference(self):  # Разность матриц А и В
        if self.nA != self.nB or self.mA != self.mB:
            return ' Введите равное количество столбцов и строчек в матрицах А и B '
        matricCd, lstes = [], []
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
        if self.nA != self.mB:
            return ' Количество столбцов А должно равняться количеству строк В '
        matricCm, lstes, lst = [], [], []
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
            return 'След матрицы можно вычислить только у квадратной матрицы'
        lst = []
        for i in range(len(self.matricA)):
            lst.append(self.matricA[i][i])
        trace = sum(lst)
        return trace

    def powerA(self, pow):  # Возведение в степень
        if self.nA != self.mA:
            return ' Возвести в степень можно только квадратную матрицу '
        matricAp = self.matricA
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
        a = re.sub(r"Decimal\('|'\)", '', str(C.suma()))
        res.set(a[1:-1].replace(r"], ", '\n', a.count(r"], ")).\
                replace(']', '', a.count(']')).replace('[', '', a.count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def difference():  # Разность
    try:
        C = Matrices(translate(entrsA), translate(entrsB))
        a = re.sub(r"Decimal\('|'\)", '', str(C.difference()))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).\
                replace(']', '', str(a).count(']')).replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def transpA():  # Транспонирование
    try:
        C = Matrices(translate(entrsA))
        a = re.sub(r"Decimal\('|'\)", '', str(C.transpA()))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')).\
                replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def traceA():  # След
    try:
        C = SquareMatrices(translate(entrsA))
        a = re.sub(r"Decimal\('|'\)", '', str(C.traceA()))
        if a != 'След матрицы можно вычислить только у квадратной матрицы':
            res.set('След матрицы А = ' + str(a))
        else:
            res.set(str(a))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def mult():  # Умножение А и В
    try:
        C = Matrices(translate(entrsA), translate(entrsB))
        a = re.sub(r"Decimal\('|'\)", '', str(C.mult()))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')).\
            replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def powerA():  # Возведение в степень
    try:
        C = SquareMatrices(translate(entrsA))
        a = re.sub(r"Decimal\('|'\)", '', str(C.powerA(power.get())))
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
frm4.grid(row=1, column=1, columnspan=2)
lbl1 = tk.Label(frm4, font=k, textvariable=res).grid(row=0, column=0)
window.mainloop()

import tkinter as tk
from random import randint
import re
from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 16


class Calc:

    def __init__(self, given):
        self.given = given

    # Основная функция
    def calc(self):
        # Ввод данных
        given = self.given.replace(' ', '', self.given.count(' '))

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
        elif out != given:
            return 0
        elif havenums is None:
            return 0
        elif not (re.search(re_oper, given) is None):
            return 0
        elif given.count('(') > given.count(')') + 1 or given.count(')') > given.count('('):
            return 0
        elif '()' in given or '()' in given + ')':
            return 0
        elif not (re.match(r'[*/^]', given) is None) or not (re.search(r'[-+*/^]$', given, re.MULTILINE) is None) or \
                not (re.search(r'\([*/^]', given) is None) or not (re.search(r'[-+*/^]\)', given) is None):
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

    # Сумма строк из списка
    @classmethod
    def summ(cls, lst):
        ks = ''
        for i in lst:
            ks += i
        return ks

    # Скобки в примере
    @classmethod
    def changing(cls, out):
        return re.search(r'[(][\d+/^*-.,]+[)]', out).start() + 1, re.search(r'[(][\d+/^*-.,]+[)]', out).end() - 1

    # Превращение "Число + Число" и "Число - Число" в "+" и "-" соответственно
    @classmethod
    def num_op2op(cls, lst):
        p = r'\d*[.,]?\d+|[+-]\('
        for i in range(len(lst)):
            kd = lst[i]
            if not (re.search(p, kd) is None):
                kd = re.sub(p, r'', kd)
                lst.pop(i)
                lst.insert(i, kd)
        return lst

    # Перебор полученных чисел
    @classmethod
    def str2Decimal(cls, lst):
        lk = []
        for i in lst:
            try:
                lk.append(Decimal(i))
            except ValueError:
                return 0
        return lk

    # Перебор операторов в списке
    @classmethod
    def equal(cls, n):
        try:
            a1 = n.index('/')
        except ValueError:
            a1 = float('inf')
        try:
            a2 = n.index('*')
        except ValueError:
            a2 = float('inf')
        try:
            a3 = n.index('^')
        except ValueError:
            a3 = float('inf')
        if a1 == float('inf') and a2 == float('inf') and a3 == float('inf'):
            try:
                a4 = n.index('+')
            except ValueError:
                a4 = float('inf')
            try:
                a5 = n.index('-')
            except ValueError:
                a5 = float('inf')
            return min([a4, a5])
        else:
            return min([a1, a2, a3])

    # Перебор полученных операторов
    @classmethod
    def operator2act(cls, lst, lstnum):
        ans = 0
        while len(lstnum) != 1:
            act = Calc.equal(lst)
            if lst[act] == '/':
                try:
                    ans = lstnum[act] / lstnum[act + 1]
                except (ZeroDivisionError, InvalidOperation):
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


def translate(lst):
    lst1, lstes = [], []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst1.append(Calc(lst[i][j].get()).calc())
        lstes.append(lst1)
        lst1 = []
    return lstes


class MatrixException(Exception):
    pass


class Matrices:  # Матрицы

    def __init__(self, matricA):
        self.matricA = matricA
        self.mA = len(self.matricA)
        self.nA = len(self.matricA[0])

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
    def set_matricA(self):
        return self.matricA

    @set_matricA.setter
    def set_matricA(self, matricA):
        self.matricA = matricA

    def __add__(self, matricB):  # Сумма матриц А и В
        nB = len(matricB[0])
        mB = len(matricB)
        if self.nA != nB or self.mA != mB:
            return ' Введите равное количество столбцов и строчек в матрицах А и B '
        matricCa, lstes = [], []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                print(f'Суммирую {i + 1} строку {j + 1} столбец матриц: {self.matricA[i][j]} + {matricB[i][j]}')
                lstes.append(self.matricA[i][j] + matricB[i][j])
            matricCa.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return matricCa

    def __sub__(self, matricB):  # Разность матриц А и В
        nB = len(matricB[0])
        mB = len(matricB)
        if self.nA != nB or self.mA != mB:
            return ' Введите равное количество столбцов и строчек в матрицах А и B '
        matricCs, lstes = [], []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                print(f'Вычитаю {i + 1} строку {j + 1} столбец матриц: {self.matricA[i][j]} - {matricB[i][j]}')
                lstes.append(self.matricA[i][j] - matricB[i][j])
            matricCs.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return matricCs

    def transpA(self):  # Транспонирование матрицы А
        matricCt, lstes = [], []
        for j in range(self.nA):
            for i in range(self.mA):
                print(f'Меняю {i + 1} строка с {j + 1} столбец')
                lstes.append(self.matricA[i][j])
            matricCt.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return matricCt

    def __mul__(self, matricB):  # Умножение матриц А и В
        try:
            nB = len(matricB[0])
            mB = len(matricB)
        except (TypeError, InvalidOperation):
            matricCmn = []
            for i in self.matricA:
                print(f'Умножаю:', list(map(lambda t: str(t), i)),
                      'cтроку на число')
                matricCmn.append(list(map(lambda x: x * matricB, i)))
            print('--------------------------------------------------------------------------------------')
            return matricCmn
        if self.nA != mB:
            return ' Количество столбцов А должно равняться количеству строк В '
        matricCm, lstes, lst = [], [], []
        for i in range(self.mA):
            for m in range(nB):
                for j in range(mB):
                    print(f'Умножаю {i + 1} строка {j + 1} столбец с {j + 1} строкой и {m + 1} столбцом'
                          f' матриц: {self.matricA[i][j]} * {matricB[j][m]}')
                    lst.append(self.matricA[i][j] * matricB[j][m])
                lstes.append(sum(lst))
                lst = []
            matricCm.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return matricCm


class SquareMatrices(Matrices):  # Квадрат

    def traceA(self):  # След матрицы А
        if self.nA != self.mA:
            return 'След матрицы можно вычислить только у квадратной матрицы'
        lst = []
        for i in range(len(self.matricA)):
            print(f'Суммирую {i + 1} c {sum(lst)} диагональный элемент матрицы')
            lst.append(self.matricA[i][i])
        print('--------------------------------------------------------------------------------------')
        trace = sum(lst)
        return trace

    def __pow__(self, powm, modulo=None):  # Возведение в степень матрицы А
        if self.nA != self.mA and powm != 1:
            return ' Возвести в степень можно только квадратную матрицу '
        matricAp = self.matricA
        for i in range(1, powm):
            matricCp = Matrices(matricAp)
            matricAp = matricCp * self.matricA
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
num = tk.DoubleVar()


# Матрица А и B
# noinspection PyGlobalUndefined
def show1():  # Показать
    frm2 = tk.LabelFrame(window, text='Матрица А', font=k)
    frm2.grid(row=0, column=1, padx=k[1])
    frm3 = tk.LabelFrame(window, text='Матрица В', font=k)
    frm3.grid(row=0, column=2, padx=k[1])
    global entrs1, entrs2, entrsA, entrsB, frms
    entrs1, entrs2, entrsA, entrsB = [], [], [], []

    for i in range(Am.get()):
        for j in range(An.get()):
            ent1d = tk.Entry(frm2, font=k, width=4)
            ent1d.grid(row=i + 1, column=j + 1)
            entrs1.append(ent1d)
        entrsA.append(entrs1)
        entrs1 = []
    if Bn.get() != 0 and Bm.get() != 0:
        for i in range(Bm.get()):
            for j in range(Bn.get()):
                ent2 = tk.Entry(frm3, font=k, width=4)
                ent2.grid(row=i + 1, column=j + 1)
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


def add():  # Сумма
    try:
        C = Matrices(translate(entrsA)) + (translate(entrsB))
        a = re.sub(r"Decimal\('|'\)", '', str(C))
        res.set(a[1:-1].replace(r"], ", '\n', a.count(r"], ")). \
                replace(']', '', a.count(']')).replace('[', '', a.count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def difference():  # Разность
    try:
        C = Matrices(translate(entrsA)) - translate(entrsB)
        a = re.sub(r"Decimal\('|'\)", '', str(C))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")). \
                replace(']', '', str(a).count(']')).replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def transpA():  # Транспонирование
    try:
        C = Matrices(translate(entrsA))
        a = re.sub(r"Decimal\('|'\)", '', str(C.transpA()))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')). \
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
        C = Matrices(translate(entrsA)) * translate(entrsB)
        a = re.sub(r"Decimal\('|'\)", '', str(C))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')). \
                replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def multnum():
    try:
        # noinspection PyTypeChecker
        C = Matrices(translate(entrsA)) * Decimal(num.get())
        a = re.sub(r"Decimal\('|'\)", '', str(C))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')). \
                replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def powerA():  # Возведение в степень
    try:
        a = re.sub(r"Decimal\('|'\)", '', str(SquareMatrices(translate(entrsA)) ** power.get()))
        res.set(str(a)[1:-1].replace(r"], ", '\n', str(a).count(r"], ")).replace(']', '', str(a).count(']')). \
                replace('[', '', str(a).count('[')))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def rnd():  # Случайные значения в ячейках матриц
    try:
        for i in range(len(entrsA)):
            for j in range(len(entrsA[i])):
                entrsA[i][j].delete(0, 'end')
        for i in range(len(entrsB)):
            for j in range(len(entrsB[i])):
                entrsB[i][j].delete(0, 'end')
        for i in range(len(entrsA)):
            for j in range(len(entrsA[i])):
                entrsA[i][j].insert(0, str(randint(-99, 99)))
        for i in range(len(entrsB)):
            for j in range(len(entrsB[i])):
                entrsB[i][j].insert(0, str(randint(-99, 99)))
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
btn1 = tk.Button(frm1, font=k, text='А + В', command=add, width=k[1] + 1).grid()
btn2 = tk.Button(frm1, font=k, text='А - В', command=difference, width=k[1] + 1).grid(column=1, row=0)
btn3 = tk.Button(frm1, font=k, text='А * В', command=mult, width=k[1] + 1).grid(column=2, row=0)
btn4 = tk.Button(frm1, font=k, text='Трансп. А', command=transpA, width=k[1] + 1).grid(row=1)
btn5 = tk.Button(frm1, font=k, text='След А', command=traceA, width=k[1] + 1).grid(row=1, column=1)
btn6 = tk.Button(frm1, font=k, text='А ^ степень       ', command=powerA, width=k[1] + 1).grid(row=1, column=2)
ent1 = tk.Spinbox(frm1, font=k, textvariable=power, from_=1, to=float('inf'), width=2).grid(row=1, column=2, sticky='e')
btn7 = tk.Button(frm1, font=k, text='A * число    ', command=multnum, width=k[1] + 1).grid(row=2)
ent2 = tk.Spinbox(frm1, font=k, textvariable=num, from_=-float('inf'), to=float('inf'), width=2) \
    .grid(row=2, column=0, sticky='e')
btn8 = tk.Button(frm1, font=k, text='Выйти из программы', command=window.destroy, width=k[1] + 5)
btn8.grid(row=2, column=1, pady=k[1] + 2, columnspan=2)
frm4 = tk.LabelFrame(window, font=k, text='Ответ')
frm4.grid(row=1, column=1, columnspan=1, sticky='s')
lbl1 = tk.Label(frm4, font=k, textvariable=res).pack()
print('-------------Начало работы-------------')
window.mainloop()
print('-------------Конец работы-------------')

import tkinter as tk
from random import randint
import re
from decimal import Decimal, getcontext, InvalidOperation
from fractions import Fraction

# Точность чисел класса Decimal и шрифт текста
getcontext().prec = 6
k = ('Times New Roman', 11)


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
    @staticmethod
    def summ(lst):
        ks = ''
        for i in lst:
            ks += i
        return ks

    # Скобки в примере
    @staticmethod
    def changing(out):
        return re.search(r'[(][\d+/^*-.,]+[)]', out).start() + 1, re.search(r'[(][\d+/^*-.,]+[)]', out).end() - 1

    # Превращение "Число + Число" и "Число - Число" в "+" и "-" соответственно
    @staticmethod
    def num_op2op(lst):
        p = r'\d*[.,]?\d+|[+-]\('
        for i in range(len(lst)):
            kd = lst[i]
            if not (re.search(p, kd) is None):
                kd = re.sub(p, r'', kd)
                lst.pop(i)
                lst.insert(i, kd)
        return lst

    # Перебор полученных чисел
    @staticmethod
    def str2Decimal(lst):
        lk = []
        for i in lst:
            try:
                lk.append(Decimal(i))
            except ValueError:
                return 0
        return lk

    # Перебор операторов в списке
    @staticmethod
    def equal(n):
        try:a1 = n.index('/')
        except ValueError:a1 = float('inf')
        try:a2 = n.index('*')
        except ValueError:a2 = float('inf')
        try:a3 = n.index('^')
        except ValueError:a3 = float('inf')
        if a1 == float('inf') and a2 == float('inf') and a3 == float('inf'):
            try:a4 = n.index('+')
            except ValueError:a4 = float('inf')
            try:a5 = n.index('-')
            except ValueError:a5 = float('inf')
            return min([a4, a5])
        else:
            return min([a1, a2, a3])

    # Перебор полученных операторов
    @staticmethod
    def operator2act(lst, lstnum):
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


def translate(lst):  # Перевод значений ячеек в числа
    if typenum == 'Decimal':
        lst1, lstes = [], []
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                lst1.append(Calc(lst[i][j].get()).calc())
            lstes.append(lst1)
            lst1 = []
        return lstes
    elif typenum == 'Fraction':
        lst1, lstes = [], []
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                try:
                    lst1.append(Fraction(lst[i][j].get()))
                except ValueError:
                    lst1.append(0)
            lstes.append(lst1)
            lst1 = []
        return lstes
    elif typenum == 'float':
        lst1, lstes = [], []
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                try:
                    lst1.append(float(lst[i][j].get()))
                except ValueError:
                    lst1.append(0)
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
        self.__ans = []

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
        try:
            nB = len(matricB[0])
        except TypeError:
            return 'Введите сумму матриц ([[]])'
        mB = len(matricB)
        if self.nA != nB or self.mA != mB:
            return ' Введите равное количество столбцов\nи строчек в матрицах А и B '
        lstes = []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                print(f'Суммирую {i + 1} строку {j + 1} столбец матриц: {self.matricA[i][j]} + {matricB[i][j]}')
                lstes.append(self.matricA[i][j] + matricB[i][j])
            self.__ans.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return Matrices(self.__ans)

    def __sub__(self, matricB):  # Разность матриц А и В
        try:
            nB = len(matricB[0])
        except TypeError:
            return 'Введите разность матриц ([[]])'
        mB = len(matricB)
        if self.nA != nB or self.mA != mB:
            return ' Введите равное количество столбцов\nи строчек в матрицах А и B '
        lstes = []
        for i in range(len(self.matricA)):
            for j in range(len(self.matricA[i])):
                print(f'Вычитаю {i + 1} строку {j + 1} столбец матриц: {self.matricA[i][j]} - {matricB[i][j]}')
                lstes.append(self.matricA[i][j] - matricB[i][j])
            self.__ans.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return self.__ans

    def transpA(self):  # Транспонирование матрицы А
        matricCt, lstes = [], []
        for j in range(self.nA):
            for i in range(self.mA):
                print(f'Меняю {i + 1} строка и {j + 1} столбец на {j + 1} строку и {i + 1} столбец')
                lstes.append(self.matricA[i][j])
            self.__ans.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return self.__ans

    def __mul__(self, matricB):  # Умножение матриц А и В
        try:
            nB = len(matricB[0])
            mB = len(matricB)
        except TypeError:
            for i in self.matricA:
                print(f'Умножаю:', list(map(lambda t: str(t), i)), 'cтроку на число')
                self.__ans.append(list(map(lambda x: x * matricB, i)))
            print('--------------------------------------------------------------------------------------')
            return self.__ans
        if self.nA != mB:
            return ' Количество столбцов А должно\nравняться количеству строк В '
        lstes, lst = [], []
        for i in range(self.mA):
            for m in range(nB):
                for j in range(mB):
                    print(f'Умножаю {i + 1} строка {j + 1} столбец с {j + 1} строкой и {m + 1} столбцом'
                          f' матриц: {self.matricA[i][j]} * {matricB[j][m]}')
                    lst.append(self.matricA[i][j] * matricB[j][m])
                lstes.append(sum(lst))
                lst = []
            self.__ans.append(lstes)
            lstes = []
        print('--------------------------------------------------------------------------------------')
        return self.__ans

    def __str__(self):  # Работает только с __add__
        return str(self.matricA)  # [1:-1].replace(r"], ", '\n', str(self.matricA).count(r"], ")) \
        #         .replace(']', '', str(self.matricA).count(']')).replace('[', '', str(self.matricA).count('[')) \
        #         .replace(',', ';  ', str(self.matricA).count(','))  # Убрано, чтобы работали числа типа Fraction.


class SquareMatrices(Matrices):  # Квадрат

    from copy import deepcopy

    # def __init__(self, matricA):
    #     super().__init__(matricA)
    #     if self.nA != self.mA:
    #         raise MatrixException('Введите равное количество стобцов и строчек в матрице')

    def traceA(self):  # След матрицы А
        if self.nA != self.mA:
            return 'След матрицы можно вычислить\nтолько у квадратной матрицы'
        lst = []
        for i in range(len(self.matricA)):
            print(f'Суммирую c {sum(lst)} - {i + 1} ({self.matricA[i][i]}) диагональный элемент матрицы')
            lst.append(self.matricA[i][i])
        print('--------------------------------------------------------------------------------------')
        self.__ans = sum(lst)
        return self.__ans

    def __pow__(self, powm, modulo=None):  # Возведение в степень матрицы А
        if powm == 0:
            return UnitMatrices(self.matricA).toUnit()
        if self.nA != self.mA and powm != 1:
            return ' Возвести в степень можно\nтолько квадратную матрицу '
        if powm < 0:
            cop, powm = SquareMatrices(self.matricA).invertA(), abs(powm)
            self.matricA = SquareMatrices.deepcopy(cop)
            del cop
        self.__ans = self.matricA
        for i in range(1, powm):
            self.__ans = SquareMatrices(self.__ans) * self.matricA
        return self.__ans

    def detA(self):  # Определитель матрицы через треугольный вид матрицы А
        if self.nA != self.mA:
            return 'Вычислить определитель можно\nтолько у квадратной матрицы'
        self.__ans = 1
        self.matricA = TriangleMatrices(self.matricA).triangulationAU()
        print('-----------Вычисляю определитель матрицы-----------')
        for i in range(self.nA):
            self.__ans *= self.matricA[i][i]
        return self.__ans

    @staticmethod
    def minor_a(matricA, pop_i, pop_j):  # Минор элемента матрицы
        if pop_i <= 0 or pop_j <= 0:
            return 'Введите номер строки\nи номер столбца больше нуля'
        print(f'-----------Вычисляю минор {pop_i} строки {pop_j} столбца-----------')
        ansm = []
        for i in range(len(matricA)):
            d = matricA[i]
            if i != pop_i - 1:
                d.pop(pop_j - 1)
                ansm.append(d)
        print(f'---------Минор {pop_i} строки {pop_j} столбца:', Matrices(ansm) * (-1) ** (pop_j + pop_i), '---------')
        return Matrices(ansm) * (-1) ** (pop_j + pop_i)

    def invertA(self):  # Обратный вид матрицы (путает + и - в матрицах nxn, при нечетных n)
        if self.nA != self.mA:
            return ' Возвести в степень можно\nтолько квадратную матрицу '
        if self.nA == 1:
            return [[self.matricA[0][0] ** (-1)]]
        copym, lst = SquareMatrices.deepcopy(self.matricA), []
        try:
            det, ans = SquareMatrices(self.matricA).detA() ** (-1), []
        except ZeroDivisionError:
            return ' Определитель равен нулю\nобратной матрицы не существует '
        if det == float('inf'):
            return ' Определитель равен нулю\nобратной матрицы не существует '
        print('Определитель матрицы больше нуля. Считаю матрицу алгебраических дополнений')
        for i in range(self.nA):
            for j in range(self.nA):
                self.matricA = SquareMatrices.deepcopy(copym)
                mnr_a = SquareMatrices.minor_a(self.matricA, i + 1, j + 1)
                lst.append(SquareMatrices(mnr_a).detA())
            ans.append(lst)
            lst = []
        ans = Matrices(Matrices(ans).transpA()) * det
        return ans


class TriangleMatrices(Matrices):  # Над или под главной диагональю нули

    def triangulationAU(self):  # Триангуляция матрицы А под главной диагональю нули
        print('-----------Привожу матрицу к ступенчатому виду-----------')
        for i in range(self.mA):  # Если 1 стр, 1 ст = 0, то поменяет местами строки
            if self.matricA[i][0] != 0:
                self.matricA[0], self.matricA[i] = self.matricA[i], self.matricA[0]
                break
        for i in range(self.mA):  # Для матриц с несколькими нулевыми строками не работает
            if self.matricA[i] == [0] * self.nA:
                print(f'Меняю местами {i + 1} строку с {self.mA} строкой')
                self.matricA[i], self.matricA[self.mA - 1] = self.matricA[self.mA - 1], self.matricA[i]
        for i in range(self.nA):
            m = i
            for j in range(i + 1, self.mA + 1):
                try:
                    while self.matricA[i][m] == 0:
                        m += 1
                    self.matricA[j] = (Matrices([self.matricA[j]]) - (Matrices([self.matricA[i]]) *
                                                                      (self.matricA[j][m] / self.matricA[i][m])))[0]
                except IndexError:
                    print(f'Пропускаю {i + 1} строку {j} столбец')
        print('-----------Матрица приведена к ступенчатому виду-----------')
        self.__ans = self.matricA
        return self.__ans


class RectangleMatrices(Matrices):  # Прямоугольник
    pass


class StringMatrices(Matrices):  # Строка
    pass


class ColumnMatrices(Matrices):  # Столбец
    pass


class UnitMatrices(SquareMatrices):  # По диагонали единицы

    def toUnit(self):  # При возведении матрицы в степень 0
        self.__ans = [[0] * max(self.nA, self.mA)] * max(self.nA, self.mA)
        print('-----------Привожу матрицу к единичной-----------')
        for i in range(len(self.__ans)):
            self.__ans[i] = [0] * i + [1] + [0] * (max(self.nA, self.mA) - i - 1)
        print('--------------------------------------------------------------------------------------')
        return self.__ans


class DiagonalMatrices(UnitMatrices):  # По диагонали числа
    pass


class ZeroMatrices(DiagonalMatrices, TriangleMatrices):  # Все нули

    def __init__(self, nA, mA):
        super().__init__([[0] * nA] * mA)


# Окно ----------------------------------------------------------------------------------------------------------------
window = tk.Tk()
screen_width = str(int(window.winfo_screenwidth() // 1.5))
screen_height = str(int(window.winfo_screenheight() // 1.5))
window.title('Matrix')
window.geometry(screen_width + 'x' + screen_height + '+' +
                str(int(int(screen_width) * 1.5 // 5)) + '+' + str(int(int(screen_height) * 1.5 // 6)))


# Ввод данных
typenum = 'Decimal'
frm0 = tk.LabelFrame(window, text='Ввод размерности матриц', font=k)
frm0.pack(side='top', anchor='nw')
lbl0Am = tk.Label(frm0, font=k, text='Количество строк матрицы А:').pack()
Am = tk.IntVar()
ent0Am = tk.Spinbox(frm0, font=k, textvariable=Am, from_=1, to=11).pack()
lbl0An = tk.Label(frm0, font=k, text='Количество столбцов матрицы А:').pack()
An = tk.IntVar()
ent0An = tk.Spinbox(frm0, font=k, textvariable=An, from_=1, to=float('inf')).pack()
lbl0Bm = tk.Label(frm0, font=k, text='Количество строк матрицы B:').pack()
Bm = tk.IntVar()
ent0Bm = tk.Spinbox(frm0, font=k, textvariable=Bm, from_=1, to=11).pack()
lbl0Bn = tk.Label(frm0, font=k, text='Количество столбцов матрицы B:').pack()
Bn = tk.IntVar()
ent0Bn = tk.Spinbox(frm0, font=k, textvariable=Bn, from_=1, to=float('inf')).pack()
power = tk.IntVar()
num = tk.DoubleVar()


# Матрица А и B
# noinspection PyGlobalUndefined
def show1():  # Показать
    frm2 = tk.LabelFrame(window, text='Матрица А', font=k)
    frm2.place(x=frm0.winfo_width())
    frm3 = tk.LabelFrame(window, text='Матрица В', font=k)
    frm3.place(x=frm0.winfo_width() + An.get() * (3 * k[1]) + k[1] + 40)
    global entrs1, entrs2, entrsA, entrsB, frms
    entrs1, entrs2, entrsA, entrsB = [], [], [], []

    for i in range(Am.get()):
        for j in range(An.get()):
            ent1 = tk.Entry(frm2, font=k, width=4)
            ent1.grid(row=i + 1, column=j + 1)
            entrs1.append(ent1)
        entrsA.append(entrs1)
        entrs1 = []
    for i in range(Bm.get()):
        for j in range(Bn.get()):
            ent2 = tk.Entry(frm3, font=k, width=4)
            ent2.grid(row=i + 1, column=j + 1)
            entrs2.append(ent2)
        entrsB.append(entrs2)
        entrs2 = []
    btn0b.pack(fill=tk.X)
    btn0a.destroy()
    frms = [frm2, frm3]
    print('Устанавливаю ячейки матриц')


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
        res.set(printres(C))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def printres(p):  # Вывод в виде матрицы
    if typenum == 'Decimal':
        p = re.sub(r"Decimal\('|'\)", '', str(p))
        return p[1:-1].replace(r"], ", '\n', p.count(r"], ")). \
            replace(']', '', p.count(']')).replace('[', '', p.count('[')).replace(',', ';  ', p.count(','))
    elif typenum == 'Fraction':
        p = str(p)
        p = re.sub(r"Fraction\(|\)", '', p)
        p = p[1:-1].replace(r"], ", ';   \n', p.count(r"], ")). \
            replace(']', '', p.count(']')).replace('[', '', p.count('[')).replace(',', ';  ', p.count(','))
        p, ans = p.split(';   '), ''
        for i in range(len(p)):
            if i % 2 == 0:
                ans = ans + '/'.join(p[i:i + 2])
            else:
                ans = ans + ';   '
        return ans.replace(';   \n', '\n', ans.count(';   \n')).rstrip(';   ')
    elif typenum == 'float':
        p = str(p)
        return p[1:-1].replace(r"], ", '\n', p.count(r"], ")). \
            replace(']', '', p.count(']')).replace('[', '', p.count('[')).replace(',', ';  ', p.count(','))


def difference():  # Разность
    try:
        res.set(printres(Matrices(translate(entrsA)) - translate(entrsB)))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def transpA():  # Транспонирование
    try:
        C = Matrices(translate(entrsA))
        res.set(printres(C.transpA()))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def traceA():  # След
    try:
        C = SquareMatrices(translate(entrsA))
        a = re.sub(r"Decimal\('|'\)", '', str(C.traceA()))
        if a != 'След матрицы можно вычислить\nтолько у квадратной матрицы':
            res.set('След матрицы А = ' + str(a))
        else:
            res.set(str(a))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def mult():  # Умножение А и В
    try:
        res.set(printres((Matrices(translate(entrsA)) * translate(entrsB))))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def multnum():  # Умножение на число
    try:
        if typenum == 'Decimal':
            # noinspection PyTypeChecker
            res.set(printres(Matrices(translate(entrsA)) * Decimal(num.get())))
        else:
            # noinspection PyTypeChecker
            res.set(printres(Matrices(translate(entrsA)) * Fraction(str(num.get()))))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def powerA():  # Возведение в степень
    try:
        res.set(printres(SquareMatrices(translate(entrsA)) ** power.get()))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def triangulationAU():  # Треугольный вид матрицы
    try:
        a = printres(TriangleMatrices(translate(entrsA)).triangulationAU())
        a = re.sub(r'[-]?0[.]0{1,}\d+|0E[-]\d*', '0', a)
        res.set(a)
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def detA():  # Определитель матрицы
    try:
        C = SquareMatrices(translate(entrsA))
        a = re.sub(r"Decimal\('|'\)", '', str(C.detA()))
        if a != 'Вычислить определитель можно\nтолько у квадратной матрицы':
            res.set('Определитель матрицы А = ' + str(a))
        else:
            res.set(str(a))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def invertA():  # Обратный вид матрицы
    try:
        res.set(printres(SquareMatrices(translate(entrsA)).invertA()))
    except (NameError, tk.TclError, IndexError):
        res.set('Введите размерность матриц')


def rnd(event):  # Случайные значения в ячейках матриц
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
        print('Генерирую числа в ячейках матриц')
    except NameError:
        res.set('Введите размерность матриц')


def A2BB2A():  # Поменять местами матрицы А и В
    try:
        global entrsA, entrsB, frms
        entrsA, entrsB = entrsB, entrsA
        if frms[0]['text'] == "Матрица В":
            frms[0].place(x=frm0.winfo_width() + len(entrsB[0]) * (3 * k[1]) + k[1] + 40)
        else:
            frms[0].place(x=frm0.winfo_width() + len(entrsA[0]) * (3 * k[1]) + k[1] + 40)
        print('Меняю местами')
        frms[1].place(x=frm0.winfo_width())
        frms[0].config(text="Матрица В"), frms[1].config(text="Матрица А")
        frms = [frms[1], frms[0]]
    except NameError:
        res.set('Введите размерность матриц')


def rndfg(event):  # Случайный цвет для кнопки, генерирующей случайные значения в ячейках матрицы
    btnr['fg'] = '#' + ''.join([str(hex(randint(0, 8)))[2] for _ in range(6)])


btnr = tk.Button(frm0, font=k, text='Случайные значения в ячейках матрицы')
btnr.bind('<Button-1>', lambda event: [rnd(event), rndfg(event)])
btnr.pack(fill=tk.X)
btn0a = tk.Button(frm0, font=k, text='Получить размерность матриц', command=show1)
btn0a.pack(fill=tk.X)
btn0b = tk.Button(frm0, font=k, text='Получить размерность матриц', command=show2)


# Кнопки вычислений
frm1 = tk.LabelFrame(window, text='Основные операции над матрицами', font=k)
frm1.pack(side='left', anchor='n')
res = tk.StringVar()
btn1 = tk.Button(frm1, font=k, text='А + В', command=add, width=k[1] + 1).grid()
btn2 = tk.Button(frm1, font=k, text='А - В', command=difference, width=k[1] + 1).grid(column=1, row=0)
btn3 = tk.Button(frm1, font=k, text='А * В', command=mult, width=k[1] + 1).grid(column=2, row=0)
btn4 = tk.Button(frm1, font=k, text='Трансп. А', command=transpA, width=k[1] + 1).grid(row=1)
btn5 = tk.Button(frm1, font=k, text='След А', command=traceA, width=k[1] + 1).grid(row=1, column=1)
btn6a = tk.Button(frm1, font=k, text='А ^ степень       ', command=powerA, width=k[1] + 1).grid(row=1, column=2)
ent1 = tk.Spinbox(frm1, font=k, textvariable=power, from_=-float('inf'), to=float('inf'), width=2)
ent1.grid(row=1, column=2, sticky='e')
btn7 = tk.Button(frm1, font=k, text='A * число      ', command=multnum, width=k[1] + 1).grid(row=2)
ent2 = tk.Spinbox(frm1, font=k, textvariable=num, from_=-float('inf'), to=float('inf'), width=2) \
    .grid(row=2, column=0, sticky='e')
btn8 = tk.Button(frm1, font=k, text='det(A)', width=k[1] + 1, command=detA).grid(row=2, column=1)
btn9 = tk.Button(frm1, font=k, text='Ступенчатый вид A (U)', width=2 * k[1] + 1, command=triangulationAU)\
    .grid(row=3, column=0, columnspan=2)
btn10 = tk.Button(frm1, font=k, text='Обратный вид А', width=k[1] + 1, command=invertA).grid(row=2, column=2)
btn11 = tk.Button(frm1, font=k, text='Поменять А и В', width=k[1] + 1, command=A2BB2A).grid(row=3, column=2)
frm4 = tk.LabelFrame(window, font=k, text='Ответ')
frm4.pack(side='left', anchor='n')
lbl1 = tk.Label(frm4, font=k, textvariable=res).pack()

frm5 = tk.LabelFrame(window, font=k, text='Другие операции')
frm5.pack(side='right', anchor='s')


# Тип чисел
def chng():  # Изменяет тип чисел
    global typenum
    if r_var.get() == 1:
        typenum = 'Decimal'
        print('Изменяю тип чисел на "Decimal"')
        btnFrac['fg'], btnfloat['fg'] = 'black', 'black'
        btnDec['fg'] = 'green'
    elif r_var.get() == 0:
        typenum = 'Fraction'
        print('Изменяю тип чисел на "Fraction"')
        btnFrac['fg'] = 'green'
        btnDec['fg'], btnfloat['fg'] = 'black', 'black'
    elif r_var.get() == 2:
        typenum = 'float'
        print('Изменяю тип чисел на "float"')
        btnfloat['fg'] = 'green'
        btnDec['fg'], btnFrac['fg'] = 'black', 'black'


frm6 = tk.LabelFrame(window, font=k, text='Тип чисел')
frm6.place(relx=0, rely=0.8)
r_var = tk.IntVar()
r_var.set(1)
btnDec = tk.Radiobutton(frm6, text='Десятичная дробь', value=1, variable=r_var, fg='green', font=k)
btnDec.pack()
btnFrac = tk.Radiobutton(frm6, text='Обыкновенная дробь', value=0, variable=r_var, fg='black', font=k)
btnFrac.pack()
btnfloat = tk.Radiobutton(frm6, text='Простой float', value=2, variable=r_var, fg='black', font=k)
btnfloat.pack()
btnchng = tk.Button(frm6, text='Изменить', font=k, command=chng).pack(fill=tk.X)


# Окно Canvas ---------------------------------------------------------------------------------------------------------
size = 200
canva = tk.Canvas(frm5, bg='white', height=size, width=size)
canva.pack(side='top')
k1 = ('Times New Roman', 6)
Y = lambda: [canva.create_line(size / 2, 0, size / 2, size, arrow='first'),
             canva.create_text(size / 2 + 7, 9, text='y', font=k),
             [canva.create_line(size / 2 - 2, 25 * i, size / 2 + 2, 25 * i) for i in range(1, int(size / 25))],
             [canva.create_text(size / 2 - 9, 25 * i, text=f'{int(size / 2) - 25 * i}', font=k1)
              for i in range(1, int(size / 25)) if i * 25 - size / 2 != 0]]
X = lambda: [canva.create_line(0, size / 2, size, size / 2, arrow='last'),
             canva.create_text(size - 7, size / 2 - 9, text='x', font=k),
             [canva.create_line(25 * i, size / 2 - 2, 25 * i, size / 2 + 2) for i in range(1, int(size / 25))],
             [canva.create_text(25 * i, size / 2 - 5, text=f'{int(25 * i - size / 2)}', font=k1)
              for i in range(1, int(size / 25)) if i * 25 - size / 2 != 0]]


def project2x2():  # Параллелограмм матрицы на Canvas
    try:
        # for i in range(100):
        #     rnd()
            a, b, c = int(entrsA[0][0].get()), int(entrsA[1][0].get()), int(entrsA[0][1].get())
            d = int(entrsA[1][1].get())
            clr = '#' + ''.join([str(hex(randint(0, 12)))[2] for _ in range(6)])
            activeclr = '#' + ''.join([str(hex(randint(0, 12)))[2] for _ in range(6)])
            half = size / 2
            canva.create_line(half, half, a + half, b + half, fill=clr, width=k[1] // 3, activefill=activeclr)
            canva.create_line(a + half, b + half, a + half + c, b + half + d, fill=clr, width=k[1] // 3,
                              activefill=activeclr)
            canva.create_line(a + half + c, b + half + d, c + half, d + half, fill=clr, width=k[1] // 3,
                              activefill=activeclr)
            canva.create_line(c + half, d + half, half, half, fill=clr, width=k[1] // 3, activefill=activeclr)
            print(f'Рисую параллелограмм в Canvas HEX-цвета {clr}')
            res.set('')
    except NameError:
        res.set('Введите размерность матриц')
    except IndexError:
        res.set('Введите матрицу А,\nкак минимум 2x2')
    except ValueError:
        res.set('Введите целые числовые\nзначения в ячейки матрицы A 2x2')


# Другие кнопки
btn12 = tk.Button(frm5, font=k, text='Параллелограмм матрицы А (2x2) в окне Canvas', command=project2x2).pack(fill=tk.X)
btn13 = tk.Button(frm5, font=k, text='Очистить окно Canvas',
                  command=lambda: [canva.delete("all"), print('Очищаю Canvas от фигур'), Y(), X()]).pack(fill=tk.X)
btn14 = tk.Button(frm5, font=k, text='Выйти из программы', command=window.destroy)
btn14.pack(fill=tk.X), Y(), X()


def snezhinki(event):  # Снежинки!
    from math import radians, sin, cos
    for j in range(int(size / 5), size, int(size / 5)):
        addy = randint(-int(size / 2), int(size / 2))
        addx = randint(-int(size / 2), int(size / 2))
        [canva.create_line(j + addx / 2, j + addy, j + size / 16 * cos(radians(i)) + addx / 2, j + size / 16
                           * sin(radians(i)) + addy, fill='#2db7e5') for i in range(0, 360, 20)]
    print('Рисую 4 снежинки в Canvas')


# Начало работы окна Tkinter
window.bind(',', snezhinki)
window.bind('r', lambda event: [rnd(event), rndfg(event)])
print('-------------Начало работы-------------')
print('<<---------------------------------------Горячие клавиши--------------------------------------->>')
print('Нарисовать снежинки в Canvas - горячая клавиша <,>\n'
      'Сгенерировать случайные элементы матриц - горячая клавиша <r>')
print('>>---------------------------------------Горячие клавиши---------------------------------------<<')
snezhinki(',')
window.mainloop()
print('-------------Конец работы-------------')

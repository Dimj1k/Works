import os
import argparse as ag

class Matrix:

    def __init__(self, matrixA: list):
        self.matrixA = matrixA
        self.mA = len(matrixA)
        self.nA = len(matrixA[0])

    __str__ = lambda self:str(self.matrixA).replace('], ', '\n').replace(', ', '\t').replace('[', '').replace(']', '')

    def __mul__(self, a: float):
        return ([[j * a for j in i] for i in self.matrixA])

    def __sub__(self, lst: list):
        return [[self.matrixA[i][j] - lst[i][j] for j in range(self.nA)] for i in range(self.mA)]

    def tri_one_step(self, st: int):
        for i in range(st, self.mA):
            if self.matrixA[i][st] != 0:
                self.matrixA[st], self.matrixA[i] = self.matrixA[i], self.matrixA[st]
                break
        m = 1
        for i in range(self.nA):
            m = i
            for j in range(i + 1, self.mA + 1):
                try:
                    while self.matrixA[i][m] == 0:
                        m += 1
                    if self.matrixA[j][m] / self.matrixA[i][m] == 0:
                        continue
                    self.matrixA[j] = (Matrix([self.matrixA[j]]) - (Matrix([self.matrixA[i]]) * \
                                                                    (self.matrixA[j][m] / self.matrixA[i][m])))[0]
                    return Matrix(self.matrixA)
                except (IndexError, ZeroDivisionError):
                    continue
        return None

    @property
    def get_Tri(self):
        return self.matrixA


class SysLinearEq:

    import re
    from random import randint

    def __init__(self, linear: str):
        self.vector, self.matrix = [], []
        linear = linear.replace(',', '.').replace(' ', '').replace('\t', '').split('\n')
        for i in linear:
            lineqvar = self.re.findall(r'[a-z]\d*', i)
            lineq = self.re.split('|'.join(lineqvar), i.strip('.').strip(';'))
            for i in range(len(lineq)):
                if lineq[i] == '' or lineq[i] == '+': lineq[i] = '+1'
                elif lineq[i] == '-': lineq[i] = '-1'
            self.matrix.append({lineqvar[j]:float(lineq[j]) for j in range(len(lineq[:-1]))})
            self.vector.append(float(lineq[-1][1:]))
        self.keys = tuple(set([j for i in [k.keys() for k in self.matrix] for j in i]))
        matincl = []
        for i in range(len(self.matrix)):
            for j in self.keys:
                if j in self.matrix[i]: matincl.append(self.matrix[i][j])
                else: matincl.append(0)
        self.matrix = [matincl[k:len(self.keys) + k] for k in range(0, len(matincl), len(self.keys))]

    @property
    def get_matrix(self): return self.matrix
    @property
    def get_keys(self): return self.keys
    @property
    def get_vector(self): return self.vector
    def setsimpllin(self, vector: list, matrix: list): self.vector, self.matrix = vector, matrix

    def solution(self):
        for i in range(len(self.vector)):
            if self.matrix[i] == [0] * len(self.matrix[0]) and self.vector[i] != 0:
                return 'Система несовместна.\nРешений данной системы нет'
        matrixT = [[self.matrix[i][j] for i in range(len(self.matrix))] for j in range(len(self.matrix[0]))]
        vectors = list(zip(self.keys, matrixT))
        variables = []
        for i in range(1, len(self.vector) + 1):
            m = 0
            try:
                while self.matrix[-i][m] == 0: m += 1
            except: continue
            a = " + ".join([(str(-self.matrix[-i][j] / self.matrix[-i][m]) + "*" + self.keys[j])
                            for j in range(len(self.keys)) if j != m])
            variables.append([vectors[m][0], f'{self.vector[-i] / self.matrix[-i][m]} + ({a})'])
        firstvars = []
        for i in range(len(variables)):
            a = variables[i][1][variables[i][1].find('(') + 1:-1]
            a = self.re.sub('-?0.0\*[a-z]\d*', '', a).replace(' ', '').strip('+')
            a = (variables[i][1][:variables[i][1].find('(')] + a).strip(' + ')
            try: firstvars, variables[i][1] = [[variables[i][0], float(a)]] + firstvars, a
            except ValueError:
                if len(variables[i][1]) == 1: firstvars = [[variables[i][0], a]] + firstvars
                else: firstvars += [[variables[i][0], a]]
                variables[i][1] = a
        keys_var = [i[0] for i in variables]
        if keys_var != self.keys:
            firstvars = [[a, chr(ord("A") + i)] for (i, a) in enumerate(self.keys) if a not in keys_var] + firstvars
        variables = firstvars
        for i in firstvars:
            for j in range(len(variables)):
                if type(variables[j][1]) == str: firstvars[j][1] = variables[j][1].replace(i[0], '(' + str(i[1]) + ')')
        a = []
        k, quest, randoms, a = False, [], [], a + [self.re.findall('[A-Z]', i[1]) for i in firstvars
                                                    if type(i[1]) != float and len(i[1]) == 1]
        randoms = [str(self.randint(-10, 10)) for _ in range(len(a))]
        for i in firstvars:
            if len(a) == 0:
                quest.append(eval(str(i[1])))
            else:
                k = True
                exec(f"{', '.join([j[0] for j in a])} = {', '.join(randoms)}")
                quest.append(eval(str(i[1])))
        ans = [f'{firstvars[i][0]} = {quest[i]}' for i in range(len(quest))]
        if k:
            infans = ', '.join([firstvars[e][1] + ' = ' + i for e, i in enumerate(randoms)])
            return 'СЛАУ имеет бесконечное количество решений. Все решения:\n' + \
             '\n'.join([f'{firstvars[i][0]} = {firstvars[i][1]}' for i in range(len(firstvars))]) + '\n' + \
                'Одно из решений при ' + infans + '\n' + '\n'.join([f'{firstvars[i][0]} = {quest[i]}'
                for i in range(len(firstvars))])
        return 'СЛАУ имеет одно решение:\n' + '\n'.join(ans)
                
    __repr__ = lambda self:'Матрица:' + str(self.matrix)+' Вектор:'+str(self.vector)+' Набор:'+' '.join(self.keys)


parser = ag.ArgumentParser(description='Решение системы линейных уравнений.')
parser.add_argument('input', help='Укажите файл с СЛАУ', nargs='?', metavar='inputfile')
parser.add_argument('-o','--output',type=str, help='Укажите с каким именем файла вывести решение СЛАУ в директорию'
                    f' {os.path.join(os.path.dirname(__file__), "output")}. По-умолчанию: [inputfile].txt',
                    dest='o', nargs='?', metavar='file')
inp, out = parser.parse_args().input, parser.parse_args().o
directory = os.path.dirname(__file__)
output = os.path.join(directory, 'output')
if not(os.path.exists(output)): os.makedirs(output)
if inp is None: print('Введите имя файла, в котором нужно считать систему линейных уравнеий'), exit()
elif inp[:len(directory)] == directory: inp = inp[len(directory) + 1:]
if out is None or out == '': out = inp
with open(os.path.join(directory, inp), 'r') as input:
    try: mat = SysLinearEq(input.read().strip())
    except: raise('Произошла ошибка, введите СЛАУ правильно.')
with open(os.path.join(output, out), 'w', encoding='UTF-8') as output:
    print('-' * 5, str(mat), '-' * 5, file=output)
    matAndvec = [mat.get_matrix[i] + [mat.get_vector[i]] for i in range(len(mat.get_vector))]
    print('СЛАУ в виде матрицы:\n' + '\t'.join(mat.get_keys) + '\tВектор' + f'\n{Matrix(matAndvec)}', file=output)
    print('Упрощение СЛАУ в виде матрицы пошагово:', file=output)
    for i in range(len(mat.get_keys) * len(mat.get_vector)):
        matAndvec2 = Matrix(matAndvec).tri_one_step(i)
        try:
            matAndvec = matAndvec2.get_Tri
            print('-' * 5, f'Шаг {i + 1}:', '-' * 5, file=output)
            print(Matrix(matAndvec), file=output)
        except AttributeError:
            print('-' * 5, 'Система линейных уравнений упрощена', '-' * 5, file=output)
            break
    mat.setsimpllin([i[-1] for i in matAndvec], [i[:-1] for i in matAndvec])
    print('Решение системы линейных уравнений:', file=output)
    print(mat.solution(), file=output)
    print('Результат сохранен в', output.name)

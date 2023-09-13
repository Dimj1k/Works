from src import *


class Main:

    zadacha: Zadacha
    data: Data
    path: ProgramPath
    graph: Graph
    timer = CalcTime()
    to_txt: TxtWriter
    __len_best_prev_expert = 0

    def main(self):
        i_v = self.__get_from_user_data()
        print("Подготовка данных")
        self.__create_zadacha(i_v)
        i_v["stats"]["hi2_table"] = self.zadacha.user_stats["hi2_table"]
        print(f"Данные подготовлены за {self.timer[-1]:.6f} с")
        combs_ranks = len(self.zadacha.all_combs_ranks)
        print(f"Количество комбинаций рангов: {combs_ranks}")
        print("Создание рабочей директории")
        self.path = ProgramPath(__file__, i_v["num_experts"])
        print(f"Рабочая директория {self.path.main_dir.absolute()} создана")
        print("Запись в текстовый файл основной информации")
        self.to_txt = TxtWriter(self.path)
        name = self.__info_to_txt(i_v)
        print(f"Запись в текстовый файл ({name}) основной информации завершен за {self.timer[-1]:.6f} с")
        self.data = Data(self.path)
        self.graph = Graph(self.path)
        print("Запись основной информации в электронную таблицу")
        name = self.__write_gen_info(i_v["stats"]["p_user"])
        print(f"Электронная таблица ({name}) создана за {self.timer[-1]:.6f} с")
        print("Начат анализ комбинаций рангов экспертами")
        solvers = self.zadacha.solve()
        num_experts = i_v["num_experts"]
        ranges = range(1, num_experts + 1) if type(num_experts) is int else range(num_experts[0], num_experts[1] + 1)
        for i in ranges:
            state_is_not_continue = self.__check_state_solver(self.zadacha.state, i - 1)
            if state_is_not_continue:
                break
            print(f"Эксперт {i} начал работу")
            solver = self.__expert_work(solvers, i, combs_ranks, i_v)
            print(f"Эксперт {i} завершил работу за {self.timer[-1]:.6f} с")
            print(f"Вывод информации в текстовый файл про проведенную работу эксперта")
            self.__len_best_prev_expert = len(solver.all_matrices["best"])
            self.__expert_to_txt(solver)
            print(f"Вывод информации завершен за {self.timer[-1]:.6f} с")
        self.to_txt.end_file(self.timer)
        print(f"Время работы программы {self.timer.program_time():.4f} с\n"
              f"Время всех расчетов: {sum(el for key, el in self.timer):.4f} с\n",
              "(" + ", ".join(f"{i}: {j:.6f} с" for i, j in self.timer) + ")")

    def __check_state_solver(self, state, i):
        if state == StateZadacha.NOT_CONVERGE:
            print(f"Эксперт №{i} обнаружил, что процесс не сходится")
            return True
        if state == StateZadacha.BEST_FINDED:
            more_one = self.__len_best_prev_expert > 1
            print(f"Эксперт №{i} обнаружил, что",
                  "подходящие матрицы решений" if more_one else "подходящая матрица решений",
                  f"найден{'аы'[more_one]}")
            return True
        return False

    @timer("alg")
    def __create_zadacha(self, i_v):
        if i_v["stats"]["w_user"]["left"] > i_v["stats"]["w_user"]["right"]:
            i_v["stats"]["w_user"]["right"], i_v["stats"]["w_user"]["left"] = \
                i_v["stats"]["w_user"]["left"], i_v["stats"]["w_user"]["right"]
        self.zadacha = Zadacha(*i_v.values())

    @timer("txt")
    def __info_to_txt(self, i_v):
        return self.to_txt.input(i_v, self.zadacha)

    @timer()
    def __expert_work(self, solvers, i, combs_ranks, i_v):
        print(f"Анализ комбинаций рангов ({combs_ranks ** i} шт.) {i} эксперта")
        solver = self.__expert_analyzing(solvers)
        if solver.total_matrices < combs_ranks ** i:
            print(f"Эксперт закончил работу досрочно. Его количество рассмотренных матриц: {solver.total_matrices}")
        print(f"Анализ комбинаций рангов {i} эксперта завершен за {self.timer[-1]:.6f} с")
        next(self.path)
        print(f"Подготовка диаграмм от {i} эксперта")
        self.graph.to_next_expert()
        print("Вывод круговой диаграммы с выбором количеств матриц решений")
        name = self.__pie_diagram(solver)
        print(f"Вывод круговой диаграммы ({name}) завершен за {self.timer[-1]:.6f} с")
        print("Вывод столбиков погрешностей со статистическими показателями матриц")
        names = self.__errorbar_diagrams(solver, i_v["stats"]["p_user"])
        print(f"Вывод столбиков погрешностей ({', '.join(names)}) завершен за {self.timer[-1]:.6f} с")
        print("Вывод столбчатой диаграммы с выполненными условиями")
        name = self.__bar_diagram(solver)
        print(f"Вывод столбчатой диаграммы ({name}) завершен за {self.timer[-1]:.6f} с")
        print(f"Вывод матриц решений и полученные диаграммы от {i} эксперта в электронную таблицу")
        self.data.to_next_expert()
        name = self.__write_matrices(solver)
        print(f"Вывод матриц решений в электронную таблицу ({name}) завершен за {self.timer[-1]:.6f} с")
        return solver

    @timer("txt")
    def __expert_to_txt(self, solver):
        self.to_txt.expert(solver, self.zadacha.state, self.timer)

    @timer("data")
    def __write_gen_info(self, p_user):
        return self.data.write_gen_info(self.zadacha, p_user)

    @timer("alg")
    def __expert_analyzing(self, solvers):
        return next(solvers)

    @timer("data")
    def __write_matrices(self, solver):
        return self.data.write_matrices_expert(solver)

    @timer("graph")
    def __pie_diagram(self, solver):
        return self.graph.pie_choice(solver)

    @timer("graph")
    def __errorbar_diagrams(self, solver, p_user):
        return self.graph.errorbar_stats(solver, p_user)

    @timer("graph")
    def __bar_diagram(self, solver):
        return self.graph.bar_met_conds(solver)

    def __get_from_user_data(self):
        return {
            "data": self.__get_data(),
            "stats": {
                "w_user": {
                    "left": self.__get_left_w(),
                    "right": self.__get_right_w()
                },
                "p_user": self.__get_p_user(),
                "eps": self.__get_eps()
            },
            "use_all_ranks": self.__get_use_all_ranks(),
            "num_experts": self.__get_num_experts(),
            "max_best": self.__get_num_max_best(),
            "save_matrices": self.__get_save_matrices()
        }

    def __get_data(self):
        d, i = [], 0
        try:
            d = input("Введите коэффициенты через пробел\n"
                      "(Вы можете вводить обыкновенные дроби): ").strip().split()
            for i, el in enumerate(d):
                stripped_d = el.replace(",", ".").strip()
                if stripped_d:
                    d[i] = eval(stripped_d)
        except SyntaxError:
            print(f"Произошла ошибка. Вы ввели {i} коэффициент не числом ({d[i]})")
            return self.__get_data()
        return d

    def __get_left_w(self, side="Левая"):
        w = ""
        try:
            w = input(f"Введите диапазон коэффициента конкордации\n{side} граница диапазона: ").strip()
            if 0 <= float(w) <= 1:
                return float(w)
            else:
                print("Коэффициент конкордации должен принадлежать отрезку [0, 1]")
                return self.__get_left_w(side)
        except ValueError:
            print(f"Произошла ошибка. Вы ввели {w} - не число.")
            return self.__get_left_w(side)

    def __get_right_w(self):
        return self.__get_left_w("Правая")

    def __get_p_user(self):
        p = ""
        try:
            p = input("Введите коэффициент значимости: ").strip()
            if 0 <= float(p) <= 1:
                return float(p)
            else:
                print("Коэффициент значимости должен принадлежать отрезку [0, 1]")
                return self.__get_p_user()
        except ValueError:
            print(f"Произошла ошибка. Вы ввели {p} - не число.")
            return self.__get_p_user()

    def __get_eps(self):
        eps = ""
        try:
            eps = input("Введите максимальную погрешность: ").strip()
            return abs(float(eps))
        except ValueError:
            print(f"Произошла ошибка. Вы ввели {eps} - не число.")
            return self.__get_eps()

    @staticmethod
    def __get_use_all_ranks():
        use_all = input("Использовать ли все комбинации сочетаний рангов (y(д)/n(н)): ").lower().strip()
        return use_all in ("y", "l", "д", "да", "yes", "нуы", "lf", "1", "t", "true")

    def __get_num_experts(self):
        num = ""
        try:
            num = input("Введите максимальное количество экспертов и"
                        " максимальное количество строк в матрице решений: ").strip()
            if ":" in num:
                if num.count(":") == 1:
                    n, m = tuple(map(int, num.split(":")))
                    if n <= 0 or m <= 0:
                        print("Количество экспертов и максимальное количество строк в матрице решений число большее 1")
                        return self.__get_num_experts()
                    return n, m if n < m else m, n
                else:
                    raise IndexError()
            if int(num) < 1:
                print("Количество экспертов и максимальное количество строк в матрице решений число большее 1")
                return self.__get_num_experts()
            return int(num)
        except ValueError:
            print(f"Произошла ошибка. Вы ввели {num} - не целое число.")
            return self.__get_num_experts()
        except IndexError:
            print(f"Произошла ошибка. Вы ввели {num} - содержит больше одного \":\".")
            return self.__get_num_experts()

    def __get_save_matrices(self):
        num = ""
        try:
            num = input("Введите сохраняемое максимальное количество комбинаций матриц решений, не подходящих под Ваши"
                        " статистические показатели (рекомендуемое количество 100000)\nВведите \"-1\" или \"inf\""
                        " для сохранения всех матриц решений: ")
            if num in ("-1", "inf", "шта", "инф", "бесконечно", "бск", "infinity", ",cr", "шташтшен"):
                return float("inf")
            if int(num) < 0:
                print("Максимальное количество матриц должно быть число неотрицательное")
                return self.__get_save_matrices()
            return int(num)
        except ValueError:
            print(f"Произошла ошибка. Вы ввели {num} - не целое число")
            return self.__get_save_matrices()

    def __get_num_max_best(self):
        num = ""
        try:
            num = input("Введите максимальное количество подходящих матриц у эксперта для прекращения его работы\n"
                        "Введите \"-1\" или \"inf\" для перебора всех комбинаций матриц: ")
            if num in ("-1", "inf", "шта", "инф", "бесконечно", "бск", "infinity", ",cr", "шташтшен"):
                return float("inf")
            if int(num) <= 0:
                print("Максимальное количество матриц должно быть число положительное")
                return self.__get_num_max_best()
            return int(num)
        except ValueError:
            print(f"Произошла ошибка. Вы ввели {num} - не целое число")
            return self.__get_num_max_best()


if __name__ == "__main__":
    Main().main()

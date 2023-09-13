from .zadacha import StateZadacha, TYPES_MATRICES
TYPES_MATRICES_RU = {mtype: mtype_ru
                     for mtype, mtype_ru in zip(TYPES_MATRICES, ["подходящих", "хороших", "не подходящих"])}


class TxtWriter:

    def __init__(self, path):
        self.path = path
        self.__out = path.main_dir / "отчет.txt"
        self.__w, self.__hi2, self.__len_combs, self.__eps = None, None, None, None

    def input(self, i_v, zadacha):
        with self.__out.open(mode="a", encoding="utf-8") as f:
            print("-" * 5, "Общая информация", "-" * 5, file=f)
            print("Введенные исходные данные:", ", ".join(map(str, i_v["data"])), file=f)
            print("Ранги исходных данных:", ", ".join(map(str, zadacha.ranks)), file=f)
            print("Количество столбцов в матрицах решений:", len(zadacha.ranks), file=f)
            print("Весовые коэффициенты:", ", ".join(map(str, zadacha.weights)), file=f)
            print("-" * 5, "Введенные статистические показатели", "-" * 5, file=f)
            stats = i_v['stats']
            self.__w = f"[{stats['w_user']['left']}, {stats['w_user']['right']}]"
            self.__hi2 = zadacha.user_stats["hi2_table"]
            self.__eps = i_v["stats"]["eps"]
            print(f"Значение конкордации: {self.__w}", file=f)
            print("Коэффициент значимости:", stats['p_user'], file=f)
            print("Табличный хи-квадрат коэффицента значимости:", self.__hi2, file=f)
            print("Максимальная погрешность:", stats["eps"], file=f)
            print("-" * 5, "Введенные данные для поиска подходящих матриц решений", "-" * 5, file=f)
            print("Использование всех сочетаний рангов:",
                  ("Используются не все сочетания рангов", "Используются все сочетания рангов")[i_v["use_all_ranks"]],
                  file=f)
            self.__len_combs = len(zadacha.all_combs_ranks)
            print("Количество сочетаний рангов:", self.__len_combs, file=f)
            if type(i_v["num_experts"]) is int:
                print("Число экспертов и максимальное число строк в матрице решений:", i_v["num_experts"], file=f)
            else:
                num_exp = i_v["num_experts"]
                print("Число экспертов:", num_exp[1] - num_exp[0] + 1, file=f)
                print(f"Число строк в матрице решений: [{num_exp[0]}, {num_exp[1]}]", file=f)
            print("Максимальное количество подходящих матриц у эксперта для прекращения его работы:",
                  i_v["max_best"], file=f)
            print("Максимальное количество сохраняемых в памяти матриц, не удовлетворяющих двум условиям:",
                  i_v["save_matrices"], file=f)
            print("-" * 15, file=f)
        return self.__out.name

    def expert(self, expert, state, timer):
        with self.__out.open(mode="a", encoding="utf-8") as f:
            print("-" * 5, f"Эксперт №{expert.num_rows}", "-" * 5, file=f)
            print("Количество рассмотренных матриц решений:", expert.total_matrices, file=f, end="")
            if self.__len_combs ** expert.num_rows > expert.total_matrices:
                print(" из", self.__len_combs ** expert.num_rows, file=f)
            else:
                print(file=f)
            print("Количество подходящих матриц решений:", len(expert.all_matrices["best"]), file=f)
            print("Количество нормальных матриц решений:", len(expert.all_matrices["normal"]), file=f)
            print("Количество не подходящих матриц решений:",
                  expert.total_matrices - len(expert.all_matrices["best"]) - len(expert.all_matrices["normal"]),
                  file=f)
            met_conds = expert.met_conds
            print("-" * 5, file=f)
            print(f"Количество выполненных условий: \"Хи-квадрат матрицы больше чем {self.__hi2:.4f}\":",
                  met_conds["hi^2"], file=f)
            print(f"Количество выполненных условий: \"Значение конкордации матрицы принадлежит отрезку {self.__w}\":",
                  met_conds["W"], file=f)
            print(f"Количество выполненных условий: \"Значение конкордации матрицы принадлежит отрезку {self.__w} и "
                  f"хи-квадрат матрицы больше чем {self.__hi2:.4f}\":", met_conds["W_hi^2"], file=f)
            print(f"Количество выполненных условий: \"Максимальная разница весовых коэффициентов матрицы меньше"
                  f"{self.__eps}\": {met_conds['eps']}", file=f)
            info, mtypes = expert.get_saved_stats_from_matrices()
            epsilons = info["eps"]
            for mtype in mtypes:
                print(f"Минимальная максимальная разница весовых коэффициентов {TYPES_MATRICES_RU[mtype]}"
                      f" матриц: {epsilons[mtype]['min']}", file=f)
            print("-" * 5, file=f)
            print(f"Время выполнения работы эксперта №{expert.num_rows}: {timer[-1]:.6f} с", file=f)
            if state == StateZadacha.NOT_CONVERGE:
                print(f"Эксперт №{expert.num_rows} обнаружил, что процесс не сходится", file=f)
            elif state == StateZadacha.BEST_FINDED:
                more_one = len(expert.all_matrices["best"]) > 1
                print(f"Эксперт №{expert.num_rows} обнаружил, что",
                      "подходящие матрицы решений" if more_one else "подходящая матрица решений",
                      f"обнаружен{'аы'[more_one]}", file=f)
            print("-" * 15, file=f)

    def end_file(self, timer):
        with self.__out.open(mode="a", encoding="utf-8") as f:
            print(f"Затраченное время {timer.program_time():.4f} с", file=f)

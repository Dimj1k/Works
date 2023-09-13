import matplotlib.pyplot as plt
from .zadacha import TYPES_MATRICES, UNSAVED_TYPE_MATRIX
from os import sep
from numpy import array, mean, arange
MTYPES_COLORS = {mtype: c for mtype, c in zip(TYPES_MATRICES, ["green", "blue", "red"])}
TYPES_MATRICES_RU = {mtype: mtype_ru
                     for mtype, mtype_ru in zip(TYPES_MATRICES, ["Подходящие", "Хорошие", "Не подходящие"])}


class Graph:

    def __init__(self, path):
        self.path = path
        self.__main_dir = None

    def to_next_expert(self):
        self.__main_dir = self.path.main_dir / "Диаграммы"
        self.__main_dir.mkdir(exist_ok=True)

    def pie_choice(self, expert):
        name_fig = self.__main_dir / "выбор_матриц_экспертом.png"
        matrices = {mtype: len(matrices) for mtype, matrices in expert.all_matrices.items()}
        all_matrices = expert.total_matrices
        if sum(matrices.values()) != all_matrices:
            matrices[UNSAVED_TYPE_MATRIX] = all_matrices - sum(matrices.values()) + matrices[UNSAVED_TYPE_MATRIX]
        show_it = [el for el in matrices.values() if el]
        _, _, pcts = plt.pie(show_it, colors=[MTYPES_COLORS[mtype] for mtype, lens in matrices.items() if lens],
                             labels=[TYPES_MATRICES_RU[mtype] for mtype, lens in matrices.items() if lens],
                             autopct="%.2f%%", pctdistance=0.75, labeldistance=1.03, normalize=True,
                             explode=[0.1 for _ in show_it])
        plt.title("Количество выбранных матриц экспертом")
        plt.text(1.1, 1.1, f"Всего: {sum(matrices.values())}",
                 bbox={"facecolor": "none", "boxstyle": "round, pad=0.25"})
        [pct.set_text(el) for pct, el in zip(pcts, show_it)]
        plt.savefig(name_fig, format="png", dpi=135)
        plt.close()
        return sep.join(name_fig.parts[-3:])

    def errorbar_stats(self, expert, p_user):
        name_figs = []
        ylabels = {"hi^2": "Критерий хи-квадрат", "W": "Значение конкордации", "p": "Коэффициент значимости",
                   "eps": "Максимальная разница между весами"}
        markers = {"hi^2": expert.hi2_table, "W": (expert.W_user["left"], expert.W_user["right"]), "p": p_user,
                   "eps": expert.eps}
        saved, mtypes = expert.get_saved_stats_from_matrices()
        colors = [MTYPES_COLORS[mtype] for mtype in TYPES_MATRICES if mtype in mtypes]
        o_x = list(range(len(mtypes)))
        for stat, item in saved.items():
            plt.xlabel("Матрицы решений")
            plt.ylabel(ylabels[stat])
            plt.xticks(o_x, [TYPES_MATRICES_RU[mtype] for mtype in mtypes])
            yerr_min = array([el["min"] for el in item.values()])
            yerr_max = array([el["max"] for el in item.values()])
            yerr_avg = mean([yerr_max, yerr_min], axis=0)
            for x, color, avg, minimum, maximum in zip(o_x, colors, yerr_avg, yerr_avg - yerr_min, yerr_max - yerr_avg):
                plt.errorbar(x, avg, yerr=[[minimum], [maximum]], marker='s', linestyle='none', ecolor=color,
                             color=color, elinewidth=0.8, capsize=4, capthick=1,
                             label=f"Значения {stat}" if x == 0 else None)
            if type(markers[stat]) is not tuple:
                plt.errorbar(o_x, [markers[stat]] * len(mtypes), yerr=[[0] * len(mtypes)] * 2,
                             fmt='v', ecolor='#0008', color='#0008', label="Выбранное значение")
            else:
                avg = mean(markers[stat])
                plt.errorbar(o_x, [avg] * len(mtypes), yerr=[[avg - markers[stat][0]] * len(mtypes),
                                                             [markers[stat][1] - avg] * len(mtypes)],
                             marker='s', ecolor='#0008', color='#0008', label="Выбранное значение", linestyle="")
            plt.legend(loc="best")
            plt.title(f"{ylabels[stat]} комбинаций матриц решений")
            name_fig = self.__main_dir / f"стат_показ_матриц_{stat}.png"
            name_figs.append(sep.join(name_fig.parts[-3:]))
            plt.savefig(name_fig, format="png", dpi=135)
            plt.close()
        return name_figs

    def bar_met_conds(self, expert):
        xticks = ["Больше табличного хи-квадрат", "W в промежутке", "Выполнены хи-квадрат и W",
                  "Максимальная разница\nвесов < заданной"]
        xticks = [f"\n{tick}" if i % 2 else tick for i, tick in enumerate(xticks)]
        met_conds = expert.met_conds
        total_matrices = expert.total_matrices
        unmet_conds = {key: total_matrices - met for key, met in met_conds.items()}
        width, mult = 0.1, 0
        x = arange(len(xticks))
        plt.xticks(x, xticks)
        rects = plt.bar(x - width / 2, met_conds.values(), width=width, label="Выполнено")
        plt.bar_label(rects, padding=1)
        rects = plt.bar(x + width / 2, unmet_conds.values(), width=width, label="Не выполнено")
        plt.bar_label(rects, padding=1)
        plt.ylabel("Количество раз выполненных условий")
        plt.title("Количество раз выполненных условий матриц решений")
        plt.legend(ncol=2)
        plt.yticks([])
        plt.subplots_adjust(top=0.922, bottom=0.118, left=0.134, right=0.908)
        name_fig = self.__main_dir / "выполненные_условия.png"
        plt.savefig(name_fig, format="png", dpi=135)
        plt.close()
        return sep.join(name_fig.parts[-3:])

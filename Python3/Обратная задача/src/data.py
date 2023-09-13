import pandas as pd
from os import sep
from .zadacha import TYPES_MATRICES, UNSAVED_TYPE_MATRIX
from pandas import DataFrame, ExcelWriter
from numpy import array, mean, unique
MTYPES_COLORS = {mtype: color for mtype, color in zip(TYPES_MATRICES, ["green", "blue", "red"])}
INDEX = "index"
ALL_ROWS = 1
APPLY = 2


class Data:

    def __init__(self, path):
        self.path = path
        self.__main_dir = path.main_dir

    def to_next_expert(self):
        self.__main_dir = self.path.main_dir
        self.__main_dir.mkdir(exist_ok=True)

    def write_gen_info(self, zadacha, p_user):
        xlsx_name = self.__main_dir / "общая_информация.xlsx"
        cols = len(zadacha.ranks)
        columns = pd.MultiIndex.from_tuples(zip(["Комбинации рангов"] * cols, range(1, cols + 1)))
        ranks_df = DataFrame.from_records(zadacha.all_combs_ranks, columns=columns,
                                          index=range(1, len(zadacha.all_combs_ranks) + 1))
        with ExcelWriter(xlsx_name, engine="xlsxwriter") as self.__writer:
            ranks_df.to_excel(self.__writer, sheet_name="gen_data", startrow=0, startcol=cols + 2)
            del ranks_df
            columns = pd.MultiIndex.from_tuples(zip(["Ранги исходных данных"] * cols, range(1, cols + 1)))
            DataFrame.from_records([zadacha.ranks], columns=columns, index=["ranks:"]) \
                .to_excel(self.__writer, sheet_name="gen_data", startrow=5, startcol=0)

            columns = pd.MultiIndex.from_tuples(zip(["Исходные данные"] * cols, range(1, cols + 1)))
            DataFrame.from_records([zadacha.data], columns=columns, index=["data:"]) \
                .to_excel(self.__writer, sheet_name="gen_data", startrow=0, startcol=0)

            columns = pd.MultiIndex.from_tuples(zip(["Весовые коэффициенты"] * cols, range(1, cols + 1)))
            DataFrame.from_records([zadacha.weights], columns=columns, index=["weights:"]) \
                .to_excel(self.__writer, sheet_name="gen_data", startrow=10, startcol=0)
            ranks = unique(zadacha.all_combs_ranks)
            columns = pd.MultiIndex.from_tuples(zip(["Ранги"] * ranks.shape[0], range(1, ranks.shape[0] + 1)))
            DataFrame.from_records([ranks], columns=columns, index=["ranks:"])\
                .to_excel(self.__writer, sheet_name="gen_data", startrow=0, startcol=cols + 2 + cols + 2)
            stats = {**{key: el for key, el in zadacha.user_stats.items() if type(el) is not dict}, "p": p_user,
                     "w_left": zadacha.user_stats["w_user"]["left"],
                     "w_right": zadacha.user_stats["w_user"]["right"]}
            columns = pd.MultiIndex.from_tuples(zip(["Исходные показатели"] * len(stats.keys()), stats.keys()))
            df = DataFrame.from_records([stats])
            df.columns = columns
            df.index = ["stats:"]
            df.to_excel(self.__writer, sheet_name="gen_stats", startrow=0, startcol=0)

        return xlsx_name.name

    def write_matrices_expert(self, expert):
        xlsx_name = self.__main_dir / "выбор_эксперта.xlsx"
        matrices = expert.get_info_matrices()
        row, col = expert.num_rows, len(expert.ranks)
        with ExcelWriter(xlsx_name, engine="xlsxwriter") as self.__writer:
            for mtype, item in matrices.items():
                self.__write_matrices(item, mtype, row, col, expert.hi2_table, expert.W_user, expert.eps)
            self.__write_used_ranks(expert)
            self.__insert_images(expert)
        return sep.join(xlsx_name.parts[-2:])

    def __write_matrices(self, matrices, sheet, row, col, hi2_user, w_user, eps_user):
        halfcol = col // 2
        added2 = 4 - col if 4 - col > 0 else 0
        for (srow, scol), matrix in zip(self.__generator_row_col(row, col, 5, 1 + added2), matrices):
            DataFrame.from_records(matrix["ranks"])\
                .to_excel(self.__writer, sheet_name=sheet, startcol=scol, startrow=srow + 1, index=False, header=False)
            DataFrame.from_dict({f"id {matrix['id']}": ""}, orient=INDEX) \
                .to_excel(self.__writer, sheet_name=sheet, startcol=scol + halfcol, startrow=srow, header=False)
            w, hi2, p, eps = matrix['W'], matrix["hi2"], matrix["p"], matrix["eps"]
            df = DataFrame.from_records([{"W": w, "hi^2": hi2, "p": p, "eps": eps}])
            df = self.__style_df(df, [["W"], ["hi^2", "p"], ["eps"]],
                                 [w_user["left"] <= w <= w_user["right"], hi2 >= hi2_user, eps <= eps_user],
                                 {"background-color": "green"}, {"background-color": "red"})
            DataFrame.from_dict({"weights": matrix["weights"]}, orient=INDEX)\
                .to_excel(self.__writer, sheet_name=sheet, startcol=scol, startrow=srow + row + 3, header=False)
            df.to_excel(self.__writer, sheet_name=sheet, startcol=scol, startrow=srow + row + 1, index=False)

    def __write_used_ranks(self, expert):
        used_ranks = expert.used_comb_ranks
        len_ranks = len(expert.ranks)
        name_sheet = "total_used_ranks"
        df = DataFrame.from_dict({row: comb
                                  for row, comb in enumerate(used_ranks.keys(), start=1)}, orient=INDEX)
        df.columns = pd.MultiIndex.from_tuples(zip(["Комбинации рангов"] * len_ranks, list(range(1, len_ranks + 1))))
        df.to_excel(self.__writer, sheet_name=name_sheet, startcol=0, startrow=0)
        transpose_used = list(zip(*map(dict.values, used_ranks.values())))
        headers = (("Количество в нормальных матрицах решений", "uniq"),
                   ("Количество в нормальных матрицах решений", "total"),
                   ("Количество в подходящих матрицах решений", "uniq"),
                   ("Количество в подходящих матрицах решений", "total")
                   )
        df = DataFrame.from_dict({head: item for head, item in zip(headers, transpose_used)})
        df.index = [""] * len(used_ranks.keys())
        col = len_ranks + 1
        df.to_excel(self.__writer, sheet_name=name_sheet, startcol=col, startrow=0)
        worksheet = self.__writer.sheets[name_sheet]
        row = len(used_ranks.keys())
        colors = ["#ff7f0e", "#3a4feb", "#b208f1", "#1f77b4"]
        width_columns = [25, 23, 19, 24]
        for i, (color, width) in enumerate(zip(colors, width_columns), start=1):
            worksheet.conditional_format(3, col + i, 3 + row, col + i, {"type": "data_bar", "bar_color": color,
                                                                        "bar_border_color": color,
                                                                        'bar_axis_color': '#FFFFFF'})
            worksheet.set_column(col + i, col + i, width)

    def __insert_images(self, expert):
        name_sheet = "images"
        sheet = self.__writer.book.add_worksheet(name_sheet)
        row, col = 0, 0
        row, col = self.__insert_pie(sheet, name_sheet, expert, row, col)
        row, col = self.__insert_errorbars(sheet, name_sheet, expert, row, col)
        row, col = self.__insert_bar(sheet, name_sheet, expert, row, col)

    def __insert_pie(self, sheet, name_sheet, expert, row, col):
        name_fig = self.__main_dir / "Диаграммы" / "выбор_матриц_экспертом.png"
        matrices = {mtype: len(matrices) for mtype, matrices in expert.all_matrices.items()}
        all_matrices = expert.total_matrices
        if sum(matrices.values()) != all_matrices:
            matrices[UNSAVED_TYPE_MATRIX] = all_matrices - sum(matrices.values()) + matrices[UNSAVED_TYPE_MATRIX]
        matrices = {mtype: el for mtype, el in zip(TYPES_MATRICES, matrices.values())}
        label = "Количество матриц"
        df = DataFrame.from_records([matrices], index=["total:"])
        df.columns = pd.MultiIndex.from_tuples(zip([label] * len(TYPES_MATRICES), TYPES_MATRICES))
        self.__style_df(df, [[(label, mtype)] for mtype in TYPES_MATRICES], [True] * len(TYPES_MATRICES),
                        [{"border": f"3px solid {MTYPES_COLORS[mtype]}"} for mtype in TYPES_MATRICES])\
            .to_excel(self.__writer, sheet_name=name_sheet, startcol=col, startrow=row)
        sheet.insert_image(row, col + len(matrices.keys()) + 1, name_fig, {"x_scale": 0.8, "y_scale": 0.8})
        row += 19
        return row, col

    def __insert_errorbars(self, sheet, name_sheet, expert, row, col):
        saved, mtypes = expert.get_saved_stats_from_matrices()
        srow, scol = row, col
        ylabels = {"hi^2": "Критерий хи-квадрат", "W": "Значение конкордации", "p": "Коэффициент значимости",
                   "eps": "Максимальная разница между весами"}
        cols = ["min", "avg", "max"]
        in_dir = self.__main_dir / "Диаграммы"
        for i, (stat, item) in enumerate(saved.items()):
            name_fig = in_dir / f"стат_показ_матриц_{stat}.png"
            yerr_min = array([el["min"] for el in item.values()])
            yerr_max = array([el["max"] for el in item.values()])
            yerr_avg = mean([yerr_max, yerr_min], axis=0)
            yerrs = zip(yerr_min, yerr_avg, yerr_max)
            columns = pd.MultiIndex.from_tuples(zip([ylabels[stat]] * 3, cols))
            df = DataFrame.from_records([{"min": mini, "avg": avg, "max": maxi} for mini, avg, maxi in yerrs],
                                        index=mtypes)
            df.columns = columns
            df.to_excel(self.__writer, sheet_name=name_sheet, startrow=row, startcol=scol)
            sheet.insert_image(srow, scol + len(cols) + 1, name_fig, {"x_scale": 0.8, "y_scale": 0.8})
            scol += 12
        row += 19
        return row, col

    def __insert_bar(self, sheet, name_sheet, expert, row, col):
        ylabels = {"hi^2": "Больше табличного хи-квадрат", "W": "Значение конкордации в промежутке",
                   "W and hi^2": "Выполнены хи-квадрат и знач. конкордации",
                   "eps": "Максимальная разница весов меньше заданной"}
        met_conds = expert.met_conds
        total_matrices = expert.total_matrices
        unmet_conds = {key: total_matrices - met for key, met in met_conds.items()}
        conds = ["Выполнено", "Не выполнено"]
        colors = ["#1f77b4", "#ff7f0e"]
        srow = row
        for met, unmet, (stat, label) in zip(met_conds.values(), unmet_conds.values(), ylabels.items()):
            columns = pd.MultiIndex.from_tuples(zip([label] * 2, conds))
            df = DataFrame.from_records([{conds[0]: met, conds[1]: unmet}], index=[stat])
            df.columns = columns
            df = self.__style_df(df, [[(label, "Выполнено")], [(label, "Не выполнено")]], [True] * 2,
                                 [{"border": f"3px solid {c}"} for c in colors])
            df.to_excel(self.__writer, sheet_name=name_sheet, startcol=col, startrow=srow)
            srow += 5
        name_fig = self.__main_dir / "Диаграммы" / "выполненные_условия.png"
        sheet.insert_image(row, col + len(conds) + 1, name_fig, {"x_scale": 0.8, "y_scale": 0.8})
        row += 19 if 5 * len(ylabels.keys()) < 19 else 5 * len(ylabels.keys()) + 4
        return row, col

    @staticmethod
    def __generator_row_col(row, col, add_to_row, add_to_col):
        border_cols = 50 * col
        scol, srow = 0, 0
        while True:
            yield srow, scol
            scol += col + add_to_col
            if scol >= border_cols:
                srow += row + add_to_row
                scol = 0

    @staticmethod
    def __style_df(df, cols, conditions, if_trues, if_falses=None, mode=ALL_ROWS):
        if if_falses is None:
            if_falses = [{}] * len(conditions)
        if type(if_trues) is dict:
            if_trues = [if_trues] * len(conditions)
        if type(if_falses) is dict:
            if_falses = [if_falses] * len(conditions)
        df = df.style
        for col, cond, true, false in zip(cols, conditions, if_trues, if_falses):
            if mode == ALL_ROWS:
                df = df.set_properties(subset=col, **(true if cond else false))
            elif mode == APPLY:
                pass
        return df

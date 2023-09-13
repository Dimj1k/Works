from .matrix import SolverMatrix, chi2
from itertools import product, repeat
from numpy import (
    unique
)
from random import shuffle, randint
TYPES_MATRICES = ("best", "normal", "abnormal")
SAVING_STATS_FROM_MATRICES = {"hi^2": (("min", float("inf")), ("max", -float("inf"))),
                              "W": (("min", float("inf")), ("max", -float("inf"))),
                              "p": (("min", float("inf")), ("max", -float("inf"))),
                              "eps": (("min", float("inf")), ("max", -float("inf")))
                              }
SAVING_DONE_CONDS = {"hi^2": 0, "W": 0, "W_hi^2": 0, "eps": 0}
UNSAVED_TYPE_MATRIX = TYPES_MATRICES[2]
FROM_RANKS_SAVED = (('uniq', 0), ('total', 0), ("in_best_uniq", 0), ("in_best_total", 0))
SAVING_BEST_MIN_EPS_MATRIX = {mtype: SolverMatrix for mtype in TYPES_MATRICES}


class Expert:

    def __init__(self, weights, num_expert, w_user, hi2_table, eps):
        self.weights = weights
        self.num_rows = num_expert
        self.all_matrices: dict[str: list[SolverMatrix]] = {mtype: [] for mtype in TYPES_MATRICES}
        self.__saving_stats_from_matrices = {save: {mtype: dict(save_item)
                                                    for mtype, save_item in
                                                    zip(TYPES_MATRICES, repeat(SAVING_STATS_FROM_MATRICES[save]))}
                                             for save in SAVING_STATS_FROM_MATRICES.keys()}
        self.met_conds = {save: item for save, item in SAVING_DONE_CONDS.items()}
        self.best_min_eps_matrices: dict[str: SolverMatrix] = {mtype: item
                                                               for mtype, item in SAVING_BEST_MIN_EPS_MATRIX.items()}
        self.W_user = w_user
        self.hi2_table = hi2_table
        self.eps = eps
        self.total_matrices = None
        self.__combs_ranks = []
        self.used_comb_ranks = None

    def analyze(self, combs_ranks, amount_save_matrices=1e5, max_best=float("inf")):
        self.total_matrices = len(combs_ranks) ** self.num_rows if max_best == float("inf") else 0
        self.used_comb_ranks = {comb: dict(FROM_RANKS_SAVED) for comb in combs_ranks}
        if max_best == float("inf"):
            self.__combs_ranks = combs_ranks
            self.__cpu_analyze_one(amount_save_matrices)
        else:
            self.__combs_ranks = self.__shuffle(combs_ranks[:])
            self.__cpu_analyze_one_with_max(amount_save_matrices, max_best)
        return self

    @staticmethod
    def __shuffle(combs):
        shuffle(combs)
        return combs

    def get_info_matrices(self):
        return {mtype: map(SolverMatrix.info, matrices)
                for mtype, matrices in self.all_matrices.items()
                if self.all_matrices[mtype]}

    def get_saved_stats_from_matrices(self):
        first_key = next(iter(SAVING_STATS_FROM_MATRICES))
        saving = self.__saving_stats_from_matrices
        s = saving[first_key]
        mtypes = [mtype for mtype in TYPES_MATRICES if all(el not in (float("inf"), None) for el in s[mtype].values())]
        new_saving = {save: {mtype: item[mtype] for mtype in mtypes} for save, item in saving.items()}
        return new_saving, mtypes

    def __cpu_analyze_one(self, amount_save_matrices):
        combs_matrix = product(self.__combs_ranks, repeat=self.num_rows)
        if amount_save_matrices != float("inf"):
            for i, comb in enumerate(combs_matrix, start=1):
                solver_matrix = SolverMatrix(comb, i)
                type_matrix = self.__what_is_matrix(solver_matrix)
                if type_matrix == UNSAVED_TYPE_MATRIX:
                    if len(self.all_matrices[type_matrix]) < amount_save_matrices:
                        self.all_matrices[type_matrix].append(solver_matrix)
                    elif solver_matrix.eps < self.eps:
                        self.all_matrices[type_matrix][randint(0, amount_save_matrices - 1)] = solver_matrix
                else:
                    self.all_matrices[type_matrix].append(solver_matrix)
                self.__save_something_from_matrix(solver_matrix, type_matrix)
        else:
            for i, comb in enumerate(combs_matrix, start=1):
                solver_matrix = SolverMatrix(comb, i)
                type_matrix = self.__what_is_matrix(solver_matrix)
                self.all_matrices[type_matrix].append(solver_matrix)
                self.__save_something_from_matrix(solver_matrix, type_matrix)
        self.__save_p()

    def __cpu_analyze_one_with_max(self, amount_save_matrices, max_best):
        combs_matrix = product(self.__combs_ranks, repeat=self.num_rows)
        if amount_save_matrices != float("inf"):
            for i, comb in enumerate(combs_matrix, start=1):
                solver_matrix = SolverMatrix(comb, i)
                type_matrix = self.__what_is_matrix(solver_matrix)
                self.total_matrices += 1
                if type_matrix == UNSAVED_TYPE_MATRIX:
                    if len(self.all_matrices[type_matrix]) < amount_save_matrices:
                        self.all_matrices[type_matrix].append(solver_matrix)
                    elif solver_matrix.eps < self.eps:
                        self.all_matrices[type_matrix][randint(0, amount_save_matrices - 1)] = solver_matrix
                else:
                    self.all_matrices[type_matrix].append(solver_matrix)
                    if len(self.all_matrices["best"]) >= max_best:
                        self.__save_something_from_matrix(solver_matrix, type_matrix)
                        break
                self.__save_something_from_matrix(solver_matrix, type_matrix)
        else:
            for i, comb in enumerate(combs_matrix, start=1):
                solver_matrix = SolverMatrix(comb, i)
                type_matrix = self.__what_is_matrix(solver_matrix)
                self.total_matrices += 1
                self.all_matrices[type_matrix].append(solver_matrix)
                self.__save_something_from_matrix(solver_matrix, type_matrix)
                if len(self.all_matrices["best"]) >= max_best:
                    break
        self.__save_p()

    def __save_something_from_matrix(self, matrix, mtype):
        self.__save_hi2(matrix, mtype)
        self.__save_w(matrix, mtype)
        self.__save_eps(matrix, mtype)

    def __save_hi2(self, matrix, mtype):
        saving = self.__saving_stats_from_matrices["hi^2"][mtype]
        if matrix.hi2 < saving["min"]:
            saving["min"] = matrix.hi2
        if matrix.hi2 > saving["max"]:
            saving["max"] = matrix.hi2

    def __save_w(self, matrix, mtype):
        saving = self.__saving_stats_from_matrices["W"][mtype]
        if matrix.W < saving["min"]:
            saving["min"] = matrix.W
        if matrix.W > saving["max"]:
            saving["max"] = matrix.W

    def __save_eps(self, matrix, mtype):
        saving = self.__saving_stats_from_matrices["eps"][mtype]
        if matrix.eps < saving["min"]:
            self.best_min_eps_matrices[mtype] = matrix
            saving["min"] = matrix.eps
        if matrix.eps > saving["max"]:
            saving["max"] = matrix.eps

    def __save_p(self):
        saving = self.__saving_stats_from_matrices
        for mtype, el in zip(TYPES_MATRICES, saving["hi^2"].values()):
            saving["p"][mtype]["min"] = 1 - chi2.cdf(el["max"], len(self.weights) - 1)\
                if el["max"] != -float("inf") else None
            saving["p"][mtype]["max"] = 1 - chi2.cdf(el["min"], len(self.weights) - 1)\
                if el["min"] != float("inf") else None

    def __what_is_matrix(self, matrix):
        is_norm_matrix = self.__matrix_is_normal(matrix)
        matrix.max_eps_with_weights(self.weights)
        eps_is_best = self.__check_eps(matrix)
        if is_norm_matrix:
            mtype = "best" if eps_is_best else "normal"
            self.__save_combs(matrix, mtype)
            return mtype
        return "abnormal"

    def __save_combs(self, matrix, mtype):
        saving = self.used_comb_ranks
        ranks, counts = unique(matrix.ranks_matrix, axis=0, return_counts=True)
        if mtype == "best":
            for comb, count in zip(map(tuple, ranks), counts):
                save_here = saving[comb]
                # save_here["uniq"] += 1
                # save_here["total"] += count
                save_here["in_best_uniq"] += 1
                save_here["in_best_total"] += count
            return
        for comb, count in zip(map(tuple, ranks), counts):
            save_here = saving[comb]
            save_here["uniq"] += 1
            save_here["total"] += count

    def __check_eps(self, matrix):
        if matrix.eps <= self.eps:
            self.met_conds["eps"] += 1
            return True
        return False

    def __matrix_is_normal(self, matrix):
        if all([self.__matrix_w_norm(matrix), self.__matrix_hi2_norm(matrix)]):
            self.met_conds["W_hi^2"] += 1
            return True
        return False

    def __matrix_w_norm(self, matrix):
        if self.W_user["left"] <= matrix.W <= self.W_user["right"]:
            self.met_conds["W"] += 1
            return True
        return False

    def __matrix_hi2_norm(self, matrix):
        if matrix.hi2 >= self.hi2_table:
            self.met_conds["hi^2"] += 1
            return True
        return False

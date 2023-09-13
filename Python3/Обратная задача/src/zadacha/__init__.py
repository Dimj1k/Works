from .expert import Expert, UNSAVED_TYPE_MATRIX, TYPES_MATRICES
from .states_zadacha import StateZadacha
from collections import Counter
from itertools import (
    product,
    permutations
)
from scipy.stats import chi2
from numpy import (
    array,
    unique,
    float32,
)


class Zadacha:

    __actual_expert: Expert
    state = StateZadacha.START

    def __init__(self, data, user_stats, use_all_ranks, num_experts, max_best, amount_save_matrices):
        self.data = data
        self.num_experts = range(1, num_experts + 1) \
            if type(num_experts) is int else range(num_experts[0], num_experts[1] + 1)
        self.user_stats = self.__change_stats(user_stats)
        self.ranks = self.__rank_data(self.data)
        self.all_combs_ranks = self.__use_all_ranks() if use_all_ranks else self.__use_existed_ranks()
        self.weights = self.__data_to_weights()
        self.amount_save = amount_save_matrices
        self.saved_info_from_experts = {"stats": [], "amount": {mtype: [] for mtype in TYPES_MATRICES},
                                        "weights": {mtype: [] for mtype in TYPES_MATRICES}}
        self.max_best = max_best
        self.__min_eps = []
        self.experts: tuple[Expert] = self.__generator_experts()

    def solve(self):
        for num_rows, expert in enumerate(self.experts, start=1):
            if self.state == StateZadacha.CONTINUE or self.state == StateZadacha.START:
                self.__actual_expert = expert
                self.__actual_expert.analyze(self.all_combs_ranks, self.amount_save, self.max_best)
                self.__check_state()
                self.__save_something_from_expert()
                yield self.__actual_expert
            else:
                raise GeneratorExit("state != 'State.CONTINUE'")

    def __check_state(self):
        info, mtypes = self.__actual_expert.get_saved_stats_from_matrices()
        self.__save_stats(info)
        if "best" in mtypes:
            self.state = StateZadacha.BEST_FINDED
            return
        if "normal" in mtypes:
            eps_actual = info["eps"]["normal"]["min"]
            if self.__min_eps:
                prev_eps = self.__min_eps[-1]
                if prev_eps <= eps_actual:
                    self.state = StateZadacha.NOT_CONVERGE
            self.__min_eps.append(eps_actual)
            return
        self.state = StateZadacha.CONTINUE

    def __save_something_from_expert(self):
        pass
        # self.__save_amount_matrices()
        # self.__save_bests_weights()

    def __save_stats(self, info):
        self.saved_info_from_experts["stats"].append(info)

    def __change_stats(self, stats):
        return {"w_user": {"left": stats["w_user"]["left"], "right": stats["w_user"]["right"]},
                "hi2_table": chi2.ppf(1 - stats["p_user"], len(self.data) - 1),
                "eps": stats["eps"]
                }

    @staticmethod
    def __rank_data(data):
        c = Counter(data)
        rv = {}
        k = 1
        for i in sorted(c.keys()):
            if c[i] == 1:
                rv[i] = k
                k += 1
            else:
                v = c[i]
                rv[i] = (2 * k + v - 1) / 2
                k += v
        return array([rv[k] for k in data], dtype=float32)

    def __use_existed_ranks(self):
        return list(map(tuple, unique([*permutations(self.ranks)], axis=0).tolist()))

    def __use_all_ranks(self):
        k = len(self.data)
        return list(map(tuple, unique([self.__rank_data(data)
                                       for data in product(range(k), repeat=k)], axis=0).tolist()))

    def __data_to_weights(self):
        return array(self.data) / sum(self.data)

    def __generator_experts(self):
        return (Expert(self.weights, i, **self.user_stats) for i in self.num_experts)

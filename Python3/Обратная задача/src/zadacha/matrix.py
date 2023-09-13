from numpy import (
    var,
    sum as npsum,
    array,
    float64,
    max as npmax,
    abs as npabs
)
from scipy.stats import chi2


class SolverMatrix:

    eps = None

    def __init__(self, ranks, variant):
        self.ranks_matrix = array(ranks, dtype=float64)
        self.variant = variant
        self.W, self.hi2, self.p = self.__stats()

    def max_eps_with_weights(self, other_weights):
        self.eps = npmax(npabs(other_weights - self.weights))

    def info(self):
        return {
            "ranks": self.ranks_matrix,
            "id": self.variant,
            "W": self.W,
            "hi2": self.hi2,
            "p": self.p,
            "weights": self.weights,
            "eps": self.eps
        }

    def __stats(self):
        m, n = self.ranks_matrix.shape
        denom = m ** 2 * (n ** 3 - n)
        rating_sums = npsum(self.ranks_matrix, axis=0)
        self.weights = rating_sums / npsum(self.ranks_matrix)
        s = n * var(rating_sums)
        hi2 = 12 * s / (m * n * (n + 1))
        w = 12 * s / denom
        return w, hi2, 1 - chi2.cdf(hi2, n - 1)

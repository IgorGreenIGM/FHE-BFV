"""
Algorithme de la transformation numérique de fourrier
"""

import math
from utils import *

def transform_fourrier(coefs: list, w_table, corps_q):
    """
    Arguments:
        coefs (list): liste contenant les coefficients du polynôme dans le domaine standard
        w_table : tableau contenant les racines de l'unité w^k dans le corps fini q, utilisées comme facteurs de twiddle
        corps_q : modulo du corps fini sur lequel sont définis les coefficients des polynômes
    """

    degre = len(coefs)
    results = [x for x in coefs]
    v = int(math.log(degre, 2))

    for i in range(0, v):
        for j in range(0, 2 ** i):
            for k in range(0, 2 ** (v - i - 1)):
                s = j * (2 ** (v - i)) + k
                t = s + (2 ** (v - i - 1))

                w = w_table[(2 ** i) * k]
                as_temp = results[s]
                at_temp = results[t]

                results[s] = (as_temp + at_temp) % corps_q
                results[t] = ((as_temp - at_temp) * w) % corps_q

    results = indexReverse(results, v)
    return results


def inverse_transform_fourrier(coefs: list, w_table, corps_q):
    """
    Arguments:
        coefs (list): liste contenant les coefficients du polynôme dans le domaine de fourrier
        w_table : tableau contenant les racines de l'unité w^k dans le corps fini q
        corps_q : modulo du corps fini sur lequel sont définis les coefficients des polynômes
    """

    degre = len(coefs)
    results = [x for x in coefs]
    v = int(math.log(degre, 2))

    for i in range(0, v):
        for j in range(0, (2 ** i)):
            for k in range(0, (2 ** (v - i - 1))):
                s = j * (2 ** (v - i)) + k
                t = s + (2 ** (v - i - 1))

                w = w_table[((2 ** i) * k)]
                as_temp = results[s]
                at_temp = results[t]

                results[s] = (as_temp + at_temp) % corps_q
                results[t] = ((as_temp - at_temp) * w) % corps_q

    results = indexReverse(results, v)
    degre_inv = modinv(degre, corps_q)
    for i in range(degre):
        results[i] = (results[i] * degre_inv) % corps_q

    return results
import os
import sys
import time
import pickle
from BFV import *
from BFV import BFV
from utils import *

from random import randint
from math import log, ceil

def init_evaluator(t=16, n=1024, q=132120577, psi=73993) -> BFV:
    psiv= modinv(psi,q)
    w   = pow(psi,2,q)
    wv  = modinv(w,q)
    mu, sigma = 0, 0.5 * 3.2
    T = 256
    p = q**3 + 1
    w_table    = [1]*n
    wv_table   = [1]*n
    psi_table  = [1]*n
    psiv_table = [1]*n
    for i in range(1,n):
        w_table[i]    = ((w_table[i-1]   *w)    % q)
        wv_table[i]   = ((wv_table[i-1]  *wv)   % q)
        psi_table[i]  = ((psi_table[i-1] *psi)  % q)
        psiv_table[i] = ((psiv_table[i-1]*psiv) % q)

    qnp = [w_table,wv_table,psi_table,psiv_table]
    Evaluator = BFV(n, q, t, mu, sigma, qnp)
    Evaluator.GenererCleSecrete()
    Evaluator.GenererClePublique()
    return Evaluator


with open("HAddition.txt", mode='w') as fp:
    Evaluator = init_evaluator()
    for i in range(2**10000):
        n1, n2 = 2**i, 2**i
        m1 = Evaluator.IntEncode(n1); m2 = Evaluator.IntEncode(n2)
        ct1 = Evaluator.Chiffrer(m1); ct2 = Evaluator.Chiffrer(m2)
        t1 = time.time()
        ct = Evaluator.HomomorphicAddition(ct1, ct2)
        fp.write("{} {:.2f}\n".format(2**i, time.time() - t1))
        fp.flush()
        
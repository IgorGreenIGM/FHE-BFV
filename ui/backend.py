from BFV import *
from math import log, ceil

t = 16
n : int
q: int
psi: int
psiv : int
w : int
wv : int

mu: float
sigma : float

T = 0
p = 0

qnp : list

w_table    : list
wv_table   : list
psi_table  : list
psiv_table : list

Evaluator : BFV

def init_params(mu, sigma, n, q, psi):
    n = n
    q = q
    psi = psi
    sigma = sigma
    mu  =mu

    psiv = modinv(psi,q)
    w = pow(psi, 2, q)
    wv = modinv(w, q)

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

    # Création de l'evaluateur
    Evaluator = BFV(n, q, t, mu, sigma, qnp)

    return Evaluator
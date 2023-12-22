import pandas as pd
import pickle
import os

noms = [
        "Mogou Igor", 
        "Fezeu Freddy",
        "Tchassi Daniel", 
        "Temgoua kros", 
        "Solefack Daniel", 
        "Mekiage Oliver", 
        "Mbassi Loic", 
        "Pacome F. K.",
        "Gabriel Ada",
        "Laelle Ingrid Olivier",
        "Laelle-3GC Olivier",
        "Laelle-Fortune Oliver",
        "Tale Kalachi"
        ]

salaires = [
            700_000,
            600_000,
            350_000,
            250_000,
            100_000,
            750_000,
            400_000,
            515_000,
            175_000,
            225_000,
            145_000,
            360_000,
            50_000
            ]

augmentations = [
                20_000,
                15_000,
                25_000,
                15_000,
                7_500,
                9_000,
                10_000,
                5_000,
                17_500,
                14_750,
                21_500,
                18_000, 
                4_000
                ]

mdict = {'nom':noms, "salaires":salaires, "augmentations":augmentations}
df = pd.DataFrame(mdict)
print(df)


from BFV import *
from utils import *

from random import randint
from math import log, ceil


t = 16;   n, q, psi = 1024, 132120577, 73993
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
Evaluator.EvaluerGenererCleV1(T)

# chiffrement des salaires
for i in range(len(df['salaires'])):
    n1 = df["salaires"][i]

    m = Evaluator.IntEncode(n1); e = Evaluator.Chiffrer(m)
    with open(f"encrypted/salaire_{i}.pkl", mode='wb') as fp:
        pickle.dump(e, fp)

# chiffrement des augmentations
for i in range(len(df['augmentations'])):
    n1 = df["augmentations"][i]

    m = Evaluator.IntEncode(n1); e1 = Evaluator.Chiffrer(m)
    with open(f"encrypted/augmentations_{i}.pkl", mode='wb') as fp:
        pickle.dump(e1, fp)

with open("pk.pkl", mode="wb") as fpk:
    pickle.dump(Evaluator.pk, fpk)

with open("sk.pkl", mode="wb") as fsk:
    pickle.dump(Evaluator.sk, fsk)
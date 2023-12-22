import json
import pickle
import pandas as pd

from BFV import *
from utils import *

conf = dict()
with open("config.json", mode="r") as config:
    conf = json.load(config)
    
t = conf['t'];   n, q, psi = conf['n'], conf['q'], conf['psi']
psiv= modinv(psi,q)
w   = pow(psi,2,q)
wv  = modinv(w,q)
mu, sigma = conf['mu'], conf['sigma']

T = conf['T']
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

with open("sk.pkl", mode='rb') as fsk_in:
    Evaluator.sk = pickle.loads(fsk_in.read())

with open("pk.pkl", mode='rb') as fpk_in:
    Evaluator.pk = pickle.loads(fpk_in.read())

resultats = []
for i in range(conf['size']):
    with open(f"results/results{i}.pkl", mode="rb") as fp1:
        ct = pickle.loads(fp1.read())
        mt = Evaluator.Dechiffrer(ct)
        r = Evaluator.IntDecode(mt)
        resultats.append(r)


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

mdict = {'nom':noms, "salaires apres aug":resultats}
df = pd.DataFrame(mdict)
print(df)
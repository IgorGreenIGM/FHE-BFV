import json
import pickle

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

with open("pk.pkl", mode='rb') as fpk_in:
    Evaluator.pk = pickle.loads(fpk_in.read())


for i in range(conf['size']):
    with open(f"encrypted/salaire_{i}.pkl", mode="rb") as fp1:
        with open(f"encrypted/augmentations_{i}.pkl", mode="rb") as fp2:
            ct1 = pickle.loads(fp1.read())
            ct2 = pickle.loads(fp2.read())

            ct = Evaluator.HomomorphicAddition(ct1, ct2)
            with open(f"results/results{i}.pkl", mode="wb") as f_out:
                pickle.dump(ct, f_out)
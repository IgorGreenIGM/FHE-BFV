from BFV import *
from utils import *

from random import randint
from math import log, ceil

"""
    n : taille de l'anneau
    q : modulo des données chiffrées
    t : modulo des données non chiffrées
    psi, psiv, w, wv : parametres d'arithmetique polynomiale
"""

# géneration des paramtètres pour le BFV
# Select one of the parameter sets below
t = 16;   n, q, psi = 1024 , 132120577         , 73993                # log(q) = 27
# t = 256;  n, q, psi = 2048 , 137438691329      , 22157790             # log(q) = 37
# t = 1024; n, q, psi = 4096 , 288230376135196673, 60193018759093       # log(q) = 58

# other necessary parameters
psiv= modinv(psi,q)
w   = pow(psi,2,q)
wv  = modinv(w,q)
# paramètres de génération aléatoire uniforme
mu, sigma = 0, 0.5 * 3.2

# t : relinearisation
# p : clé galoise
T = 256
p = q**3 + 1

# generation des tables d'arithmetique polynomiale
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


print("=======| Début de la Démonstration BFV |=======")
Evaluator = BFV(n, q, t, mu, sigma, qnp)

Evaluator.GenererCleSecrete()
Evaluator.GenererClePublique()
Evaluator.EvaluerGenererCleV1(T)
# Evaluator.EvaluerGenererCleV2(p)

print("BFV : \n==============================================\n", Evaluator)

# generation de deux nombres aléatoirement : 
n1, n2 = randint(-(2**15),2**15-1), randint(-(2**15),2**15-1)

print("Nombre n1 et n2 généré aleatoirement.")
print("* n1: ", n1)
print("* n2: ", n2)


# Encodage des message dans l'anneau des polynôme plaintext
print("n1 and n2 sont encodés comme les polynomes m1(x) and m2(x).")
m1 = Evaluator.IntEncode(n1)
m2 = Evaluator.IntEncode(n2)
print("* m1(x): ", m1)
print("* m2(x): ", m2)

# chrifrement des messages
ct1 = Evaluator.Chiffrer(m1)
ct2 = Evaluator.Chiffrer(m2)

print("--- m1 and m2 sont chiiffrés comme ct1 et ct2.")
print("* ct1[0]: {}".format(ct1[0]))
print("* ct1[1]: {}".format(ct1[1]))
print("* ct2[0]: {}".format(ct2[0]))
print("* ct2[1]: {}".format(ct2[1]))
print("")

# Réalisation de différentes opérations : 
ct = Evaluator.HomomorphicAddition(ct1, ct2)
mt = Evaluator.Dechiffrer(ct)
nr = Evaluator.IntDecode(mt)

print("Résultat initial : ", n1 + n2)
print("Resultat chiffré : ", nr)

from BFV.BFV import *

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
    Evaluator.EvaluerGenererCleV1(256)
    return Evaluator


def boostrap(message, Evaluator):
    pk1 = Evaluator.pk
    sk1 = Evaluator.sk

    # generer une seconde paire de clés
    Evaluator2 = init_evaluator()
    pk2 = Evaluator2.pk
    sk2 = Evaluator2.sk

    # chiffrer la premiere clé secrete avec la seconde avec la seconde
    Evaluator2.pk = sk2
    csk1 = Evaluator2.Chiffrer(sk1)
    Evaluator2.pk = pk2

    # chiffrer le message avec la deuxieme clé publique
    cct = Evaluator2.Chiffrer(message)

    # déchiffrer le message
    Evaluator2.sk = csk1
    return Evaluator2.Dechiffrer(cct)
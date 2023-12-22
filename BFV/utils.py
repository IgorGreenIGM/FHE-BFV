"""
Fonctions de calculs utilitaires
"""

from random import randint
from premier import *


def egcd(a, b):
    """algorithme du modulo inverse d'entiers. on cherche x tq ax congru a 1 modulo n 
    il calcul à la fois le pgcd et les coefficients de bézout d'un couple entier (a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b%a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Le modulo inverse de cet entier n'exsite pas")
    else:
        return x % m
    
def gcd(n1, n2):
    """ 
        algorithme du pcgd
    """
    a = n1
    b = n2
    while b != 0:
        a, b = b, a%b
    return a 

def intReverse(a, n):
    """
        bit-reverse integer
    """
    b = ('{:0' + str(n)+'b}').format(a)
    return int(b[::-1], 2)

def indexReverse(a, r):
    n = len(a)
    b = [0] * n
    for i in range(n):
        rev_idx = intReverse(i, r)
        b[rev_idx] = a[i]
    
    return b


def RefPolMul(A, B, M):
    """
    Multiplication polynomiale (Reference)
    avec f(x) = x^n + 1
    """
    C = [0] * (2 * len(A))
    D = [0] * (len(A))
    for indexA, elemA in enumerate(A):
        for indexB, elemB in enumerate(B):
            C[indexA + indexB] = (C[indexA + indexB] + elemA * elemB) % M

    for i in range(len(A)):
        D[i] = (C[i] - C[i + len(A)]) % M
    return D


def RefPolMulv2(A, B):
    """ 
    Multiplication polynomiale (Reference) avec (w/ modulus)
    et f(x) = x^n + 1
    """
    C = [0] * (2 * len(A))
    D = [0] * (len(A))
    for indexA, elemA in enumerate(A):
        for indexB, elemB in enumerate(B):
            C[indexA + indexB] = (C[indexA + indexB] + elemA * elemB)

    for i in range(len(A)):
        D[i] = (C[i] - C[i + len(A)])
    return D

def estRacineUnite(w, m, q):
    """
        vérifie si m-ieme (peut etre n ou 2n) racine de l'unité du corps q
    """
    if w == 0:
        return False
    elif pow(w, m//2, q) == q - 1:
        return True
    else:
        return False
    
def ntt_premier(n, logq):
    factor = 2 * n
    value = (1 << logq) - factor + 1
    lbound = (1 << (logq - 1))

    while (value > lbound):
        if (est_premier(value)) == True:
            return value
        else:
            value = value - factor
    raise Exception("Impossible d'obtenir un nombre premier pour la ntt")

def trouver_racine(m, q):
    """
        retourne une racine de l'unité dans le corps q
    """
    g = (q - 1) // m

    if (q-1) != g*m:
        return False

    attempt_ctr = 0
    attempt_max = 100
    
    while(attempt_ctr < attempt_max):
        a = randint(2,q-1)
        b = pow(a,g,q)
        # check 
        if estRacineUnite(b,m,q):
            return True,b
        else:
            attempt_ctr = attempt_ctr+1
        
    return True,0

# generer les paramètres nécessaires du BFV
def genererBFV_params(n, logq):
    pfound = False
    while not(pfound):
        # on cherche un entier premier
        q = ntt_premier(n, logq)
        # on recherche une racine
        pfound, psi = trouver_racine(2*n, q)
    
    psiv = modinv(psi, q)
    w = pow(psi, 2, q)
    wv = modinv(w, q)
    return q, psi, psiv, w, wv


def get_superscript_unicode(number):
    superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return str(number).translate(superscript_digits)
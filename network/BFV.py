# BFV

from polynome import *

class BFV:
    """
    Definitions
    Z_q[x]/f(x) = x^n + 1 ou n est une puissance de 2

    Operations
    -- GenererCleSecrete
    -- GenererClePublique
    -- Chiffrer
    -- Dehiffrer
    -- DechiffrerV2
    -- EvaluerGenererCle
    -- HomAdd
    -- HomMult
    -- RelinV1

    Paramètre
    (Ceux ci sont fourni avec le constructeur)
    -- n (taille de l'anneau)
    -- q (module de l'anneau des messages chiffré)
    -- t (module de l'anneau des messages en clair)
    -- mu (moyenne de la loi de gauss utilisée pour générer les erreurs aléatoires lors du chiffrement)
    -- sigma (écart type de la loi de gauss utilisée pour générer les erreurs aléatoires lors du chiffrement)
    -- qnp (tableau de paramètres NTT (Number Theoretic Transform) utilisés dans les calculs: [w,w_inv,psi,psi_inv])
    (Ceux ci sont généré par la classe a l'aide des paramètre fourni par constructeur)
    -- sk (clé secrète utilisée pour le déchiffrement des messages)
    -- pk (clé publique utilisée pour le chiffrement des messages)
    -- rlk1(Clé d'évaluation les calculs homomorphes, clé de relinearisation)
    """

    #Constructeur de la classe qui prend les paramètres et les enregistres
    def __init__(self, n, q, t, mu, sigma, qnp):
        self.n = n
        self.q = q
        self.t = t
        self.T = 0
        self.l = 0
        self.p = 0
        self.mu = mu
        self.sigma = sigma
        self.qnp= qnp # tableau de paramètre NTT sous la forme [w,w_inv,psi,psi_inv]
        #initialisation des attributs qui seront génére
        self.sk = []
        self.pk = []
        self.rlk1 = []

    #Methode permetant a la classe d'afficher ses attributs
    def __str__(self):
        str = ""
        str = str + "n     :  	[ taille de l'anneau des polynômes                     					]    ->   {}\n".format(self.n)
        str = str + "q     :  	[ module de l'anneau des messages chiffré    					]    ->   {}\n".format(self.q)
        str = str + "t      :  	[ module de l'anneau des messages en clair					]    ->   {}\n".format(self.t)
        str = str + "mu :  	[ moyenne de la loi de gauss					]    ->   {}\n".format(self.mu)
        str = str + "sigma :      [ écart type de la loi de gauss						]    ->   {}\n".format(self.sigma)
        return str
    
    #Cette fonction génère une clé secrète pour le chiffrement homomorphe.
    def GenererCleSecrete(self):
        #La clé secrète ici n'est qu'un polynome aleatoire avec les coefficient appartenant à {-1, 0, 1}
        s = Polynome(self.n,self.q,self.qnp)
        s.randomize(2)
        self.sk = s
    
    #Génère une clé publique à partir de la clé secrète
    def GenererClePublique(self):
        #on genère deux polynome aleatoire a et e, a suivant une loi de gauss et e une loi uniforme
        a, e = Polynome(self.n,self.q,self.qnp), Polynome(self.n,self.q,self.qnp)
        a.randomize(self.q)
        e.randomize(0, domaine=False, type="gauss", mu=self.mu, sigma=self.sigma)
        #on applique la formule donne pour le calcul de la clé publique
        pk0 = -(a*self.sk + e)
        pk1 = a
        self.pk = [pk0,pk1]
    
    #Génère une clé d'évaluation pour la multiplication homomorphe
    def EvaluerGenererCleV1(self, T):
        self.T = T
        self.l = int(math.floor(math.log(self.q,self.T)))# l = E(log_T(q)) partie entière de log de q en base T

        rlk1 = []

        sk2 = (self.sk * self.sk) #Clé secrète au carré

        #On applique la formule pour chaque coefficient
        for i in range(self.l+1):
            #On génère deux polynome aléatoire ai et ei, ai suivant la loi de gauss et ei une loi uniforme 
            ai, ei = Polynome(self.n,self.q,self.qnp), Polynome(self.n,self.q,self.qnp)
            ai.randomize(self.q)
            ei.randomize(0, domaine=False, type="gauss", mu=self.mu, sigma=self.sigma)
            #On genere le polynome T dans l'anneau des cyphertext et on effectue le calcul de T^i*S² 
            Ts2 = Polynome(self.n,self.q,self.qnp)
            Ts2.fourrier = [((self.T**i)*j) % self.q for j in sk2.fourrier]

            #On recupère donc finalement la clé de relinéarisation
            rlki0 = Ts2 - (ai*self.sk + ei)
            rlki1 = ai

            rlk1.append([rlki0,rlki1])

        self.rlk1 = rlk1


    #Cette fonction chiffre un message donné 
    def Chiffrer(self, m):
        delta = int(math.floor(self.q/self.t))

        u, e1, e2 = Polynome(self.n,self.q,self.qnp), Polynome(self.n,self.q,self.qnp), Polynome(self.n,self.q,self.qnp)

        u.randomize(2)
        e1.randomize(0, domaine=False, type="gauss", mu=self.mu, sigma=self.sigma)
        e2.randomize(0, domaine=False, type="gauss", mu=self.mu, sigma=self.sigma)

        md = Polynome(self.n,self.q,self.qnp)
        md.fourrier = [(delta*x) % self.q for x in m.fourrier]

        c0 = self.pk[0]*u + e1
        c0 = c0 + md
        c1 = self.pk[1]*u + e2

        return [c0,c1]
    
    #Cette fonction dechiffre un message donné qui à été relinéarisé surtout parlant des message qui n'ont que deux composante
    #Cet a dire qeux qui ont subi principalement que l'addition, la soustraction ou la multiplication puis la relinéarisation
    def Dechiffrer(self, ct):
        m = ct[1]*self.sk + ct[0]
        m.fourrier = [((self.t*x)/self.q) for x in m.fourrier]
        m = round(m)
        m = m % self.t
        mr = Polynome(self.n,self.t,self.qnp)
        mr.fourrier = m.fourrier
        mr.dans_fourrier = m.dans_fourrier
        return mr

    #Cette fonction dechiffre un message donné sans qu'il soit relinéarisé surtout parlant des message qui ont 3 composantes
    #Cet à dire multiplication uniquement
    def DechiffrerV2(self, ct):
        sk2 = (self.sk * self.sk)
        m = ct[0]
        m = (m + (ct[1]*self.sk))
        m = (m + (ct[2]*sk2))
        m.fourrier = [((self.t * x) / self.q) for x in m.fourrier]
        m = round(m)
        m = m % self.t
        mr = Polynome(self.n,self.t,self.qnp)
        mr.fourrier = m.fourrier
        mr.dans_fourrier = m.dans_fourrier
        return mr
    
    #Lorsqu'on effectue une multiplication sur les textes chiffré, on obtient un message a trois composantes dans l'espace des chiffré
    #Cette fonction permet de ramener le messages à trois composantes a un message à 2 composantes dans l'espace des chiffrés
    def Relinearization(self,ct):
        c0 = ct[0]
        c1 = ct[1]
        c2 = ct[2]

        #On ecris C2 en base T
        c2i = []

        c2q = Polynome(self.n,self.q,self.qnp)
        c2q.fourrier = [x for x in c2.fourrier]

        for i in range(self.l+1):
            c2r = Polynome(self.n,self.q,self.qnp)

            for j in range(self.n):
                qt = int(c2q.fourrier[j]/self.T)
                rt = c2q.fourrier[j] - qt*self.T

                c2q.fourrier[j] = qt
                c2r.fourrier[j] = rt

            c2i.append(c2r)

        c0r = Polynome(self.n,self.q,self.qnp)
        c1r = Polynome(self.n,self.q,self.qnp)
        c0r.fourrier = [x for x in c0.fourrier]
        c1r.fourrier = [x for x in c1.fourrier]

        for i in range(self.l+1):
            c0r = c0r + (self.rlk1[i][0] * c2i[i])
            c1r = c1r + (self.rlk1[i][1] * c2i[i])

        return [c0r,c1r]
    
    #Cette fonction permet d'encoder un message clair lisible par l'utilisateur en un message
    #appartenant a l'anneau des polynomes des messages clair(plaintexts) avec des coefficients de la base 2
    def IntEncode(self,m):
        #On initialise un polynome dans l'anneau des messages clair, donc dans l'anneau de taille n et des coefficients <= t
        mr = Polynome(self.n, self.t)
        #Si l'entier(le message) qu'on veut coder est positif, on le convertit simplement en base 2 et chaque chiffre correspond a un coefficient
        if m >0:
            mt = m
            for i in range(self.n):
                mr.fourrier[i] = (mt % 2)
                mt      = (mt // 2)
        #Si par contre l'entier est negatif, on fait comme pareillement avec son opposé mais on remplace les coefficients unitaire par le module maximum des plaintext
        elif m<0:
            mt = -m
            for i in range(self.n):
                mr.fourrier[i] = (self.t-(mt % 2)) % self.t
                mt      = (mt // 2)
        else:
            mr = mr
        return mr
    
    #Cette fonction permet de decoder un message contenu dans l'anneau des polynomes des messages
    #clair en un message lisible par l'utilisateur
    def IntDecode(self,m):
        mr = 0
        thr_ = 2 if(self.t == 2) else ((self.t+1)>>1)
        for i,c in enumerate(m.fourrier):
            if c >= thr_:
                c_ = -(self.t-c)
            else:
                c_ = c
            mr = (mr + (c_ * pow(2,i)))
        return mr
    
    #Cette fonction permet d'effectuer l'addition des messages dans l'espaces des cyphertexts
    def HomomorphicAddition(self, ct0, ct1):
        #On additionne chaque composante du cyphertext entre elle
        ct0_b = ct0[0] + ct1[0]
        ct1_b = ct0[1] + ct1[1]
        return [ct0_b,ct1_b]
    
    #Cette fonction permet d'effectuer la soustraction des messages dans l'espace des cyphertexts
    def HomomorphicSubtraction(self, ct0, ct1):
        #On soustrait chaque composante du cyphertext entre elle
        ct0_b = ct0[0] - ct1[0]
        ct1_b = ct0[1] - ct1[1]
        return [ct0_b,ct1_b]
    
    #Cette fonction permet d'effectuer la multiplication des messages dans l'espace des cyphertexts
    def HomomorphicMultiplication(self, ct0, ct1):
        ct00 = ct0[0]
        ct01 = ct0[1]
        ct10 = ct1[0]
        ct11 = ct1[1]

        r0 = RefPolMulv2(ct00.fourrier,ct10.fourrier)
        r1 = RefPolMulv2(ct00.fourrier,ct11.fourrier)
        r2 = RefPolMulv2(ct01.fourrier,ct10.fourrier)
        r3 = RefPolMulv2(ct01.fourrier,ct11.fourrier)

        c0 = [x for x in r0]
        c1 = [x+y for x,y in zip(r1,r2)]
        c2 = [x for x in r3]

        c0 = [((self.t * x) / self.q) for x in c0]
        c1 = [((self.t * x) / self.q) for x in c1]
        c2 = [((self.t * x) / self.q) for x in c2]

        c0 = [(round(x) % self.q) for x in c0]
        c1 = [(round(x) % self.q) for x in c1]
        c2 = [(round(x) % self.q) for x in c2]

        # Move to regular modulus
        r0 = Polynome(self.n,self.q,self.qnp)
        r1 = Polynome(self.n,self.q,self.qnp)
        r2 = Polynome(self.n,self.q,self.qnp)

        r0.fourrier = c0
        r1.fourrier = c1
        r2.fourrier = c2

        return [r0,r1,r2]
    
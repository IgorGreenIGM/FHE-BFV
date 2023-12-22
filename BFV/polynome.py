# classe polynomiale

# importation des modules
from random import randint, gauss
from typing import Literal
from fourrier import *
import utils


class Polynome:
    """
    Definition de la classe polynome utilisée pour faciliter la creation, modification et manipulation des polynomes
    """
    def __init__(self, degre: int, corps_q, np: list = [0, 0, 0, 0]) -> None:
        """
        Arguments:
            degre (int): dégré du polynome
            corps_q : corps de définition du polynome
            np (list) : parametres de la tranformée de fourrier
        """
        self.degre = degre
        self.corps_q = corps_q
        self.np = np # [w : racine degre-ieme dans le corps q, w_inv : inverse de w, psi : facteur de twiddle, psi_inv : facteur de twiddle]
        self.fourrier = [0] * degre # representation du polynome dans le domaine de fourrier
        self.dans_fourrier = False # indique si le polynome est déja dans le domaine de fourrier ou non

    def randomize(self, amplitude, domaine=False, type: Literal["uniform", "gauss"] = "gauss", mu=0, sigma=0):
            if type == "uniform":
                self.fourrier = [randint(-(amplitude//2), amplitude//2) % self.corps_q for i in range(self.degre)]
                self.dans_fourrier = domaine
            else:
                self.fourrier = [int(gauss(mu, sigma))%self.corps_q for i in range(self.degre)]
                self.dans_fourrier = domaine

    def __str__(self) -> str:
        """
            surcharge de l'operation str pour la classe polynome. permet un meilleur affichage du polynome
        Returns:
            str: chaine de caracteres correspondante
        """
        pstr = str(self.fourrier[0])
        tmp = min(self.degre, 19)

        for i in range(1, tmp):
            pstr = pstr + " + " + str(self.fourrier[i]) + "x" + get_superscript_unicode(i)
        
        if self.degre > 19:
                pstr = pstr + " + ..."

        return pstr
    
    def __add__(self, poly_b):
        """ fonction d'addition de deux polynomes
        Args:
            poly_b (Polynome): 
        """
        if self.dans_fourrier != poly_b.dans_fourrier:
            raise Exception("Addition de polynomes : les entrées doivent etre dans le meme domaine")
        elif self.corps_q != poly_b.corps_q:
            raise Exception("Addition de polynomes : les entrées doivent etre dans le meme corps q")
        else:
            result = Polynome(self.degre, self.corps_q, self.np)
            result.fourrier = [(x+y)%self.corps_q for x,y in zip(self.fourrier, poly_b.fourrier)]
            result.dans_fourrier = self.dans_fourrier
            return result

    def __sub__(self, poly_b):
        """ fonction de soustraction de deux polynomes
        Args:
            poly_b (Polynome): 
        """
        if self.dans_fourrier != poly_b.dans_fourrier:
            raise Exception("Soustraction de polynomes : les entrées doivent etre dans le meme domaine")
        elif self.corps_q != poly_b.corps_q:
            raise Exception("Soustraction de polynomes : les entrées doivent etre dans le meme corps q")
        else:
            result = Polynome(self.degre, self.corps_q, self.np)
            result.fourrier = [(x-y)%self.corps_q for x,y in zip(self.fourrier, poly_b.fourrier)]
            result.dans_fourrier = self.dans_fourrier
            return result
        
    def __mul__(self, poly_b):
        """ fonction de multiplication de deux polynomes
        Args:
            poly_b (Polynome): 
        """
        if self.dans_fourrier != poly_b.dans_fourrier:
            raise Exception("Multiplication de polynomes : les entrées doivent etre dans le meme domaine")
        elif self.corps_q != poly_b.corps_q:
            raise Exception("Multiplication de polynomes : les entrées doivent etre dans le meme corps q")
        else:
            """
                En fonction du domaine ou on se situe(polynome normal/domaine de fourrier), on applique une multiplication spécifique
            """
            result = Polynome(self.degre, self.corps_q, self.np)
            if (self.dans_fourrier and poly_b.dans_fourrier):
                result.fourrier = [(x*y)%self.corps_q for x,y in zip(self.fourrier, poly_b.fourrier)]
                result.dans_fourrier = True
            
            else:
                w_table = self.np[0]
                wv_table = self.np[1]
                psi_table = self.np[2]
                psiv_table = self.np[3]

                s_p = [(x*psi_table[pwr])%self.corps_q for pwr,x in enumerate(self.fourrier)]
                b_p = [(x*psi_table[pwr])%self.corps_q for pwr,x in enumerate(poly_b.fourrier)]
                s_n = transform_fourrier(s_p,w_table,self.corps_q)
                b_n = transform_fourrier(b_p,w_table,self.corps_q)
                sb_n= [(x*y)%self.corps_q for x,y in zip(s_n,b_n)]
                sb_p= inverse_transform_fourrier(sb_n,wv_table,self.corps_q)
                sb  = [(x*psiv_table[pwr])%self.corps_q for pwr,x in enumerate(sb_p)]

                result.fourrier = sb
                result.dans_fourrier = False

            return result
        
    def __mod__(self, base: int):
        """
            Opération modulo sur un polynome
        """
        result = Polynome(self.degre, self.corps_q, self.np)
        result.fourrier = [(x%base) for x in self.fourrier]
        result.dans_fourrier = self.dans_fourrier
        return result
    
    def __neg__(self):
        """
            Opération oppose(x -> -x) sur un polynome
        """
        result = Polynome(self.degre, self.corps_q, self.np)
        result.fourrier = [((-x) % self.corps_q) for x in self.fourrier]
        result.dans_fourrier = self.dans_fourrier
        return result
    

    def __round__(self):
        """
            operation arrondi sur le polynome
        """
        result = Polynome(self.degre, self.corps_q, self.np)
        result.fourrier = [round(x) for x in self.fourrier]
        result.dans_fourrier = self.dans_fourrier
        return result
    
    def __eq__(self, poly_b) -> bool:
        """
            fonction de test d'égalité entre deux polynomes
        """
        if self.degre != poly_b.degre:
            return False
        elif self.corps_q != poly_b.corps_q:
            return False
        else:
            for x, y in zip(self.fourrier, poly_b.fourrier):
                if x != y:
                    return False
            return True
        
    def vers_fourrier(self):
        """
            fonction de transformation du polynome actuel dans le domaine de fourrier
        """
        result = Polynome(self.degre, self.corps_q, self.np)
        if not self.dans_fourrier:
            result.fourrier = transform_fourrier(self.F, self.np[0], self.corps_q)
            result.dans_fourrier = True
        else:
            result.dans_fourrier = [x for x in self.fourrier]
            result.dans_fourrier = False
        
        return result
    
    def vers_polynome(self):
        result = Polynome(self.degre, self.corps_q, self.np)
        if not self.dans_fourrier:
            result.fourrier = [x for x in self.fourrier]
        
        else:
            result.fourrier = inverse_transform_fourrier(self.fourrier, self.np[1], self.corps_q)
            result.dans_fourrier = False
        
        return result
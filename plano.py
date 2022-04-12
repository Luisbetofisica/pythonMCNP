# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:17:41 2022

@author: Abrah
"""
from punto import punto
from vector import vector
from solucion import resuelve
from utilidades import SIG_FIGURES, FLOAT_EPS
from linea import linea
from objeto import objeto

class plano(objeto):
    clase=2

    @classmethod
    def plano_xy(cls):
        return cls(punto.origen(),vector.z_uni())

    @classmethod
    def plano_yz(cls):
        return cls(punto.origen(),vector.x_uni())

    @classmethod
    def plano_xz(cls):
        return cls(punto.origen(),vector.y_uni())

    def __repr__(self):
        return "Plano ({},{}) = 0".format(self.n,self.p)

    def in_general(self,a,b,c,d):
        sol=resuelve([[a,b,c,d]])
        self.n=vector(a,b,c).normalizar()
        self.p=punto(*sol(1,1))

    def in_punto_normal(self,p,normal):
        self.p=p
        self.n=normal.normalizar()

    def __init__(self, *args):
        if len(args)==3:
            a,b,c=args
            if (isinstance(a,punto) and isinstance(b,punto) and isinstance(c,punto)):
                vab=b.apunta()-a.apunta()
                vac=c.apunta()-a.apunta()

            elif(isinstance(a,punto) and isinstance(b,vector) and isinstance(c,vector)):
                vab, vac=b,c
                
            vec=vab.pcruz(vac)
            self.in_punto_normal(a,vec)

        elif len(args)==2:
            self.in_punto_normal(*args)

        elif len(args)==4:
            self.in_general(*args)  

    def __contains__(self,b):
        if isinstance(b,punto):
            #print(abs(b.apunta()*self.n-self.p.apunta()*self.n))
            return abs(b.apunta()*self.n-self.p.apunta()*self.n)<FLOAT_EPS
        if isinstance(b,linea):
            return punto(b.il) in self and paralelo(self,b)
        elif b.clase>self.clase:
            b.in_(self)
        else:
            raise NotImplementedError("")

    def __eq__(self, b):
        if isinstance(b, plano):
            return self.p in b and self.n.paralelo(b.n)
        else:
            return False
    def __neg__(self):
        return plano(self.p,-self.n)

    def __hash__(self):
        return hash(("plano",round(self.n[0],SIG_FIGURES),round(self.n[1],SIG_FIGURES),round(self.n[2],SIG_FIGURES),round(self.n * self.p.apunta(),SIG_FIGURES)))

    def punto_normal(self):
        return (self.p.apunta(),self.n)

    def for_gen(self):
        return(self.n[0],self.n[1],self.n[2],self.n*self.p.apunta())

    def f_param(self):
        s=resuelve([list(self.n)+[0]])
        v=vector(*s(1,1))
        
        assert v.ortogonal(self.n)

        s=resuelve([list(self.n)+[0],list(v)+[0],])
        w=vector(*s(1))
        return (self.p.apunta(),v,w)

    def mover(self,v):
        if isinstance(v,vector):
            self.p.mover(v)
            return plano(self.p,self.n)
        else:
            return NotImplementedError("El segundo parametro debe ser un vector")

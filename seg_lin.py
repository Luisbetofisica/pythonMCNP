# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:29:37 2022

@author: Abrah
"""

import copy
from punto import punto
from linea import linea
from vector import vector
from utilidades import FLOAT_EPS
from plano import plano
from objeto import objeto

class seg_lin(objeto):
    clase=3
    def __init__(self,a,b):
        a=copy.deepcopy(a)
        b=copy.deepcopy(b)

        if isinstance(a,punto) and isinstance(b,punto):
            if a==b:
                raise ValueError("El punto a es igual al punto b")
            self.linea=linea(a,b)
            self.punto_in=a
            self.punto_fin=b

        elif isinstance(a,punto) and isinstance(b,vector):
            if b.magn() < FLOAT_EPS:
                raise ValueError("La longitud del vector es 0")
            self.linea=linea(a,b)
            self.punto_in=a
            self.punto_fin=punto(a.apunta()+b)
        else:
            raise ValueError("No se puede crear un segmento de linea con los tipos: {}, {}".format(type(a),type(b)))

    def __eq__(self,b):
        return ((self.punto_in==b.punto_in and self.punto_fin==b.punto_fin) or (self.punto_in==b.punto_fin and self.punto_fin==b.punto_in))

    def __repr__(self):
        return "Segmento ({},{})".format(self.punto_in, self.punto_fin)

    def __contains__(self,b):
        if isinstance(b,punto):
            r1=b in self.linea
            v1=vector(self.punto_in,self.punto_fin)
            v2=vector(self.punto_in,b)
            if v2.magn()<FLOAT_EPS:
                return True
            else:
                long_rel=v2*v1/(v1.magn()**2)

                return r1 and (long_rel>-FLOAT_EPS) and (long_rel<1+FLOAT_EPS)

        elif isinstance(b,seg_lin):
            return (b.punto_in in self) and (b.punto_fin in self)

        else:
            return False

    def in_(self,other):
        if isinstance(other,linea):
            return (self.start_point in other) and (self.end_point in other)
        elif isinstance(other,plano):
            return (self.start_point in other) and (self.end_point in other)
        else:
            return NotImplementedError("")

    def __getitem__(self,i):
        return (self.punto_in,self.punto_fin)[i]

    def __setitem__(self,i,valor):
        if i==0:
            self.punto_in=valor
        elif i==1:
            self.punto_fin=valor
        else:
            raise IndexError("Indice fuera de rango")

    def param(self):
        return (self.punto_in,self.punto_fin)

    def long(self):
        return self.punto_in.distancia(self.punto_fin)

    def mover(self, v):
        if isinstance(v,vector):
            self.punto_in.mover(v)
            self.punto_fin.mover(v)
            return seg_lin(self.punto_in,self.punto_fin)
        else:
            raise NotImplementedError("El parametro debe ser un vector")

    def __hash__(self):
        return hash(("Segmento",
        hash(self.punto_in) + hash(self.punto_fin),
        hash(self.punto_in) * hash(self.punto_fin)
        ))
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:16:20 2022

@author: Abrah
"""

from punto import punto
from vector import vector


class linea(object):
    clase=1     #empezamos a hablar de niveles, porque van a ser necesarios para ver si el objeto está contenido en otro, una linea seria nivel 1, 
                #un plano nivel 2

    @classmethod
    def eje_x(cls):
        return cls(punto.origen(),punto(1,0,0))

    @classmethod
    def eje_y(cls):
        return cls(punto.origen(),punto(0,1,0))

    @classmethod
    def eje_z(cls):
        return cls(punto.origen(),punto(0,0,1))

    def __init__(self,a,b):
        #checamos que se entregó en el argumento a y b

        if isinstance(a, punto):
            self.il=a.apunta()
        elif isinstance(a, vector):
            self.il=a
        elif len(a)==3:
            self.il=vector(a)
        else:
            raise TypeError("a no fue reconocido como un tipo de dato usable")

        if isinstance(b, punto):
            self.fl=b.apunta()-self.il
        elif isinstance(b, vector):
            self.fl=b
        elif len(b)==3:
            self.fl=vector(b)
        else:
            raise TypeError("b no fue reconocido como un tipo de dato usable")

    def __contains__(self, other):
        if isinstance(other, punto):
            comp=other.apunta()-self.il
            return comp.paralelo(self.fl)
        elif other.clase>self.clase:
            return other.in_(self) #llama a la funcion in de other, sera necesario crear casos de contencion para planos y volumenes
        else:
            raise TypeError("No se ha implementado")

    def __eq__(self, other):
        pass

    def __repr__(self):
        return "Inicio linea: {}, Direccion: {}".format(self.il,self.fl)

    def param(self):
        #p=a+br
        return (self.il, self.fl)

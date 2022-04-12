# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:26:21 2022

@author: Abrah
"""

class objeto(object): #queremos heredar metodos en comun para que compartan metodos, cosas como intersecciones u ortogonalidad, implementarlo cuando veamos
                    #que se necesita el mismo metodo
    def interseccion(self, otro):
        from calculos import interseccion
        return interseccion(self, otro)
    
    def paralelo(self, otro):
        from calculos import paralelo
        return paralelo(self, otro)
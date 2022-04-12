# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:49:38 2022

@author: Abrah
"""

from decimal import Decimal
from fractions import Fraction


global SIG_FIGURES,FLOAT_EPS,SMALL_ANGLE
SIG_FIGURES = 10
FLOAT_EPS = 1 / (10 ** SIG_FIGURES)
SMALL_ANGLE=0.1



def unifica_tipo(lista):
    tipos_valor = {
        Fraction: 1,
        Decimal: 2,
        float: 3,
        int: 4,
    }
    tipos = []
    for item in lista:
        for tipos_, valor in tipos_valor.items():
            if isinstance(item, tipos_):
                tipos.append((valor, tipos_))
                break
        else:
            tipos.append((0, type(item)))
    result_type = min(tipos)[1]
    return [result_type(i) for i in lista]
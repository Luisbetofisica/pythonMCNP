# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:19:57 2022

@author: Abrah
"""
from punto import punto
from linea import linea
from vector import vector
from seg_lin import seg_lin
from poliedroConvexo import poliedroConvexo
from polignoConvexo import poligonoConvexo
from plano import plano
from solucion import resuelve


def interseccion(a,b):
    #puntos
    if isinstance(a,punto) and isinstance(b,punto):
        return inter_punto_punto(a,b)

    elif isinstance(a, punto) and isinstance(b,seg_lin):
        return inter_punto_seg_lin(a,b)

    elif isinstance(a, seg_lin) and isinstance(b,punto):
        return inter_punto_seg_lin(b,a)

    elif isinstance(a, punto) and isinstance(b, poligonoConvexo):
        return inter_punto_poligono(a,b)

    elif isinstance(b, punto) and isinstance(a, poligonoConvexo):
        return inter_punto_poligono(b,a)

    #######################################################

    #lineas
    elif isinstance(a, linea) and isinstance(b,linea):
        return inter_linea_linea(a,b)

    elif isinstance(a, linea) and isinstance(b,seg_lin):
        return inter_linea_seg_lin(a,b)

    elif isinstance(b, linea) and isinstance(a,seg_lin):
        return inter_linea_seg_lin(b,a)

    elif isinstance(a, linea) and isinstance(b,plano):
        return inter_linea_plano(a,b)

    elif isinstance(a, plano) and isinstance(b,linea):
        return inter_linea_plano(b,a)

    elif isinstance(a, linea) and isinstance(b,poligonoConvexo):
        return inter_linea_poligono(a,b)

    elif isinstance(b, linea) and isinstance(a,poligonoConvexo):
        return inter_linea_poligono(b,a)

    #segmento

    elif isinstance(b, seg_lin) and isinstance(a,seg_lin):
        return inter_seg_lin_seg_lin(a,b)

    #planos

    elif isinstance(a, plano) and isinstance(b,plano):
        return inter_plano_plano(a,b)

    elif isinstance(a, plano) and isinstance(b,seg_lin):
        return inter_plano_seg_lin(a,b)

    elif isinstance(b, plano) and isinstance(a,seg_lin):
        return inter_plano_seg_lin(b,a)

    elif isinstance(a, plano) and isinstance(b,poliedroConvexo):
        return inter_plano_poliedro(a,b)

    elif isinstance(a, poliedroConvexo) and isinstance(b, plano):
        return inter_plano_poliedro(b,a)

    #poligonos
    elif isinstance(a,poligonoConvexo) and isinstance(b,poliedroConvexo):
        return inter_poligono_poliedro(a,b)

    elif isinstance(b,poligonoConvexo) and isinstance(a,poliedroConvexo):
        return inter_poligono_poliedro(b,a)

    elif isinstance(b,poligonoConvexo) and isinstance(a,poligonoConvexo):
        return inter_poligono_poligono(b,a)        

    #poliedros

    elif isinstance(a,poliedroConvexo) and isinstance(b,poliedroConvexo):
        return inter_poliedro_poliedro(a,b)

def inter_punto_punto(a,b):##
    if a==b:
        return a

    else:
        return None

def inter_punto_seg_lin(a,b):##
    if a in b:
        return a

    else:
        return None


def inter_punto_poligono(a,b):##
    if a in b:
        return a
    else:
        return None

def inter_linea_linea(a,b):##
    #print(b,a)
    if a==b:
        return a
    else:
        try:
            sol=resuelve([
                [a.fl[0],-b.fl[0],b.il[0]-a.il[0]],
                [a.fl[1],-b.fl[1],b.il[1]-a.il[1]],
                [a.fl[2],-b.fl[2],b.il[2]-a.il[2]],
                ])

            if not sol:
                return None

            lam, _ =sol()
            lam = float(lam)

            return punto(a.il+lam*a.fl) 

        except ValueError:
            if a.il==b.il:
                return punto(a.il[0],a.il[1],a.il[2])

            elif a.fl==b.il:
                return punto(b.il[0],b.il[1],b.il[2])

            elif b.fl==a.il:
                return punto(a.il[0],a.il[1],a.il[2])

def inter_linea_seg_lin(a,b):  ##
    inter=interseccion(a,b.linea)
    if inter is None:
        return None

    elif isinstance(inter,linea):
        return b

    elif isinstance(inter, punto):
        return interseccion(inter,b)

def inter_linea_plano(a,b): ##
    if a in b:
        return a

    elif paralelo(a,b):
        return None

    m=(b.n*b.p.apunta()-b.n*a.il)/(b.n*a.fl)
    return punto(a.il+float(m)*a.fl)

def inter_linea_poligono(a,b): ##
    inter= interseccion(a,b.plano)

    if inter is None:
        return None

    elif isinstance(inter,linea):
        con_puntos=set()
        for seg in b.segmentos():
            inter_l_s=interseccion(seg,a)

            if inter_l_s is None:
                continue

            elif isinstance(inter_l_s, punto):
                con_puntos.add(inter_l_s)

            elif isinstance(inter_l_s,seg_lin):
                return inter_l_s

        if len(con_puntos)==0:
            return None

        elif len(con_puntos)==1:
            lista_puntos=list(con_puntos)
            return lista_puntos[0]

        elif len(con_puntos)==2:
            lista_puntos=list(con_puntos)
            return seg_lin(con_puntos[0],con_puntos[1])

    elif isinstance(inter,punto):
        return interseccion(inter,b)


def inter_plano_seg_lin(a,b): ##
    inter_p_l=interseccion(a,b.linea)

    if inter_p_l is None:
        return None

    elif isinstance(inter_p_l,punto):
        return interseccion(inter_p_l,b)

    elif isinstance(inter_p_l,linea):
        return b



def inter_plano_plano(a,b):##

    if a==b:
        return a

    elif paralelo(a,b):
        return None

    else:
        linea_v=a.n.pcruz(b.n).normalizar()
        linea_auxiliar=linea(a.p,linea_v.pcruz(a.n).normalizar())
        linea_p=inter_linea_plano(linea_auxiliar,b)
        return linea(linea_v,linea_p)

def inter_plano_poliedro(a,b):##
    for pgc in b.poligonos_convexos:
        if pgc in a:
            return pgc
    con_puntos=set()
    for i in b.con_segm:
        inter_seg_poli=interseccion(i,a)

        if inter_seg_poli is None:
            continue

        elif isinstance(inter_seg_poli,seg_lin):
            continue

        elif isinstance(inter_seg_poli,punto):
            con_puntos.add(inter_seg_poli)

    tupla_puntos=tuple(con_puntos)
    if len(tupla_puntos)==0:
        return None

    elif len(tupla_puntos)==1:
        return tupla_puntos[0]

    elif len(tupla_puntos)==2:
        return seg_lin(tupla_puntos[0],tupla_puntos[1])

    else:
        return poligonoConvexo(tupla_puntos)


def inter_seg_lin_seg_lin(a,b): ##
    if a.linea == b.linea:
        con_puntos=set()

        if a.punto_in in b:
            con_puntos.add(a.punto_in)

        if a.punto_fin in b:
            con_puntos.add(a.punto_fin)

        if b.punto_in in a:
            con_puntos.add(b.punto_in)

        if b.punto_fin in a:
            con_puntos.add(b.punto_fin)

        if  len(con_puntos)==0:
            return None

        lista_puntos=list(con_puntos)

        if len(lista_puntos)==1:
            return lista_puntos[0]

        elif len(lista_puntos)==2:
            return seg_lin(lista_puntos[0],lista_puntos[1])

    else:
        inter_l_l=interseccion(a.linea,b.linea)
        if inter_l_l is None:
            return None

        elif isinstance(inter_l_l,punto):
            if inter_l_l in a and inter_l_l in b:
                return inter_l_l
            else: 
                return None

def inter_seg_lin_poligono(a,b):##
    inter_l_p=interseccion(a.linea,b.plano)
    if inter_l_p is None:
        return None

    elif isinstance(inter_l_p,punto):
        if (not inter_l_p in a) or (not inter_l_p in b):
            return None
        else:
            return inter_l_p

    elif isinstance(inter_l_p,linea):
        inter_l_pgc=interseccion(a.linea,b)
        if inter_l_pgc is None:
            return None
        elif isinstance(inter_l_pgc, punto) or isinstance(inter_l_pgc,seg_lin):

            return interseccion(inter_l_pgc,a)

def inter_poligono_poligono(a,b):
    inter_p_p=interseccion(a.plano,b.plano)
    if inter_p_p is None:
        return None

    elif isinstance(inter_p_p,linea):
        inter_p_a=interseccion(inter_p_p,a)
        inter_p_b=interseccion(inter_p_p,b)

        if inter_p_a is None or inter_p_b is None:
            return None

        else:
            return interseccion(inter_p_a,inter_p_b)

    else:
        if not a.plano==b.plano:
            raise TypeError("Los planos no coinciden")
        con_puntos=set()
        for ap in a.puntos:
            if ap in b:
                #print(ap)
                con_puntos.add(ap)

        for bp in b.puntos:
            if bp in a:
                #print(bp)
                con_puntos.add(bp)

        if len(con_puntos)<3:

            for seg in a.segmentos():

            #    print(seg)
                con_puntos=con_puntos.union(inter_seg_poligono_puntos(seg,b))

        tupla_puntos=tuple(con_puntos)
        #print(tupla_puntos,"\n")
        #print(a,b,"\n")

        if len(tupla_puntos)==0:
            return None
        elif len(tupla_puntos)==1:
            return tupla_puntos[0]

        elif len(tupla_puntos)==2:
            return seg_lin(tupla_puntos[0],tupla_puntos[1])

        else:
            return poligonoConvexo(tupla_puntos,checar_convex=False)

def inter_seg_poligono_puntos(seg,pol):
    con_puntos=set()

    for s in pol.segmentos():
        inter_s_s=interseccion(seg,s)

        if inter_s_s is None:
            continue

        elif isinstance(inter_s_s,seg_lin):
            continue

        elif isinstance(inter_s_s,punto):
            con_puntos.add(inter_s_s)

    return con_puntos

def inter_poligono_poliedro(a,b):##
    inter_plano_polie=interseccion(b,a.plano)

    if inter_plano_polie is None:
        return None

    elif isinstance(inter_plano_polie,punto) or isinstance(inter_plano_polie,seg_lin) or isinstance(inter_plano_polie,poligonoConvexo):

        return interseccion(inter_plano_polie,a)

def inter_poliedro_poliedro(a,b):
    con_pgc=set()
    con_segm=set()
    con_puntos=set()

    for pgc in a.poligonos_convexos:
        inter = interseccion(b,pgc)
        if inter is None:
            continue

        if isinstance(inter,punto):
            con_puntos.add(inter)

        elif isinstance(inter,seg_lin):
            con_segm.add(inter)

        elif isinstance(inter,poligonoConvexo):
            con_pgc.add(inter)

    for pgc in b.poligonos_convexos:
        inter= interseccion(a,pgc)
        if inter is None:
            continue

        if isinstance(inter,punto):
            con_puntos.add(inter)

        elif isinstance(inter,seg_lin):
            con_segm.add(inter)

        elif isinstance(inter,poligonoConvexo):
            con_pgc.add(inter)

    if len(con_pgc)>1:
        return poliedroConvexo(tuple(con_pgc), checar_convex=False)

    elif len(con_pgc)==1:
        return list(con_pgc)[0]

    elif len(con_segm)>1:
        raise TypeError(f"Bug {len(con_segm)}>1")

    elif len(con_segm)==1:
        return list(con_segm)[0]

    elif len(con_puntos)>1:
        raise TypeError(f"Bug {len(con_puntos)}>1")

    elif len(con_puntos)==1:
        return list(con_puntos)[0]

    else:
        return None

def paralelo(a,b):
    if isinstance(a, linea) and isinstance(b, linea):
        return a.fl.paralelo(b.fl)

    elif isinstance(a, linea) and isinstance(b, plano):
        return a.fl.ortogonal(b.n)

    elif isinstance(a, plano) and isinstance(b, linea):
        return paralelo(b, a)
    
    elif isinstance(a, plano) and isinstance(b, plano):
        return a.n.paralelo(b.n)
    
    elif isinstance(a, vector) and isinstance(b, vector):
        return a.paralelo(b)
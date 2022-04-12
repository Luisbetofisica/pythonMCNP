# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 21:30:44 2022

@author: Abrah
"""

import math
from utilidades import FLOAT_EPS
from punto import punto

class matrix(object):

    def rotx(ang,rad=True):
        if rad==False:
            ang=ang*180/math.pi
        mat=matrix(3,3)
        mat[0][0]=1
        mat[1][1]=math.cos(ang)
        mat[1][2]=-math.sin(ang)
        mat[2][1]=math.sin(ang)
        mat[2][2]=math.cos(ang)

        for i in range(mat.filas):
            for j in range(mat.columnas):
                if abs(mat[i][j])<FLOAT_EPS:
                    mat[i][j]=0 


        return mat

    def roty(ang,rad=True):
        if rad==False:
            ang=ang*180/math.pi
        mat=matrix(3,3)
        mat[0][0]=math.cos(ang)
        mat[0][2]=math.sin(ang)
        mat[2][0]=-math.sin(ang)
        mat[2][2]=math.cos(ang)
        mat[1][1]=1

        for i in range(mat.filas):
            for j in range(mat.columnas):
                if abs(mat[i][j])<FLOAT_EPS:
                    mat[i][j]=0

        return mat

    def rotz(ang,rad=True):
        if rad==False:
            ang=ang*180/math.pi
        mat=matrix(3,3)
        mat[0][0]=math.cos(ang)
        mat[0][1]=-math.sin(ang)
        mat[1][0]=math.sin(ang)
        mat[1][1]=math.cos(ang)
        mat[2][2]=1

        for i in range(mat.filas):
            for j in range(mat.columnas):
                if abs(mat[i][j])<FLOAT_EPS:
                    mat[i][j]=0

        return mat
    #cambiar al agregar interfaz

    def __init__(self, n,m,*valores):
        
        self.matriz=[]
        self.filas=n
        self.columnas=m
        if not valores:
            for i in range(n):
                aux=[]
                for j in range(m):
                    aux.append(0)
                self.matriz.append(aux)

        elif valores:
            for i in range(n):
                aux=[]
                for j in range(m):
                    try:
                        aux.append(valores[j+i*n]) 
                    except:
                        aux.append(0)
                self.matriz.append(aux)
    
    def identidad(self,n=1):
        iden=matrix(self.filas,self.columnas)
        for i in range(self.filas):
            for j in range(self.columnas):
                if i == j:
                    iden[i][j]=n
        return iden

    def issim(self):
        for i in range(self.filas):
            for j in range(i,self.columnas):
                if self.matriz[i][j]!=self.matriz[j][i]:
                    return False
        return True


    def traspuesta(self):
        tras=matrix(self.columnas,self.filas)
        for i in range(self.columnas):
            for j in range(self.filas):
                tras[i][j]=self.matriz[j][i]
        return tras

    def forma(self):
        return (self.filas,self.columnas)

    def unos(self,n=1):
        mat=matrix(self.filas,self.columnas)
        for i in range(self.filas):
            for j in range(self.columnas):
                mat[i][j]=n

        return mat

    def __repr__(self):
        cadena=""
        matmay=matrix(self.filas,self.columnas)
        veclen=[]
        for i in range(self.columnas):
            may=0
            for j in range(self.filas):
                matmay[j][i]=len(str(self.matriz[j][i]))
                if matmay[j][i]>may:
                    may=matmay[j][i]

            veclen.append(may)


        for i in range(self.filas):
            for j in range(self.columnas):
                esp=" "*(veclen[j]-matmay[i][j])
                cadena=cadena+esp+f"{self.matriz[i][j]}   "
                if j == self.columnas-1:
                    cadena+="\n"

        return cadena

    def __mul__(self,other):
        if isinstance(other,matrix):
            if self.columnas==other.filas:
                res=matrix(self.filas,other.columnas)
                for i in range(self.filas):
                    for j in range(other.columnas):
                        aux=0
                        for k in range(self.columnas):
                            aux+=self.matriz[i][k]*other.matriz[k][j]
                        res[i][j]=aux
                return res
            else:
                raise ValueError("Las matrices no pueden multiplicarse, la cantidad de columnas de la primera debe coincidir con la cantidad de filas de la segunda")
        #elif isinstance(other,vector): por implementar
        elif str(other).isnumeric() and (isinstance(other,int) or isinstance(other,float)):
            return other*self

        elif isinstance(other,punto):
            if self.columnas==3:
                #out=punto(1,1,1)
                puntom=matrix(3,1)
                puntom[0][0]=other.x
                puntom[1][0]=other.y
                puntom[2][0]=other.z

                return self*puntom

        elif isinstance(other,list):
            if self.columnas==len(other):
                #out=punto(1,1,1)
                arr=matrix(self.columnas,1)
                for i in range(self.columnas):
                    arr[i][0]=other[i]

                return self*arr

                

        else:
            raise TypeError("No es posible multiplicar por el tipo {}".format(type(other)))

    def __add__(self,other):
        if isinstance(other, matrix):
            if self.forma() == other.forma():
                res=matrix(self.filas,self.columnas)
                for i in range(self.filas):
                    for j in range(self.columnas):
                        res[i][j]=self.matriz[i][j]+other.matriz[i][j]
                return res
            else:
                raise ValueError("Las matrices no tienen la misma forma")

        elif str(other).isnumeric():
            suma=self.unos(n=other)
            return self.__add__(suma)
        else:
            raise TypeError("No se puede sumar un {} con un {}".format(type(self.matriz),other))


    def __rmul__(self,other):
        if isinstance(other,matrix):
            if self.columnas==other.filas:
                res=matrix(other.filas,self.columnas)
                for i in range(other.filas):
                    for j in range(self.columnas):
                        aux=0
                        for k in range(self.columnas):
                            aux+=other.matriz[i][k]*self.matriz[k][j]
                        res[i][j]=aux
                return res
            else:
                raise ValueError("Las matrices no pueden multiplicarse, la cantidad de columnas de la primera debe coincidir con la cantidad de filas de la segunda")
        #elif isinstance(other,vector): por implementar
        elif str(other).isnumeric():
            res=matrix(self.filas,self.columnas)
            other=matrix(self.filas,self.columnas).identidad(n=other)
            return self*other

        elif isinstance(other,punto):
            if self.filas==3:
                #out=punto(1,1,1)
                puntom=matrix(1,3)
                puntom[0][0]=other.x
                puntom[0][1]=other.y
                puntom[0][2]=other.z

                return puntom*self
        else:
            raise TypeError("No es posible multiplicar por el tipo {}".format(type(other)))

    def __getitem__(self,item):
        return self.matriz.__getitem__(item)

    def __setitem__(self,item,valor):
        self.matriz.__setitem__(item,valor)

    def __neg__(self):
        return -1*self.matriz

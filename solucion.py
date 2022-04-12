# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:06:35 2022

@author: Abrah
"""

def dim(arr):
    if not arr:
        return (0,0)
    try:
        return (len(arr),len(arr[0]))
    except:
        return len(arr)

#indice 
def index(f, l):
    for i, v in enumerate(l):
        if f(v):
            return i
    raise ValueError("No item satisfies {}".format(f))

#cuenta, pero con una funcion
def count(f, l):
    c = 0
    for i in l:
        if f(i):
            c += 1
    return c

#verifica si el numero es cero
def cero(num):
    return float(num)==float(0)

#verifica si el vector tiene ceros
def veccero(vec):
    return all(map(cero,vec))

#encuentra el primer no cero
def primer_nocero(r):
    for i, v in enumerate(r):
        if not cero(v):
            return i
    return len(r)

#clase para buscar soluciones a polinomios
class solucion(object):
    def __init__(self, sol):
        #guardamos el arreglo introducido, se supone que se espera algo como a1*sol[0]+a2*sol[1]...+an*sol[n]=sol[-1]
        self.s=sol
        #almacenamos el numero de variables, restamos uno porque se considera como la constante
        self.var=dim(sol)[1]-1
        #verificamos que se pueda resolver el sistema
        self.hay=not any(all(cero(coef) for coef in fila[:-1]) 
                         and not cero(fila[-1]) for fila in sol)
        
        #sumamos uno por cada fila que no sea 0, piensa en una matriz y como no tendria solucion si una fila tiene ceros|
        soluciones_unicas=sum(1 for i in sol if not veccero(i))
        #ahora guardamos cuantas variables dependeran de otras
        self.depen=self.var-soluciones_unicas
        #si todas son variables independientes tendremos solucion exacta
        self.exact= self.depen == 0

    #definimos que dira si lo introducimos en un if, para saber si tiene solucion o no
    def __bool__(self):
        return self.hay
    __nonzero__=__bool__

    def __call__(self, *v):
        #si no hay solucion, se detiene la llamada y devuelve un error
        if not self.hay:
            raise ValueError("El sistema no tiene solucion")
        #verificamos cuantos valores se ingresaron y checamos si son suficientes para resolver el sistema
        if len(v)!=self.depen:
            raise ValueError("Se esperaban {} valores, se ingresaron {}".format(self.depen,len(v)))

        #convertimos nuestros argumentos v a una lista, y creamos una lista de valores nulos con extension de variables
        v=list(v)
        coeficientes=[None]*self.var

        for i, fila in enumerate(self.s):
            #Se identifican los no ceros excluyendo solo el ultimo elemento
            if count(lambda i: not cero(i), fila[:-1])==1:

                n=index(lambda i: not cero(i), fila[:-1])
                coeficientes[n]=fila[-1]/fila[n]


        for i in reversed(range(len(coeficientes))):
            if not v:
                break
            if coeficientes[i] is None:
                coeficientes[i]=v.pop()

        for i in reversed(range(len(self.s))):
            fila=self.s[i]
            if veccero(fila):
                continue
            aux=primer_nocero(fila)
            s = sum(-1*fila[j]*coeficientes[j] for j in range(aux+1,len(fila)-1))
            s+=fila[-1]
            coeficientes[aux]=s/fila[aux]

        return tuple(coeficientes)

def pivote(m):
    opciones=[]
    for i, fila in enumerate(m):
        if fila[0] != 0:
            opciones.append((abs(fila[0]),i))
    if not opciones:
        return None
    
    return max(opciones)[1]

def elim_gauss(m):
    
    f,c=dim(m)
    for i in range(f-1):
        piv=pivote([fila[i:] for fila in m[i:]])
        if piv is None:
            continue
        piv += i
        m[i],m[piv]=m[piv],m[i]

        for j in range(i+1,f):
            factor = m[j][i]/m[i][i]*-1
            filam=[factor*x for x in m[i]]

            m[j]=[x+y for x,y in zip(m[j],filam)]
            #hacemos el elemento [j][i]=0 porque pueden salir numeros muy pequeños y arruinar el resultado
            #es valido porque debería hacerse
            m[j][i]=0

    return m

def resuelve(m):
    ref=elim_gauss(m)
    return solucion(ref)

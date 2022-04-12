from tkinter import ttk
import math

import tkinter as tk
#import MCNPpython

from punto import punto
from vector import vector
#from plano import plano
from linea import linea
#from poligonoConvexo import polignoConvexo
from poliedroConvexo import poliedroConvexo
from matrix import matrix

from utilidades import FLOAT_EPS, geomRenderVertices2, geomRenderCaras


############################################################################################################################################
################################################## Clase geometria para optimizar la creacion de formas, sus metodos etc ###################
############################################################################################################################################

class geometria:
    def __init__(self, canvas_width, canvas_height):
        self.CANVAS_WIDTH = canvas_height
        self.CANVAS_HEIGHT= canvas_height
        self.POSICION_OBJ = [canvas_width // 2, canvas_height-20]
        self.ESCALA_OBJ = 2500
        self._angulo_x=0
        self._angulo_y=0
        self._angulo_z=0
        self._zoom=30
        self._caras=[]
        self._vertices={}
        self.LLENAR=""
        self.COLOR_LINEA="#0000FF"
        self.COLOR_PUNTO="#000000"

    def cambiar_color_llenado(self, color, no_llenado=False):
        if(no_llenado):
            self.LLENAR=""
        else:
            self.LLENAR=color

    def cambiar_color_linea(self, color):
        self.COLOR_LINEA=color

    def actualizar_posicion(self, x, y):
        self.POSICION_OBJ[0]+=x
        self.POSICION_OBJ[1]+=y

    def _matriz_rotacion(self):
        rot_x=matrix.rotx(self._angulo_x)
        rot_y=matrix.roty(self._angulo_y)
        rot_z=matrix.rotz(self._angulo_z)

        return rot_x, rot_y, rot_z

    def _transformar_2d(self,punto, rot_x, rot_y, rot_z):
        rotado2d=rot_x*punto
        rotado2d=rot_y*rotado2d
        rotado2d=rot_z*rotado2d

        z=0.5/(self._zoom-rotado2d[2][0])

        matriz_proyeccion=matrix(2,3)
        matriz_proyeccion[0][0]=z
        matriz_proyeccion[1][1]=z

        proyectado2d=matriz_proyeccion*rotado2d

        x=int(proyectado2d[0][0]*self.ESCALA_OBJ)+self.POSICION_OBJ[0]
        y=-int(proyectado2d[1][0]*self.ESCALA_OBJ)+self.POSICION_OBJ[1]

        return x, y

    def reiniciar_angulos(self):
        self._angulo_x=0
        self._angulo_y=0
        self._angulo_z=0

    def dibujar_punto(self, point, canvas):
        POINT_SIZE=2
        canvas.create_oval(point[0],point[1],point[0],point[1], width=POINT_SIZE, fill=self.COLOR_PUNTO)
        return canvas

    def dibujar_caras(self, canvas, puntos):

        for cara in self._caras:
            #print(puntos)
            dibujar=[puntos[cara[i]] for i in range(len(cara))]
            #print(dibujar)

            for point in dibujar:
                if point[0]<0 or point[1]<0 or point[0]> self.CANVAS_WIDTH or point[1]>self.CANVAS_HEIGHT:
                    continue

                canvas = self.dibujar_punto(point, canvas)

            canvas.create_polygon(dibujar, outline= self.COLOR_LINEA, fill= self.LLENAR)

        
        return canvas

    def dibujar_linea(self, canvas, puntos):

        puntos_proyectados={}
        rot_x, rot_y, rot_z =self._matriz_rotacion()
        i=0

        for point in puntos:
            x,y=self._transformar_2d(point, rot_x, rot_y, rot_z)
            puntos_proyectados[i]=[x,y]
            i+=1

        canvas.create_line(puntos_proyectados[0],puntos_proyectados[1])

    def dibujar_objeto(self, canvas):
        puntos_proyectados = {}

        rot_x, rot_y, rot_z =self._matriz_rotacion()   
        for vertice in self._vertices.items():
            x, y = self._transformar_2d(vertice[1], rot_x, rot_y, rot_z)
            puntos_proyectados[vertice[0]]=[x,y]

        #print(puntos_proyectados[vertice[0]][1])
        #
        # print(puntos_proyectados)
        return self.dibujar_caras(canvas, puntos_proyectados)


class interfaz(tk.Tk):
    ANCHO_CANVAS=800
    ALTURA_CANVAS=600
    COLOR_CANVAS="white"
    X_REL=0.97
    TAMAÑO_PASO=0.5

    FONDO="#0b0b0b"
    figuras={"esferas":set(),"paralelepipedos":set(),"plano":set(),"cilindro":set()}

    def __init__(self, titulo="MCNPython", tam_min=(1200,600)):
        super().__init__()
        self.cambio=True
        self.cambioFig=False
        self._manejo_geometria=geometria(self.ANCHO_CANVAS,self.ALTURA_CANVAS)
        self._iniciar_ventana(titulo, tam_min)
        self._crear_herramientas()
        self._reiniciar_rotacion()

    def _iniciar_ventana(self, titulo, tam):
        self.title(titulo)
        self.minsize(*tam)
        self["bg"]=self.FONDO

    def _crear_herramientas(self):
        self._crear_lienzo()
        self._crear_herramienta_zoom()

        ttk.Separator(self, orient="horizontal").place(relx=self.X_REL, rely=0.100, relwidth=0.2, anchor="ne")

        self._crear_rotador_x()
        self._crear_rotador_y()
        self._crear_rotador_z()
        self._boton_crear_cubo()
        self._boton_crear_esfera()
        self._boton_reiniciar_rotacion()


    def _crear_lienzo(self):
        self.color_lienzo= tk.StringVar()
        self.color_lienzo.set("#FFFFFF")

        self.canvas= tk.Canvas(self, width=self.ANCHO_CANVAS, height=self.ALTURA_CANVAS, bg=self.color_lienzo.get())
        #print(type(self.canvas))
        self.canvas.place(relx=0.03, rely=0.050, relheight=0.9, relwidth=0.7)

    def _crear_herramienta_zoom(self):
        ttk.Label(self, text="Zoom", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.052, relheight=0.035, relwidth=0.2, anchor="ne")

        self.deslizante_zoom=ttk.Scale(self, from_=2000, to=0.1, orient="horizontal", command=self._cambio)
        self.deslizante_zoom.set(self._manejo_geometria._zoom)
        self.deslizante_zoom.place(relx=self.X_REL, rely=0.01, relheight=0.04, relwidth=0.2, anchor="ne")

    def _crear_rotador_x(self):
        ttk.Label(self, text="Rotacion x", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.180, relheight=0.035, relwidth=0.2, anchor="ne")

        self.deslizante_rot_x=ttk.Scale(self, from_=-math.pi, to=math.pi, orient="horizontal", command=self._cambio)
        self.deslizante_rot_x.set(self._manejo_geometria._angulo_x)
        self.deslizante_rot_x.place(relx=self.X_REL, rely=0.22, relheight=0.04, relwidth=0.2, anchor="ne")

    def _crear_rotador_y(self):
        ttk.Label(self, text="Rotacion y", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.290, relheight=0.035, relwidth=0.2, anchor="ne")

        self.deslizante_rot_y=ttk.Scale(self, from_=-math.pi, to=math.pi, orient="horizontal", command=self._cambio)
        self.deslizante_rot_y.set(self._manejo_geometria._angulo_y)
        self.deslizante_rot_y.place(relx=self.X_REL, rely=0.33, relheight=0.04, relwidth=0.2, anchor="ne")

    def _crear_rotador_z(self):
        ttk.Label(self, text="Rotacion z", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.400, relheight=0.035, relwidth=0.2, anchor="ne")

        self.deslizante_rot_z=ttk.Scale(self, from_=-math.pi, to=math.pi, orient="horizontal", command=self._cambio)
        self.deslizante_rot_z.set(self._manejo_geometria._angulo_z)
        self.deslizante_rot_z.place(relx=self.X_REL, rely=0.44, relheight=0.04, relwidth=0.2, anchor="ne")

    def _boton_reiniciar_rotacion(self):
        ttk.Button(self, text="Reiniciar angulos", command=self._reiniciar_rotacion).place(relx=self.X_REL, rely=0.9, relheight=0.05, relwidth=0.2, anchor="ne")

    def _boton_crear_esfera(self):
        ttk.Button(self, text="Crear esfera", command=self._crear_esfera).place(relx=self.X_REL, rely=0.8, relheight=0.05, relwidth=0.2, anchor="ne")

    def _boton_crear_cubo(self):
        ttk.Button(self, text="Crear cubo", command=self._crear_cubo).place(relx=self.X_REL, rely=0.7, relheight=0.05, relwidth=0.2, anchor="ne")

    def _crear_esfera(self):
        esfera=poliedroConvexo.esfera(punto(2,2,2),2)
        #vertices={item: val.punto_arreglo() for item, val in enumerate(esfera.con_puntos)}
        #self._manejo_geometria._vertices= vertices

        hashes=[]
        for i in self.figuras["esferas"]:
            hashes.append(hash(i))


        if hash(esfera) not in hashes:
            self.figuras["esferas"].add(esfera)
            #print("nueva figura")
            self._cambioFig()
            self._cambio()
        #vertices=geomRenderVertices(esfera)
        #caras, vertices=geomRenderCaras(esfera, vertices)

        #self._manejo_geometria._caras=caras
        #self._manejo_geometria._vertices=vertices

        #caras=[]

        #for cara in esfera.poligonos_convexos:
        #    aux=[]
        #    for point in cara.puntos:
        #        aux.append(keyValue(vertices, point.punto_arreglo()))

        #    caras.append(aux)

        #self._manejo_geometria._caras=caras
        #self._cambioFig()
        #self._cambio()

    def _crear_cubo(self):
        cubo=poliedroConvexo.paralelepipedo(punto(1,1,1),vector(2,0,0),vector(0,2,0),vector(0,0,2))
        #vertices=geomRenderVertices(cubo)
        #vertices={item: val.punto_arreglo() for item, val in enumerate(cubo.con_puntos)}
        #self._manejo_geometria._vertices= vertices

        #caras, vertices=geomRenderCaras(cubo, vertices)
        hashes=[]
        for i in self.figuras["paralelepipedos"]:
            hashes.append(hash(i))

        if hash(cubo) not in hashes:
            self.figuras["paralelepipedos"].add(cubo)
            self._cambioFig()
            self._cambio()

        #self._manejo_geometria._caras=caras
        #self._manejo_geometria._vertices=vertices
        #print(self._manejo_geometria._vertices)

        #caras=[]

        #for cara in cubo.poligonos_convexos:
        #    aux=[]
        #    for point in cara.puntos:
        #        aux.append(keyValue(vertices, point.punto_arreglo()))

        #    caras.append(aux)

        #self._manejo_geometria._caras=caras
        #self._cambioFig()
        #self._cambio()

    def _figurasRender(self):
        if self.cambioFig:
            caras=self._manejo_geometria._caras
            vertices=self._manejo_geometria._vertices
            for geom in self.figuras:
                for fig in self.figuras[geom]:
                    #print(hash(fig))
                    vertices=geomRenderVertices2(fig,vertices)
                    #print(vertices)
                    caras=geomRenderCaras(fig,vertices)[0]+caras

            #print(caras)
            #print(vertices)

            self._manejo_geometria._caras=caras
            self._manejo_geometria._vertices=vertices



    def _cambio(self,*arg):
        self.cambio=True

    def _cambioFig(self, *args):
        self.cambioFig=True

    def _reiniciar_rotacion(self):
        self._manejo_geometria.reiniciar_angulos()
        self.deslizante_rot_x.set(0)
        self.deslizante_rot_y.set(0)
        self.deslizante_rot_z.set(0)

        self._cambio()

    def _obtener_rotacion(self):
        self._manejo_geometria._angulo_x=self.deslizante_rot_x.get()
        self._manejo_geometria._angulo_y=self.deslizante_rot_y.get()
        self._manejo_geometria._angulo_z=self.deslizante_rot_z.get()

    def _obtener_zoom(self):
        self._manejo_geometria._zoom=self.deslizante_zoom.get()

    def dibujar(self):
        self._obtener_rotacion()
        self._obtener_zoom()
        #print(type(self.canvas))
        if self.cambioFig:
            self._figurasRender()
            self.cambioFig=False

        if self.cambio and len(self._manejo_geometria._caras):
            
            self.canvas.delete("all")
            self.canvas=self._manejo_geometria.dibujar_objeto(self.canvas)
            self.cambio=False



class main_():
    def __init__(self):
        self._iniciarInterfaz()
        self._actualizarPantalla()
        self._gui.mainloop()

    def _iniciarInterfaz(self):
        self._gui=interfaz()

    def _actualizarPantalla(self):
        self._gui.dibujar()
        self._gui.after(10, self._actualizarPantalla)

main_()
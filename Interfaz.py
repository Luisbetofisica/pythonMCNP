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
from utilidades import geomRenderVertices2, geomRenderCaras
from geometriaRender import geometria


############################################################################################################################################
################################################## Clase geometria para optimizar la creacion de formas, sus metodos etc ###################
############################################################################################################################################



class interfaz(tk.Tk):
    ANCHO_CANVAS=800
    ALTURA_CANVAS=600
    COLOR_CANVAS="white"
    X_REL=0.97
    TAMAÑO_PASO=0.5

    FONDO="#0b0b0b"
    figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list()}

    def __init__(self, titulo="MCNPython", tam_min=(1200,600)):
        super().__init__()
        self.cambio=True
        self.cambioFig=False
        self._manejo_geometria=geometria(self.ANCHO_CANVAS,self.ALTURA_CANVAS)
        self._iniciar_ventana(titulo, tam_min)
        self._crear_herramientas()
        self._reiniciar_rotacion()
        self.bind("<Configure>", self._cambio_ventana)

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

        self.deslizante_zoom=ttk.Scale(self, from_=20, to=0.01, orient="horizontal", command=self._cambio)
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
            self.figuras["esferas"].append(esfera)
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
            self.figuras["paralelepipedos"].append(cubo)
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
        
    def _cambio_ventana(self, evento):
        self._manejo_geometria.CANVAS_WIDTH=self.canvas.winfo_width()
        self._manejo_geometria.CANVAS_HEIGHT==self.canvas.winfo_height()

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
        if self._gui:
            self._gui.dibujar()
            self._gui.after(10, self._actualizarPantalla)

main_()
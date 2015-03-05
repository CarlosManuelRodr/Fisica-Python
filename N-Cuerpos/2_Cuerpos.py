#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#title           : 2_Cuerpos.py
#description     : Simula la interacción gravitacional entre dos cuerpos.
#author          : Carlos Manuel Rodríguez, Jose Ramón Palacios, Román Perdomo
#usage           : python 2_Cuerpos.py
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from __future__ import division
from visual import *
from visual.controls import *
from math import *
import os

# Constantes
G = 1

# Objetos
class Objetos:
    Tierra = 1
    Sol = 2

class PTierra:
    x = 10.0        # Posiciones
    y = 7.0
    z = 9.0
    vx = -1.0       # Velocidades
    vy = -3.0
    vz = 0.5
    m = 5.0         # Masa
    
class PSol:
    x = 0.0
    y = 0.0
    z = 4.0
    vx = 0.0
    vy = 0.0
    vz = 0.0
    m = 150.0

cps = 350         # Cuadros por segundo
deltaT = 0.005    # Intervalo temporal
t = 0             # Contador de tiempo

# Crea escena    
scene.width = 800
scene.height = 600
scene.autoscale = False

# Efectos
Esfera = sphere(pos=(0,0,0), radius=30, color=color.white, 
                opacity=0.3, material=materials.rough)
luz = local_light(pos=(0, 0, 0), color=color.yellow)

# Objetos
tierra = sphere(pos=(PTierra.x, PTierra.y, PTierra.z), material=materials.BlueMarble, radius=1, coils=50, make_trail = True)
sol = sphere(pos=(PSol.x, PSol.y, PSol.z) ,color = color.yellow, material=materials.emissive, radius=1, coils=50, make_trail = True)

# Ejes de coordenadas
eje1 = arrow(pos=(-6, 0, 0), axis=(1,0,0), color=color.red)
eje2 = arrow(pos=(-6, 0, 0), axis=(0,1,0), color=color.green)
eje3 = arrow(pos=(-6, 0, 0), axis=(0,0,1), color=color.blue)

# Controles y acciones asociadas
Centrar = Objetos.Sol
def Vista(posicion):
    global Centrar
    Centrar = posicion
    

control = controls(title='Parametros', x = scene.width + 10, y = scene.y, width = 300, height = 300, range = 50)
botonSol = button(pos=(-10,20), width=60, height=20, text='Centrar en sol', action=lambda: Vista(Objetos.Sol))
botonTierra = button(pos=(-10,-20), width=60, height=20, text='Centrar en Tierra', action=lambda: Vista(Objetos.Tierra))

# Loop principal
i = 0
while True:
    # Cuadros por segundo
    rate(cps)
    
    # Mueve la tierra
    Dist = (PTierra.x-PSol.x)**2 + (PTierra.y-PSol.y)**2 + (PTierra.z-PSol.z)**2
    
    PTierra.vx -= deltaT*((G*(PTierra.x-PSol.x)*PSol.m)/(Dist)**(3/2))
    PTierra.vy -= deltaT*((G*(PTierra.y-PSol.y)*PSol.m)/(Dist)**(3/2))
    PTierra.vz -= deltaT*((G*(PTierra.z-PSol.z)*PSol.m)/(Dist)**(3/2))
    PTierra.x += deltaT*PTierra.vx
    PTierra.y += deltaT*PTierra.vy
    PTierra.z += deltaT*PTierra.vz
    
    # Mueve el sol
    PSol.vx -= deltaT*((G*(-PTierra.x+PSol.x)*PTierra.m)/(Dist)**(3/2))
    PSol.vy -= deltaT*((G*(-PTierra.y+PSol.y)*PTierra.m)/(Dist)**(3/2))
    PSol.vx -= deltaT*((G*(-PTierra.z+PSol.z)*PTierra.m)/(Dist)**(3/2))
    PSol.x += deltaT*PSol.vx
    PSol.y += deltaT*PSol.vy
    PSol.z += deltaT*PSol.vz
    
    # Actualiza posiciones de objetos
    tierra.pos = vector(PTierra.x, PTierra.y, PTierra.z)
    sol.pos = vector(PSol.x, PSol.y, PSol.z)
    
    if Centrar == Objetos.Sol:
        centro = vector(PSol.x, PSol.y, PSol.z)
    else:
        centro = vector(PTierra.x, PTierra.y, PTierra.z)
    
    scene.center = centro
    Esfera.pos = centro
    luz.pos = centro
    eje1.pos = centro + vector(-6, 0, 0)
    eje2.pos = centro + vector(-6, 0, 0)
    eje3.pos = centro + vector(-6, 0, 0)
    
    # Escribe texto
    if i > 100:
        os.system('cls' if os.name == 'nt' else 'clear')
        i = 0
        
        eCTierra = 0.5*PTierra.m*sqrt(PTierra.vx**2 + PTierra.vy**2 + PTierra.vz**2)
        ePTierra = -G*PSol.m*PTierra.m/(Dist**(1/2))
        eCSol = 0.5*PSol.m*sqrt(PSol.vx**2 + PSol.vy**2 + PSol.vz**2)
        ePSol = -G*PSol.m*PTierra.m/(Dist**(1/2))
        
        print("Energia cinetica Tierra: ")
        print(eCTierra)
        
        print("Energia potencial Tierra: ")
        print(ePTierra)
        
        print("Energia cinetica Sol: ")
        print(eCSol)
        
        print("Energia potencial Sol: ")
        print(ePSol)
        
        print("Energia total")
        print(eCTierra+ePTierra)
        
    
    # Actualiza reloj
    t += deltaT
    i+=1
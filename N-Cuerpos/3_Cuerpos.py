#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#title           : 3_Cuerpos.py
#description     : Simula la interacción gravitacional entre tres cuerpos.
#author          : Carlos Manuel Rodríguez, Jose Ramón Palacios, Román Perdomo
#usage           : python 3_Cuerpos.py
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from __future__ import division
from visual import *
from visual.controls import *
from math import *
import os

# Constantes fisicas
G = 1

class Objetos:
    Tierra = 1
    Sol = 2
    Satelite = 3

class PTierra:
    # Valores iniciales
    x = 10
    y = 7.0
    z = 9.0
    vx = -1.0
    vy = -3.0
    vz = 4
    m = 10.0
    
class PSol:
    # Valores iniciales
    x = 0.0
    y = 0.0
    z = 0.0
    vx = -1.0
    vy = 0.0
    vz = 0.0
    m = 150.0
    
class PSat:
    # Valores iniciales
    x = 5.0
    y = 5.0
    z = 8.0
    vx = -4.0
    vy = 2.0
    vz = 2.0
    m = 40.0

cps = 200         # Cuadros por segundo
deltaT = 0.005    # Intervalo temporal

# Crea escena    
scene.width = 800
scene.height = 600
scene.autoscale = False

# Efectos
Esfera = sphere(pos = (0,0,0), radius = 50, color = color.black, opacity = 0.3, material = materials.rough)
luz = local_light(pos = (0, 0, 0), color = color.yellow)

# Objetos
tierra = sphere(pos = (PTierra.x, PTierra.y, PTierra.z), material=materials.BlueMarble, radius=1, coils=50, make_trail = True)
sol = sphere(pos = (PSol.x, PSol.y, PSol.z), color = color.yellow, material=materials.emissive, radius=2, coils=50, make_trail = True)
sat = sphere(pos = (PSat.x, PSat.y, PSat.x), color = color.blue, material = materials.rough , radius = 1, coils= 50, make_trail = True)

# Ejes de coordenadas
eje1 = arrow(pos = (-6, 0, 0), axis = (1,0,0), color=color.red)
eje2 = arrow(pos = (-6, 0, 0), axis = (0,1,0), color=color.green)
eje3 = arrow(pos = (-6, 0, 0), axis = (0,0,1), color=color.blue)

# Controles
Centrar = Objetos.Sol
def Vista(posicion):
    global Centrar
    Centrar = posicion
    

control = controls(title = 'Parametros', x = scene.width + 10, y = scene.y, width = 300, height = 300, range = 50)
m1 = menu(pos=(-20,0), height=7, width=25, text='Vista')
m1.items.append(('Sol', lambda: Vista(Objetos.Sol)))
m1.items.append(('Tierra', lambda: Vista(Objetos.Tierra)))
m1.items.append(('Satelite', lambda: Vista(Objetos.Satelite)))


# Loop principal
i = 0
while True:
    # Cuadros por segundo
    rate(cps)
    
    ### Mueve la tierra ###
    DistTierraSol = (PTierra.x-PSol.x)**2 + (PTierra.y-PSol.y)**2 + (PTierra.z-PSol.z)**2
    DistTierraSat = (PTierra.x-PSat.x)**2 + (PTierra.y-PSat.y)**2 + (PTierra.z-PSat.z)**2
    DistSolSat = (PSol.x-PSat.x)**2 + (PSol.y-PSat.y)**2 + (PSol.z-PSat.z)**2

    # Interaccion con el sol
    PTierra.vx -= deltaT*((G*(PTierra.x-PSol.x)*PSol.m)/(DistTierraSol)**(3/2))
    PTierra.vy -= deltaT*((G*(PTierra.y-PSol.y)*PSol.m)/(DistTierraSol)**(3/2))
    PTierra.vz -= deltaT*((G*(PTierra.z-PSol.z)*PSol.m)/(DistTierraSol)**(3/2))
    
    # Interaccion con el satelite
    PTierra.vx -= deltaT*((G*(PTierra.x-PSat.x)*PSat.m)/(DistTierraSat)**(3/2))
    PTierra.vy -= deltaT*((G*(PTierra.y-PSat.y)*PSat.m)/(DistTierraSat)**(3/2))
    PTierra.vz -= deltaT*((G*(PTierra.z-PSat.z)*PSat.m)/(DistTierraSat)**(3/2))
    
    
    ### Mueve el sol ###

    # Interaccion con el satelite
    PSol.vx += deltaT*((G*(PSat.x-PSol.x)*PSat.m)/(DistSolSat)**(3/2))
    PSol.vy += deltaT*((G*(PSat.y-PSol.y)*PSat.m)/(DistSolSat)**(3/2))
    PSol.vz += deltaT*((G*(PSat.z-PSol.z)*PSat.m)/(DistSolSat)**(3/2))
    
    # Iteraccion con la tierra
    PSol.vx += deltaT*((G*(PTierra.x-PSol.x)*PTierra.m)/(DistTierraSol)**(3/2))
    PSol.vy += deltaT*((G*(PTierra.y-PSol.y)*PTierra.m)/(DistTierraSol)**(3/2))
    PSol.vz += deltaT*((G*(PTierra.z-PSol.z)*PTierra.m)/(DistTierraSol)**(3/2))
    
    
    ### Mueve el satelite ###
    # Interaccion con la tierra
    PSat.vx += deltaT*((G*(PTierra.x-PSat.x)*PTierra.m)/(DistTierraSat)**(3/2))
    PSat.vy += deltaT*((G*(PTierra.y-PSat.y)*PTierra.m)/(DistTierraSat)**(3/2))
    PSat.vz += deltaT*((G*(PTierra.z-PSat.z)*PTierra.m)/(DistTierraSat)**(3/2))
    
    # Interaccion con el sol
    PSat.vx -= deltaT*((G*(PSat.x-PSol.x)*PSol.m)/(DistSolSat)**(3/2))
    PSat.vy -= deltaT*((G*(PSat.y-PSol.y)*PSol.m)/(DistSolSat)**(3/2))
    PSat.vz -= deltaT*((G*(PSat.z-PSol.z)*PSol.m)/(DistSolSat)**(3/2))
    
    PSol.x += deltaT*PSol.vx
    PSol.y += deltaT*PSol.vy
    PSol.z += deltaT*PSol.vz
    
    PTierra.x += deltaT*PTierra.vx
    PTierra.y += deltaT*PTierra.vy
    PTierra.z += deltaT*PTierra.vz
    
    PSat.x += deltaT*PSat.vx
    PSat.y += deltaT*PSat.vy
    PSat.z += deltaT*PSat.vz
    
    # Actualiza posiciones de objetos
    tierra.pos = vector(PTierra.x, PTierra.y, PTierra.z)
    sol.pos = vector(PSol.x, PSol.y, PSol.z)
    sat.pos = vector(PSat.x, PSat.y, PSat.z)
    
    if Centrar == Objetos.Sol:
        centro = vector(PSol.x, PSol.y, PSol.z)
    elif Centrar == Objetos.Tierra:
        centro = vector(PTierra.x, PTierra.y, PTierra.z)
    else:
        centro = vector(PSat.x, PSat.y, PSat.z)
    
    scene.center = centro
    Esfera.pos = centro
    luz.pos = vector(PSol.x, PSol.y, PSol.z)
    eje1.pos = centro + vector(-6, 0, 0)
    eje2.pos = centro + vector(-6, 0, 0)
    eje3.pos = centro + vector(-6, 0, 0)
    
    # Escribe texto
    if i > 100:
        os.system('cls' if os.name == 'nt' else 'clear')
        i = 0
        
        eCTierra = 0.5*PTierra.m*(PTierra.vx**2 + PTierra.vy**2 + PTierra.vz**2)
        eCSol = 0.5*PSol.m*(PSol.vx**2 + PSol.vy**2 + PSol.vz**2)
        eCSat = 0.5*PSat.m*(PSat.vx**2 + PSat.vy**2 + PSat.vz**2)
        ePTierraSol= -G*PSol.m*PTierra.m/(DistTierraSol**(1/2))
        ePTierraSat = -G*PSat.m*PTierra.m/(DistTierraSat**(1/2))
        ePSolSat = -G*PSat.m*PSol.m/(DistSolSat**(1/2))
        
        print("Energia cinetica Tierra: ")
        print(eCTierra)
        
        print("Energia cinetica Sol: ")
        print(eCSol)
        
        print("Energia cinetica Sat:")
        print(eCSat)

        print("Energia potencial tierra-sol: ")
        print(ePTierraSol)
        
        print("Energia potencial tierra-satelite: ")
        print(ePTierraSat)
        
        print("Energia potencial satelite-sol: ")
        print(ePSolSat)
        
        print("Energia total")
        print(eCTierra + eCSol + eCSat + ePTierraSol + ePTierraSat + ePSolSat)
        
    
    # Actualiza iteraciones
    i += 1
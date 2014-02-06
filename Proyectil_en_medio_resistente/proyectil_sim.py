#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Simula la trayectoria de un proyectil en un medio resistente.
#author          : José Ramón Palacios, Carlos Manuel Rodríguez
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from visual import *
from visual.controls import *

# Parámetros
class Parametros:
	cps=16
	deltat = 0.1
	t = 0.0
	plano = 100

p = Parametros()

# Ejes de coordenadas
arrow(pos=(0,10,-15), axis=(5,0,0), shatfwidth=5, color=color.red)
arrow(pos=(0,10,-15), axis=(0,5,0), shatfwidth=5, color=color.green)
text(pos=(7,10,-15), text='X', height=3)
text(pos=(0,15,-15), text='Y', height=3)

# Objetos
plano = box(pos=(p.plano/2,-2,0), axis=(1,0,0), length=p.plano, width=25, height=1, material=materials.wood)
particula1 = sphere(pos=(1,0,-10), radius=1, color=color.red, make_trail=true)
particula2 = sphere(pos=(0,0,10), radius=1, color=color.blue, make_trail=true)
medioRes = box(pos=(p.plano/2,-2,-6), axis=(1,0,0), length=p.plano, width=12, height=50, color=color.white, opacity=0)

# Otros
scene.center = vector(p.plano/2,-2,0)
scene.autoscale = True

# Variables de simulación
x1 = 0.0
y1 = 0.0
x2 = 0.0
y2 = 0.0
k = 0.5
v = 30
phi = radians(45)
g = 9.81

# Control
def setK(val):
	global k
	global medioRes
	global labelK
	k = val
	labelK.text = "k = {0:.2}".format(val)
	medioRes.opacity = val/2;
	
def reset():
	global p
	global x1
	global y1
	global x2
	global y2
	
	p.t = 0.0
	x1 = 0.0
	y1 = 0.0
	x2 = 0.0
	y2 = 0.0

control = controls(title='Parametros', x = scene.width + 10, y = scene.y, width = 300, height = 300, range = 50)
botonReset = button(pos=(0,20), width=60, height=20, text='Disparar', action=lambda: reset())
labelK = label(display=control.display, text="k = 0.5", pos=(30, 0), height=8)
sliderK = slider(pos=(-40,0), length=50, axis=(1,0,0), width=5, action=lambda: setK(sliderK.value), min=0.01, max=1)
sliderK.value = 0.5

# Iterar indefinidamente
while True:
	# Control de cuadros p segundo
	rate(p.cps)

	# Actualizar posiciones
	x1 = (v/k)*cos(phi)*(1 - exp(-k*p.t))
	x2 = v*cos(phi)*p.t
	y1 = ((k*v*sin(phi) + g)/(k**2))*(1 - exp(-k*p.t)) - (g*p.t/k)
	y2 = v*sin(phi)*p.t - (0.5)*g*(p.t**2)

	# Actualizar objetos
	if(y1 >= 0): particula1.pos = vector(x1,y1,particula1.pos.z)
	if(y2 >= 0): particula2.pos = vector(x2,y2,particula2.pos.z)

	# Incrementar reloj
	p.t += p.deltat


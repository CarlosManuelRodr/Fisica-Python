#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Tres osciladores acoplados en arreglo triangular.
#author          : Carlos Manuel Rodríguez
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from visual import *
from visual.controls import *

# Parámetros
scene.width = 500
scene.height = 480
class Parametros:
	cps = 200		# Cuadros por segundo
	deltat = 0.01	# Intervalo de tiempo para cada paso en la simulación
	t = 0.0			# Contador de tiempo

p = Parametros()

# Condiciones iniciales de la simulación
x1_init = 5.0
x2_init = 2.0
x3_init = 0.0
y1_init = 5.0
y2_init = 0.0
y3_init = 1.0

# Variables de la simulación
x1 = x1_init
x2 = x2_init
x3 = x3_init
y1 = y1_init
y2 = y2_init
y3 = y3_init
vx1 = 0.0
vx2 = 0.0
vx3 = 0.0
vy1 = 0.0
vy2 = 0.0
vy3 = 0.0
k = 1
m = 1

# Variables internas
refX1 = -20
refX2 = 0
refX3 = 20
refY1 = 20
refY2 = 0
refY3 = 20
refPlano1 = 27
refPlano2 = 33

# Ejes de coordenadas
arrow(pos = (-33,15,5), axis = (5,0,0), shatfwidth = 5, color = color.red)
arrow(pos = (-33,15,5), axis = (0,5,0), shatfwidth = 5, color = color.green)
arrow(pos = (-33,15,5), axis = (0,0,5), shatfwidth = 5, color = color.blue)
text(pos = (-26,15,5), text = 'X', height = 3)
text(pos = (-33,20,5), text = 'Y', height = 3)
text(pos = (-33,15,10), text = 'Z', height = 3)

# Objetos
planoV = box(pos=(0,7,-3), axis=(0,0,1), length=1, width=70, height=50, material=materials.wood)
particula1 = sphere(pos=(refX1+x1,refY1+y1,0), radius=2, color=color.blue, material=materials.chrome)
particula2 = sphere(pos=(refX2+x2,refY2+y2,0), radius=2, color=color.red, material=materials.chrome)
particula3 = sphere(pos=(refX3+x3,refY3+y3,0), radius=2, color=color.green, material=materials.chrome)
resorte1 = helix(pos=(refX1+x1, refY1+y1, 0), axis=(refX3+x3-x1-refX1,refY3+y3-y1-refY1,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
resorte2 = helix(pos=(refX1+x1, refY1+y1, 0), axis=(refX2+x2-x1-refX1,refY2+y2-y1-refY1,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
resorte3 = helix(pos=(refX2+x2, refY2+y2, 0), axis=(refX3+x3-x2-refX2,refY3+y3-y2-refY2,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
posEq1 = cylinder(pos = (refX1,refY1,0), axis = (0,0,1), radius = 1)
posEq2 = cylinder(pos = (refX2,refY2,0), axis = (0,0,1), radius = 1)
posEq3 = cylinder(pos = (refX3,refY3,0), axis = (0,0,1), radius = 1)
texto1 = text(pos = (refX1+x1,refY1+y1,3), text = '1', height = 3)
texto2 = text(pos = (refX2+x2,refY2+y2,3), text = '2', height = 3)
texto3 = text(pos = (refX3+x3,refY3+y3,3), text = '3', height = 3)

# Funciones de los controles
def Reset():
	global x1
	global x2
	global x3
	global y1
	global y2
	global y3
	global vx1
	global vx2
	global vx3
	global vy1
	global vy2
	global vy3
	
	x1 = x1_init
	x2 = x2_init
	x3 = x3_init
	y1 = y1_init
	y2 = y2_init
	y3 = y3_init
	vx1 = 0.0
	vx2 = 0.0
	vx3 = 0.0
	vy1 = 0.0
	vy2 = 0.0
	vy3 = 0.0
	p.t = 0
	
def CambiaX1(val):
	global x1
	global labelX1
	global x1_init
	Reset()
	x1_init = x1 = val
	labelX1.text = "X1 = {0} ".format(val)
	
def CambiaX2(val):
	global x2
	global labelX2
	global x2_init
	Reset()
	x2_init = x2 = val
	labelX2.text = "X2 = {0} ".format(val)
	
def CambiaX3(val):
	global x3
	global labelX3
	global x3_init
	Reset()
	x3_init = x3 = val
	labelX3.text = "X3 = {0} ".format(val)
	
def CambiaY1(val):
	global y1
	global labelY1
	global y1_init
	Reset()
	y1_init = y1 = val
	labelY1.text = "Y1 = {0} ".format(val)
	
def CambiaY2(val):
	global y2
	global labelY2
	global y2_init
	Reset()
	y2_init = y2 = val
	labelY2.text = "Y2 = {0} ".format(val)
	
def CambiaY3(val):
	global y3
	global labelY3
	global y3_init
	Reset()
	y3_init = y3 = val
	labelY3.text = "Y3 = {0} ".format(val)
	
def CambiaM(val):
	global m
	global labelM
	Reset()
	m = val
	labelM.text = "M = {0} ".format(val)
	
def CambiaK(val):
	global k
	global labelK
	Reset()
	k = val
	labelK.text = "K = {0} ".format(val)

	
# Control
control = controls(title = 'Parametros', x=scene.x + scene.width + 8, y = scene.y, width = 400, height = 400, range = 50)
labelX1 = label(display = control.display, pos = (30, 0), height = 8)
sliderX1 = slider(pos = (-40,0), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaX1(sliderX1.value), min = 0.00, max = 10)
sliderX1.value = x1_init
CambiaX1(x1_init)

labelX2 = label(display = control.display, pos = (30, -5), height = 8)
sliderX2 = slider(pos = (-40,-5), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaX2(sliderX2.value), min = 0.00, max = 10)
sliderX2.value = x2_init
CambiaX2(x2_init)

labelX3 = label(display = control.display, pos = (30, -10), height = 8)
sliderX3 = slider(pos = (-40,-10), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaX3(sliderX3.value), min = 0.00, max = 10)
sliderX3.value = x3_init
CambiaX3(x3_init)

labelY1 = label(display = control.display, pos = (30, -15), height = 8)
sliderY1 = slider(pos = (-40,-15), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaY1(sliderY1.value), min = 0.00, max = 10)
sliderY1.value = y1_init
CambiaY1(y1_init)

labelY2 = label(display = control.display, pos = (30, -20), height = 8)
sliderY2 = slider(pos = (-40,-20), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaY2(sliderY2.value), min = 0.00, max = 10)
sliderY2.value = y2_init
CambiaY2(y2_init)

labelY3 = label(display = control.display, pos = (30, -25), height = 8)
sliderY3 = slider(pos = (-40,-25), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaY3(sliderY3.value), min = 0.00, max = 10)
sliderY3.value = y3_init
CambiaY3(y3_init)

labelM = label(display = control.display, pos = (30, -30), height = 8)
sliderM = slider(pos = (-40,-30), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaM(sliderM.value), min = 0.00, max = 10)
sliderM.value = m
CambiaM(m)


labelK = label(display = control.display, pos = (30, -40), height = 8)
sliderK = slider(pos = (-40,-40), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaK(sliderK.value), min = 0.00, max = 10)
sliderK.value = k
CambiaK(k)

resetButton = button(pos = (0,30), height = 15, width = 30, text = 'Reset', action=lambda: Reset())

# Iterar indefinidamente
while True:
	# Control de cuadros por segundo
	rate(p.cps)
	
	if m == 0:
		pass
	else:
		# Calcula posición de las masas por el método de Euler
		vx1 += p.deltat*((k/m)*(x2+x3-2*x1))
		vx2 += p.deltat*((k/m)*(x1+x3-2*x2))
		vx3 += p.deltat*((k/m)*(x2+x1-2*x3))
		vy1 += p.deltat*((k/m)*(y2+y3-2*y1))
		vy2 += p.deltat*((k/m)*(y1+y3-2*y2))
		vy3 += p.deltat*((k/m)*(y2+y1-2*y3))
		x1 += p.deltat*vx1
		x2 += p.deltat*vx2
		x3 += p.deltat*vx3
		y1 += p.deltat*vy1
		y2 += p.deltat*vy2
		y3 += p.deltat*vy3
	
	# Actualiza posiciones
	particula1.pos = vector(refX1+x1,refY1+y1,0)
	particula2.pos = vector(refX2+x2,refY2+y2,0)
	particula3.pos = vector(refX3+x3,refY3+y3,0)
	resorte1.pos = vector(refX1+x1, refY1+y1, 0)
	resorte1.axis = vector(refX3+x3-x1-refX1,refY3+y3-y1-refY1,0)
	resorte2.pos = vector(refX1+x1, refY1+y1, 0)
	resorte2.axis = vector(refX2+x2-x1-refX1,refY2+y2-y1-refY1,0)
	resorte3.pos = vector(refX2+x2, refY2+y2, 0)
	resorte3.axis = vector(refX3+x3-x2-refX2,refY3+y3-y2-refY2,0)
	texto1.pos = vector(refX1+x1,refY1+y1,3)
	texto2.pos = vector(refX2+x2,refY2+y2,3)
	texto3.pos = vector(refX3+x3,refY3+y3,3)
	
	# Incrementa reloj
	p.t += p.deltat
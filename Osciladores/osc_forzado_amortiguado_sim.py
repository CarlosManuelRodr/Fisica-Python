#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Oscilador forzado y amortiguado.
#author          : Carlos Manuel Rodríguez
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from visual import *
from visual.controls import *

# Parámetros
scene.width = 600
scene.height = 480
class Parametros:
	cps = 200		# Cuadros por segundo
	deltat = 0.01	# Intervalo de tiempo para cada paso en la simulación
	t = 0.0			# Contador de tiempo

p = Parametros()

# Condiciones iniciales de la simulación
x_init = 10
vx_init = 0.0

# Variables de la simulación
x = x_init
vx = vx_init
k = 1
m = 1
Fo = 4
omega = 1
gamma = 1

# Variables internas
refX = 0
refPlano = 27
forzado = False
amortiguado = False

# Ejes de coordenadas
arrow(pos = (-33,15,-15), axis = (5,0,0), shatfwidth = 5, color = color.red)
arrow(pos = (-33,15,-15), axis = (0,5,0), shatfwidth = 5, color = color.green)
arrow(pos = (-33,15,-15), axis = (0,0,5), shatfwidth = 5, color = color.blue)
text(pos = (-26,15,-15), text = 'X', height = 3)
text(pos = (-33,20,-15), text = 'Y', height = 3)
text(pos = (-33,15,-10), text = 'Z', height = 3)

# Objetos
planoH = box(pos=(3,-2,0), axis=(1,0,0), length=60, width=25, height=1, material=materials.wood)
planoV = box(pos=(-refPlano,4,0), axis=(0,1,0), length=13, width=25, height=1, material=materials.wood)
particula = sphere(pos=(refX+x,0,0), radius=2, color=color.blue)
resorte = helix(pos=(-refPlano, 0, 0), axis=(refX+refPlano+x,0,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
fExt = arrow(pos=(refX+x+3,0,0), axis=(5,0,0), shaftwidth=1)
fExt.visible = False

# Efectos
scene.ambient=0.5

# Gráfica
grafica = display(title = "Grafica", x=scene.x + scene.width + 8, y = scene.y, width = 300, height = 300, background = (255,255,255))
grafica.autoscale = False
curva = curve(display = grafica, color = color.blue)

# Funciones de los controles
def Reset():
	global x
	global vx
	global curva
	global grafica
	curva.visible = False
	del curva
	curva = curve(display = grafica, color = color.blue)
	grafica.forward = vector(0,0,-1)
	
	x = x_init
	vx = vx_init
	p.t = 0
	
def CambiaX(val):
	global x
	global labelX1
	global x_init
	Reset()
	x_init = x = val
	labelX.text = "X = {0} ".format(val)
	
def CambiaVx(val):
	global vx
	global labelVx
	global vx_init
	Reset()
	vx_init = vx = val
	labelVx.text = "Vx = {0} ".format(val)
	
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
	
def CambiaFo(val):
	global Fo
	global labelFo
	Reset()
	Fo = val
	labelFo.text = "Fo = {0} ".format(val)
	
def CambiaOmega(val):
	global omega
	global labelOmega
	Reset()
	omega = val
	labelOmega.text = "Omega = {0} ".format(val)
	
def CambiaGamma(val):
	global gamma
	global labelGamma
	Reset()
	gamma = val
	labelGamma.text = "Gamma = {0} ".format(val)
	
def Amortiguar(val):
	global amortiguado
	amortiguado = val
	
def Forzar(val):
	global forzado
	forzado = val
	
# Control
control = controls(title = 'Parametros', x = grafica.x, y = grafica.y + grafica.height + 8, width = 400, height = 400, range = 50)
labelX = label(display = control.display, pos = (30, 0), height = 8)
sliderX = slider(pos = (-40,0), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaX(sliderX.value), min = 0.00, max = 20)
sliderX.value = x_init
CambiaX(x_init)

labelVx = label(display = control.display, pos = (30, -5), height = 8)
sliderVx = slider(pos = (-40,-5), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVx(sliderVx.value), min = 0.00, max = 10)
sliderVx.value = vx_init
CambiaVx(vx_init)

labelM = label(display = control.display, pos = (30, -10), height = 8)
sliderM = slider(pos = (-40,-10), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaM(sliderM.value), min = 0.00, max = 10)
sliderM.value = m
CambiaM(m)

labelK = label(display = control.display, pos = (30, -15), height = 8)
sliderK = slider(pos = (-40,-15), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaK(sliderK.value), min = 0.00, max = 10)
sliderK.value = k
CambiaK(k)

labelFo = label(display = control.display, pos = (30, -20), height = 8)
sliderFo = slider(pos = (-40,-20), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaFo(sliderFo.value), min = 0.00, max = 10)
sliderFo.value = Fo
CambiaFo(Fo)

labelOmega = label(display = control.display, pos = (30, -25), height = 8)
sliderOmega = slider(pos = (-40,-25), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaOmega(sliderOmega.value), min = 0.00, max = 10)
sliderOmega.value = omega
CambiaOmega(omega)

labelGamma = label(display = control.display, pos = (30, -30), height = 8)
sliderGamma = slider(pos = (-40,-30), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaGamma(sliderGamma.value), min = 0.00, max = 2)
sliderGamma.value = gamma
CambiaGamma(gamma)

swithAmort = toggle(pos = (10,30), height = 5, width = 5, text0 = 'No Amortiguado', text1 = 'Amortiguado', action=lambda: Amortiguar(swithAmort.value))
swithForz = toggle(pos = (38,30), height = 5, width = 5, text0 = 'No Forzado',text1 = 'Forzado' , action=lambda: Forzar(swithForz.value))
resetButton = button(pos = (-25,30), height = 15, width = 30, text = 'Reset', action=lambda: Reset())

# Iterar indefinidamente
while True:
	# Control de cuadros por segundo
	rate(p.cps)
	
	if m == 0:
		pass
	else:
		# Calcula posición de las masas por el método de Euler
		vx += p.deltat*(-(k/m)*x)
		if forzado == True:
			vx += p.deltat*(Fo*math.sin(omega*p.t))
		if amortiguado == True:
			vx += p.deltat*(-gamma*vx)
		x += p.deltat*vx
	
	# Actualiza posiciones
	particula.pos = vector(refX+x,0,0)
	resorte.axis = vector(refX+refPlano+x,0,0)
	if forzado == True:
		fExt.visible = True
		fExt.pos = vector(refX+x,3,0)
		if math.sin(omega*p.t) > 0:
			fExt.axis = vector(7*abs(math.sin(omega*p.t)),0,0)
		else:
			fExt.axis = vector(-7*abs(math.sin(omega*p.t)),0,0)
	else:
		fExt.visible = False
	
	# Añade punto a curva
	try: curva.append(pos = (p.t,x))
	except: pass
	grafica.center = vector(p.t, 0, 0)
	
	# Incrementa reloj
	p.t += p.deltat
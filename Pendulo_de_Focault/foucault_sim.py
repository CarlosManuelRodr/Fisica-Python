#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Visualización del péndulo de foucault.
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
x_init = 2.5
y_init = 0.0
vx_init = 0.0
vy_init = 0.0

# Variables de la simulación
x = x_init								# Posiciones y velocidades del péndulo
y = y_init								# en el marco de referencia primado.
vx = vx_init
vy = vy_init
omega = 1								# omega = raiz de g/l
lambdaA = 1								# Ángulo del pendulo respecto a la tierra
anguloTierra = 0						# Ángulo de rotación de la tierra
velAngularTierra = 0.1
vistaTierra = True
radioPendulo = sqrt(x**2 + y**2 + 4)


# Ejes de coordenadas
arrow(pos = (-30,10,-15), axis = (5,0,0), shatfwidth = 5, color = color.red)
arrow(pos = (-30,10,-15), axis = (0,5,0), shatfwidth = 5, color = color.green)
arrow(pos = (-30,10,-15), axis = (0,0,5), shatfwidth = 5, color = color.blue)
text(pos = (-23,10,-15), text = 'X', height = 3)
text(pos = (-30,15,-15), text = 'Y', height = 3)
text(pos = (-30,10,-10), text = 'Z', height = 3)

# Objetos
tierra = sphere(pos = (0,0,0),axis = (0,1,0), radius = 20, material = materials.earth)
barra = cylinder(pos = (0,0,0), axis = (22*math.cos(lambdaA), 22*math.sin(lambdaA), 0), radius = 0.1)
bolaPendulo = sphere(pos = (21*math.cos(lambdaA), 21*math.sin(lambdaA), 0), radius = 0.3, color = color.blue)
cablePendulo = cylinder(pos = (0,0,0), axis = (22*math.cos(lambdaA), 22*math.sin(lambdaA), 0), radius = 0.05, color = color.green)

# Otros
scene.autoscale = False
scene.center = vector(0,0,0)

# Efectos
cielo = sphere(pos = (0,0,0), radius = 200, color = color.black, opacity = 0.3, material = materials.rough)
luz = local_light(pos = (100,0,0), color = color.yellow)
sol = sphere(pos = (100,0,0), color = color.yellow, material = materials.emissive, radius = 2)

# Gráfica
grafica = display(title = "Grafica", x=scene.x + scene.width + 8, y = scene.y, width = 300, height = 300, background = (255,255,255))
grafica.autoscale = True
ls = curve(display = grafica, color = color.blue)

# Funciones de los controles
def Reset():
	global x
	global y
	global vx
	global vy
	global anguloTirra
	global p
	global ls    
	global grafica
	ls.visible = False
	del ls
	ls = curve(display = grafica, color = color.blue)
	grafica.forward = vector(0,0,-1)
	
	x = x_init
	y = y_init
	vx = vx_init
	vy = vy_init
	anguloTierra = 0
	p.t = 0
	
def CambiaVistaTierra(val):
	global vistaTierra
	vistaTierra = val
	if val == True:
		scene.scale = vector(0.025,0.025,0.025)
		scene.forward = vector(0,0,-1)
		scene.center = vector(0,0,0)
	else:
		scene.scale = vector(0.1,0.1,0.1)
		
def CambiaVelAngularTierra(val):
	global velAngularTierra
	global labelVAT
	Reset()
	velAngularTierra = (2*pi)/(3600.*24.)*val
	labelVAT.text = "Vel. Tierra = 2pi/(24 h)*{0}".format(val)
	
def CambiaLambda(val):
	global lambdaA
	global labelLamb
	Reset()
	lambdaA = val*3.14159/180
	labelLamb.text = "Lambda = {0} grados".format(val)
	
def CambiaOmega(val):
	global omega
	global labelOmega
	Reset()
	omega = val
	labelOmega.text = "Omega = {0:.2}".format(val)
	
# Control
control = controls(title = 'Parametros', x = grafica.x, y = grafica.y + grafica.height + 8, width = 400, height = 400, range = 50)
labelVAT = label(display = control.display, text = "Vel. Tierra = 0.1", pos = (30, 0), height = 8)
sliderVAT = slider(pos = (-40,0), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVelAngularTierra(sliderVAT.value), min = 0.00, max = 15000)
sliderVAT.value = 4750

labelLamb = label(display = control.display, text = "Lambda = 1 rad", pos = (30, -20), height = 8)
sliderLamb = slider(pos = (-40,-20), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaLambda(sliderLamb.value), min = 0.00, max = 180)
sliderLamb.value = 90

labelOmega = label(display = control.display, text = "Omega = 1", pos = (30, -40), height = 8)
sliderOmega = slider(pos = (-40,-40), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaOmega(sliderOmega.value), min = 0.00, max = 3)
sliderOmega.value = 1

menuButton = menu(pos = (0,30), height = 15, width = 30, text = 'Vista')
menuButton.items.append(('Tierra', lambda: CambiaVistaTierra(True)))
menuButton.items.append(('Pendulo', lambda: CambiaVistaTierra(False)))

# Iterar indefinidamente
while True:
	# Control de cuadros p segundo
	rate(p.cps)
	
	# Calcula posición del péndulo por el método de Euler
	vx += p.deltat*(2*velAngularTierra*math.sin(lambdaA)*vy - (omega**2)*x)
	vy += p.deltat*(-2*velAngularTierra*math.sin(lambdaA)*vx - (omega**2)*y)
	x += p.deltat*vx
	y += p.deltat*vy
	z = -sqrt(radioPendulo**2 - x**2 - y**2) + 3
	
	# Transformación de coordenadas del péndulo
	xP = -x*math.sin(anguloTierra) - y*math.sin(lambdaA)*math.cos(anguloTierra) + z*math.cos(anguloTierra)*math.cos(lambdaA)
	yP = y*math.cos(lambdaA) + z*math.sin(lambdaA)
	zP = x*math.cos(anguloTierra) - y*math.sin(lambdaA)*math.sin(anguloTierra) + z*math.sin(anguloTierra)*math.cos(lambdaA)
	
	# Cambio de coordenadas esféricas a coordenadas cartesianas
	xPrime = math.cos(lambdaA)*math.cos(anguloTierra)
	yPrime = math.sin(lambdaA)
	zPrime = math.cos(lambdaA)*math.sin(anguloTierra)

	# Actualizar posiciones
	bolaPendulo.pos = vector(22*xPrime + xP, 22*yPrime + yP, 22*zPrime + zP)
	barra.axis = vector(25*xPrime, 25*yPrime, 25*zPrime)
	cablePendulo.pos = vector(22*xPrime + xP, 22*yPrime + yP, 22*zPrime + zP)
	cablePendulo.axis = vector(3*xPrime-xP, 3*yPrime-yP, 3*zPrime-zP)
	
	# Cambia vista
	if vistaTierra != True:
		scene.center = vector(25*xPrime, 25*yPrime, 25*zPrime)
		scene.forward = vector(25*xPrime, -90*yPrime, 25*zPrime)

	# Actualizar rotación de tierra
	tierra.rotate(angle = (anguloTierra - velAngularTierra*p.t))
	
	# Añade punto a gráfica
	try: ls.append(pos = (x,y))
	except: pass

	# Incrementar reloj
	anguloTierra = velAngularTierra*p.t
	p.t += p.deltat


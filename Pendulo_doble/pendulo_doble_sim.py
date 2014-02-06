#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#title           : pendulo_doble.py
#description     : Simulador del péndulo doble. Resuelve usando el método de Euler.
#author          : Carlos Manuel Rodríguez
#usage           : python pendulo_doble.py  [opciones]
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from visual import *
from visual.controls import *
from visual.graph import *
import sys


# Parametros
scene.width = 600
scene.height = 480
scene.title = 'Simulacion: Pendulo doble'

cps = 200		# Cuadros por segundo
deltat = 0.01	# Intervalo de tiempo para cada paso en la simulacion
t = 0.0			# Contador de tiempo
plotError = True


# Condiciones iniciales de la simulacion
th1_init = 1
vth1_init = 0.0
th2_init = 1
vth2_init = 0.0

# Variables de la simulacion
m1 = 10
m2 = 10
l = 20
g = 9.81

# Variables internas
refPlanoH = 20

# Parametros opcionales
def usage():
    print 'Ejemplo de uso: pendulo_doble_sim.py [opciones]'
    print '--th1init=1        | Necesaria           | Angulo 1 inicial.'
    print '--th2init=1        | Necesaria           | Angulo 2 inicial.'
    print '--deltat=0.01      | Opcional            | Intervalo temporal en sim.'
    print '--m1=10            | Opcional            | Masa del cuerpo 1.'
    print '--m2=10            | Opcional            | Masa del cuerpo 2.'
    print '--length=20        | Opcional            | Longitud de las cuerdas.'
    print '--gravity=9.8      | Opcional            | Valor de la gravedad.'
    print '--ploterror=True   | Opcional=True,False | Graficar error numerico.'
    print ''
    sys.exit(2);

if len(sys.argv) < 2: usage()
for a in sys.argv:
    if a[-3:] != '.py':
        o = a.split('=')
        if len(o) != 2: usage()
        if o[0] == '--th1init':
            th1_init = float((o[1]))
        elif o[0] == '--th2init':
            th2_init = float((o[1]))
        elif o[0] == '--deltat':
            deltat = float((o[1]))
            cps = 3.0/deltat
        elif o[0] == '--m1':
            m1 = float((o[1]))
        elif o[0] == '--m2':
            m2 = float((o[1]))
        elif o[0] == '--length':
            l = float((o[1]))
        elif o[0] == '--gravity':
            g = float((o[1]))
        elif o[0] == '--ploterror':
            if o[1] in ('True', 'true', 'y', 'yes'):
                plotError = True
            elif o[1] in ('False', 'false', 'n', 'no'):
                plotError = False
            else: usage()
        else: usage()
        
# Asigna valores a variables de sim
th1 = th1_init
vth1 = vth1_init
th2 = th2_init
vth2 = vth2_init

# Ejes de coordenadas
arrow(pos = (-33,-30,-15), axis = (5,0,0), shatfwidth = 5, color = color.red)
arrow(pos = (-33,-30,-15), axis = (0,5,0), shatfwidth = 5, color = color.green)
arrow(pos = (-33,-30,-15), axis = (0,0,5), shatfwidth = 5, color = color.blue)
text(pos = (-26,-30,-15), text = 'X', height = 3)
text(pos = (-33,-25,-15), text = 'Y', height = 3)
text(pos = (-33,-30,-10), text = 'Z', height = 3)

# Objetos
planoH = box(pos=(0,refPlanoH,0), axis=(1,0,0), length=3, width=15, height=1, material=materials.wood)
planoV = box(pos=(0,0,-7), axis=(0,1,0), length=40, width=1, height=3, material=materials.wood)
particula1 = sphere(pos=(l*math.sin(th1),-l*math.cos(th1)+refPlanoH,0), radius=2, color=color.red, material=materials.chrome)
particula2 = sphere(pos=(l*math.sin(th1)+l*math.sin(th2),-l*math.cos(th1)-l*math.cos(th2)+refPlanoH,0), radius=2, color=color.blue, material=materials.chrome)
cable1 = cylinder(pos = (0,refPlanoH,0), axis = (l*math.sin(th1),-l*math.cos(th1),0), radius = 0.1)
cable2 = cylinder(pos = (l*math.sin(th1),-l*math.cos(th1)+refPlanoH,0), 
			axis = (l*math.sin(th2),-l*math.cos(th2),0), radius = 0.1)

# Efectos
scene.ambient=0.5

# Grafica
grafica = display(title = "Grafica", x=scene.x + scene.width + 8, y = scene.y, width = 300, height = 300, background = (255,255,255))
grafica.autoscale = True
curva = curve(display = grafica, color = color.blue)
gd = gdisplay(x=scene.x, y=scene.y+scene.height, width=600, height=300, title='Error', xtitle='t', ytitle='E')
f1 = gcurve(color=color.cyan)

# Espacio fase
eFasePlot = display(title = "Espacio fase", x=grafica.x + grafica.width + 8, y = grafica.y, width = 300, height = 300, background = (255,255,255))
eFasePlot.autoscale = True
eFase1 = curve(display = eFasePlot, color = color.red)
eFase2 = curve(display = eFasePlot, color = color.blue)

# Funciones de los controles
def Reset():
	global th1
	global vth1
	global th2
	global vth2
	global curva
	global eFase1
	global eFase2
	global grafica
	curva.visible = False
	eFase1.visible = False
	eFase2.visible = False
	del curva
	del eFase1
	del eFase2
	curva = curve(display = grafica, color = color.blue)
	eFase1 = curve(display = eFasePlot, color = color.red)
	eFase2 = curve(display = eFasePlot, color = color.blue)
	grafica.forward = vector(0,0,-1)
	
	th1 = th1_init
	vth1 = vth1_init
	th2 = th2_init
	vth2 = vth2_init
	t = 0
	
def CambiaTh1(val):
	global th1
	global labelTh1
	global th1_init
	Reset()
	th1_init = th1 = val
	labelTh1.text = "Theta1 = {0} ".format(val)
	
def CambiaTh2(val):
	global th2
	global labelTh2
	global th2_init
	Reset()
	th2_init = th2 = val
	labelTh2.text = "Theta2 = {0} ".format(val)
	
def CambiaVTh1(val):
	global vth1
	global labelVTh1
	global vth1_init
	Reset()
	vth1_init = vth1 = val
	labelVTh1.text = "VTheta1 = {0} ".format(val)
	
def CambiaVTh2(val):
	global vth2
	global labelVTh2
	global vth2_init
	Reset()
	vth2_init = vth2 = val
	labelVTh2.text = "VTheta2 = {0} ".format(val)
	
def CambiaM1(val):
	global m1
	global labelM1
	Reset()
	m1 = val
	labelM1.text = "M1 = {0} ".format(val)
	
def CambiaM2(val):
	global m2
	global labelM2
	Reset()
	m2 = val
	labelM2.text = "M2 = {0} ".format(val)
	
# Control
control = controls(title = 'Parametros', x = grafica.x, y = grafica.y + grafica.height + 8, width = 400, height = 400, range = 50)
labelTh1 = label(display = control.display, pos = (30, 0), height = 8)
sliderTh1 = slider(pos = (-40,0), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaTh1(sliderTh1.value), min = 0.00, max = 6)
sliderTh1.value = th1_init
CambiaTh1(th1_init)

labelTh2 = label(display = control.display, pos = (30, -5), height = 8)
sliderTh2 = slider(pos = (-40,-5), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaTh2(sliderTh2.value), min = 0.00, max = 6)
sliderTh2.value = th2_init
CambiaTh2(th2_init)

labelVTh1 = label(display = control.display, pos = (30, -10), height = 8)
sliderVTh1 = slider(pos = (-40,-10), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVTh1(sliderVTh1.value), min = 0.00, max = 10)
sliderVTh1.value = vth1_init
CambiaVTh1(vth1_init)

labelVTh2 = label(display = control.display, pos = (30, -15), height = 8)
sliderVTh2 = slider(pos = (-40,-15), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVTh2(sliderVTh2.value), min = 0.00, max = 10)
sliderVTh2.value = vth2_init
CambiaVTh2(vth2_init)

labelM1 = label(display = control.display, pos = (30, -20), height = 8)
sliderM1 = slider(pos = (-40,-20), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaM1(sliderM1.value), min = 0.00, max = 20)
sliderM1.value = m1
CambiaM1(m1)

labelM2 = label(display = control.display, pos = (30, -25), height = 8)
sliderM2 = slider(pos = (-40,-25), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaM2(sliderM2.value), min = 0.00, max = 20)
sliderM2.value = m2
CambiaM2(m2)

resetButton = button(pos = (0,30), height = 15, width = 30, text = 'Reset', action=lambda: Reset())

# Calcula energía total del sistema
eTotalInit = 0.5*(l**2)*((vth1**2)*(m1+m2) + (vth2**2)*m2 + 2*m2*vth1*vth2*math.cos(th1-th2)) - g*l*((m1+m2)*math.cos(th1) + m2*math.cos(th2))

# Iterar indefinidamente
while True:
	# Control de cuadros por segundo
	rate(cps)
	
	if m1 == 0 or m2 == 0:
		pass
	else:
		# Calcula posicion de las masas por el metodo de Euler
		ecMov1 = -g*(m1+m2)*math.sin(th1)+g*m2*math.sin(th2)*math.cos(th1-th2)-l*m2*(vth2**2)*math.sin(th1-th2)-l*m2*(vth1**2)*math.sin(th1-th2)*math.cos(th1-th2)
		ecMov1 /= l*(m1+m2)-l*m2*(cos(th1-th2)**2)
		ecMov2 = (m1+m2)*l*(vth1**2)*math.sin(th1-th2)-(m1+m2)*g*math.sin(th2)+m2*l*(vth2**2)*math.sin(th1-th2)*math.cos(th1-th2)+(m1+m2)*g*math.sin(th1)*math.cos(th1-th2)
		ecMov2 /= l*(m1+m2)-l*m2*(cos(th1-th2)**2)
		vth1 += deltat*ecMov1
		vth2 += deltat*ecMov2
		th1 += deltat*vth1
		th2 += deltat*vth2
	
	# Actualiza posiciones
	particula1.pos = vector(l*math.sin(th1),-l*math.cos(th1)+refPlanoH,0)
	particula2.pos = vector(l*math.sin(th1)+l*math.sin(th2),-l*math.cos(th1)-l*math.cos(th2)+refPlanoH,0)
	cable1.axis = vector(l*math.sin(th1),-l*math.cos(th1),0)
	cable2.pos = vector(l*math.sin(th1),-l*math.cos(th1)+refPlanoH,0)
	cable2.axis = vector(l*math.sin(th2),-l*math.cos(th2),0)
	
	# Añade punto a curva
	try:
		curva.append(pos = (7*(math.sin(th1)+math.sin(th2)),7.0*(-math.cos(th1)-math.cos(th2)+2.0),0))
		eFase1.append(pos = (th1, vth1))
		eFase2.append(pos = (th2, vth2))
	except: pass
	
        if(plotError):
            try:
                eTot = 0.5*(l**2)*((vth1**2)*(m1+m2) + (vth2**2)*m2 + 2*m2*vth1*vth2*math.cos(th1-th2)) - g*l*((m1+m2)*math.cos(th1) + m2*math.cos(th2))
                f1.plot(pos = (t, (eTotalInit-eTot)/eTotalInit)) # -abs((eTotalInit-eTot)/eTotalInit))
            except: pass
    
    # Incrementa reloj
	t += deltat

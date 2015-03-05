#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Tres osciladores acoplados con cuatro resortes.
#author          : Carlos Manuel Rodríguez
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from visual import *
from visual.controls import *

# Parámetros
scene.width = 600
scene.height = 480
cps = 200        # Cuadros por segundo
deltat = 0.01    # Intervalo de tiempo para cada paso en la simulación
t = 0.0          # Contador de tiempo

# Condiciones iniciales de la simulación
x1_init = 5.0
x2_init = 0.0
x3_init = 0.0
vx1_init = 0.0
vx2_init = 0.0
vx3_init = 0.0

# Variables de la simulación
x1 = x1_init
x2 = x2_init
x3 = x3_init
vx1 = vx1_init
vx2 = vx2_init
vx3 = vx3_init
k = 1
m1 = 1
m2 = 1

# Variables internas
refX1 = -20
refX2 = 0
refX3 = 20
refPlano1 = 27
refPlano2 = 33

# Ejes de coordenadas
arrow(pos = (-33,15,-15), axis = (5,0,0), shatfwidth = 5, color = color.red)
arrow(pos = (-33,15,-15), axis = (0,5,0), shatfwidth = 5, color = color.green)
arrow(pos = (-33,15,-15), axis = (0,0,5), shatfwidth = 5, color = color.blue)
text(pos = (-26,15,-15), text = 'X', height = 3)
text(pos = (-33,20,-15), text = 'Y', height = 3)
text(pos = (-33,15,-10), text = 'Z', height = 3)

# Objetos
planoH = box(pos=(3,-2,0), axis=(1,0,0), length=60, width=25, height=1, material=materials.wood)
planoV1 = box(pos=(-refPlano1,4,0), axis=(0,1,0), length=13, width=25, height=1, material=materials.wood)
planoV2 = box(pos=(refPlano2,4,0), axis=(0,1,0), length=13, width=25, height=1, material=materials.wood)
particula1 = sphere(pos=(refX1+x1,0,0), radius=2, color=color.blue, material=materials.chrome)
particula2 = sphere(pos=(refX2+x2,0,0), radius=2, color=color.red, material=materials.chrome)
particula3 = sphere(pos=(refX2+x2,0,0), radius=2, color=color.green, material=materials.chrome)
resorte1 = helix(pos=(-refPlano1, 0, 0), axis=(refX1+refPlano1+x1,0,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
resorte2 = helix(pos=(refX1+x1, 0, 0), axis=(refX2+x2-x1-refX1,0,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
resorte3 = helix(pos=(refX2+x2, 0, 0), axis=(refX3+x3-x2-refX2,0,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
resorte4 = helix(pos=(refX3+x3,0,0), axis=(refPlano2-refX3-x3,0,0), color=(128,128,128), radius=1, coils = 25, thickness=0.4)
texto1 = text(pos = (refX1+x1,3,0), text = 'm', height = 3)
texto2 = text(pos = (refX2+x2,3,0), text = 'M', height = 3)
texto3 = text(pos = (refX3+x3,3,0), text = 'm', height = 3)

# Efectos
scene.ambient=0.5

# Gráfica
grafica = display(title = "Grafica", x=scene.x + scene.width + 8, y = scene.y, width = 300, height = 300, background = (255,255,255))
grafica.autoscale = False
curva1 = curve(display = grafica, color = color.blue)
curva2 = curve(display = grafica, color = color.red)
curva3 = curve(display = grafica, color = color.green)

# Funciones de los controles
def Reset():
    global x1
    global x2
    global x3
    global vx1
    global vx2
    global vx3
    global curva1
    global curva2
    global curva3
    global grafica
    curva1.visible = False
    curva2.visible = False
    curva3.visible = False
    del curva1
    del curva2
    del curva3
    curva1 = curve(display = grafica, color = color.blue)
    curva2 = curve(display = grafica, color = color.red)
    curva3 = curve(display = grafica, color = color.green)
    grafica.forward = vector(0,0,-1)
    
    x1 = x1_init
    x2 = x2_init
    x3 = x3_init
    vx1 = vx1_init
    vx2 = vx2_init
    vx3 = vx3_init
    t = 0
    
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
    
def CambiaVx1(val):
    global vx1
    global labelVx1
    global vx1_init
    Reset()
    vx1_init = vx1 = val
    labelVx1.text = "Vx1 = {0} ".format(val)

def CambiaVx2(val):
    global vx2
    global labelVx2
    global vx2_init
    Reset()
    vx2_init = vx2 = val
    labelVx2.text = "Vx2 = {0} ".format(val)

def CambiaVx3(val):
    global vx3
    global labelVx3
    global vx3_init
    Reset()
    vx3_init = vx3 = val
    labelVx3.text = "Vx3 = {0} ".format(val)
    
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
    
def CambiaK(val):
    global k
    global labelK
    Reset()
    k = val
    labelK.text = "K = {0} ".format(val)

    
# Control
control = controls(title = 'Parametros', x = grafica.x, y = grafica.y + grafica.height + 8, width = 400, height = 400, range = 50)
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

labelVx1 = label(display = control.display, pos = (30, -15), height = 8)
sliderVx1 = slider(pos = (-40,-15), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVx1(sliderVx1.value), min = 0.00, max = 10)
sliderVx1.value = vx1_init
CambiaVx1(vx1_init)

labelVx2 = label(display = control.display, pos = (30, -20), height = 8)
sliderVx2 = slider(pos = (-40,-20), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVx2(sliderVx2.value), min = 0.00, max = 10)
sliderVx2.value = vx2_init
CambiaVx2(vx2_init)

labelVx3 = label(display = control.display, pos = (30, -25), height = 8)
sliderVx3 = slider(pos = (-40,-25), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaVx3(sliderVx3.value), min = 0.00, max = 10)
sliderVx3.value = vx3_init
CambiaVx3(vx3_init)

labelM1 = label(display = control.display, pos = (30, -30), height = 8)
sliderM1 = slider(pos = (-40,-30), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaM1(sliderM1.value), min = 0.00, max = 10)
sliderM1.value = m1
CambiaM1(m1)

labelM2 = label(display = control.display, pos = (30, -35), height = 8)
sliderM2 = slider(pos = (-40,-35), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaM2(sliderM2.value), min = 0.00, max = 10)
sliderM2.value = m2
CambiaM2(m2)

labelK = label(display = control.display, pos = (30, -40), height = 8)
sliderK = slider(pos = (-40,-40), length = 50, axis = (1,0,0), width = 5, action = lambda: CambiaK(sliderK.value), min = 0.00, max = 10)
sliderK.value = k
CambiaK(k)

resetButton = button(pos = (0,30), height = 15, width = 30, text = 'Reset', action=lambda: Reset())

# Iterar indefinidamente
while True:
    # Control de cuadros por segundo
    rate(cps)
    
    if m1 == 0 or m2 == 0:
        pass
    else:
        # Calcula posición de las masas por el método de Euler
        vx1 += deltat*(-(k/m1)*x1 - (k/m1)*(x1-x2))
        vx2 += deltat*(-(k/m2)*(2*x2-x1-x3))
        vx3 += deltat*(-(k/m1)*(x3-x2)-(k/m1)*x3)
        x1 += deltat*vx1
        x2 += deltat*vx2
        x3 += deltat*vx3
    
    # Actualiza posiciones
    particula1.pos = vector(refX1+x1,0,0)
    particula2.pos = vector(refX2+x2,0,0)
    particula3.pos = vector(refX3+x3,0,0)
    texto1.pos = vector(refX1+x1,3,0)
    texto2.pos = vector(refX2+x2,3,0)
    texto3.pos = vector(refX3+x3,3,0)
    resorte1.axis = vector(refX1+refPlano1+x1,0,0)
    resorte2.pos = vector(refX1+x1, 0, 0)
    resorte2.axis = vector(refX2+x2-x1-refX1,0,0)
    resorte3.pos = vector(refX2+x2, 0, 0)
    resorte3.axis = vector(refX3+x3-x2-refX2,0,0)
    resorte4.pos = vector(refX3+x3,0,0)
    resorte4.axis = vector(refPlano2-refX3-x3,0,0)
    
    # Añade punto a curva
    try: curva1.append(pos = (t,x1))
    except: pass
    try: curva2.append(pos = (t,x2))
    except: pass
    try: curva3.append(pos = (t,x3))
    except: pass
    grafica.center = vector(t, 0, 0)
    
    # Incrementa reloj
    t += deltat
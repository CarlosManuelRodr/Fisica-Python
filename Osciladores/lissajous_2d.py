#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Demostración de problema: Oscilador armónico amortiguado
#author          : José Ramón Palacios, 2010 - palacios_barreda@hotmail.com
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================


# La demostración consiste en un oscilador armónico amortiguado
# bi-dimensional que traza curvas de Lissajous sobre un 
# plano proyectado en R3.

from __future__ import division
from visual import *
from visual.controls import *
from math import *

# Notas importantes
#############################################################
#
# - 'crear_log=True' para activar registro de datos simulados
#
# - 'puntos_log=n' donde n es un número entero.
#
# - Los controles se desactivan si se están registrando datos
#
# - En la línea 336 se ajustan las condiciones inciales. 
#

# Opciones de datos
crear_log = False
puntos_log = 300

# Apagar pantalla
scene.visible = False
scene.x = 16
scene.y = 16
scene.height = 682
scene.width = 600

# Parámetros
# Se asumen unidades S.I.
m = 0      # masa
k_x = 0    # constante resorte x
k_y = 0    # constante resorte y
cx = 0     # coef. amrt. viscoso x
cy = 0     # coef. amrt. viscoso y
zeta_x = 0 # razón de amortiguamiento x
zeta_y = 0 # razón de amortiguamiento y

# Posiciones iniciales y dinámicas
xo = 0
yo = 0
vxo = 0
vyo = 0
x = 0
y = 0

# Constantes para condiciones iniciales
A = 0 
B = 0 

# Frecuencia angular
w_x = 0
w_y = 0

    
# Intervalos temporales
deltat = 0.01 # intervalo mínimo
t = 0         # contador general

# Dos osciladores por coordenada
f = frame()
l_res = 16.8 # elongación @ delta_x = 0
vueltas = 75
resorte_x1 = helix(axis=(-15,0,0), color=(128,128,128),
                   radius=1, coils = vueltas, thickness=1/10, frame=f)
                   
resorte_x2 = helix(axis=(15,0,0), color=(128,128,128), 
                   radius=1, coils = vueltas, thickness=1/10, frame=f)
                   
resorte_y1 = helix(axis=(0,-15,0), color=(128,128,128), 
                   radius=1, coils = vueltas, thickness=1/10, frame=f)
                   
resorte_y2 = helix(axis=(0,15,0), color=(128,128,128), 
                   radius=1, coils = vueltas, thickness=1/10, frame=f)

# Partícula acoplada al sistema
particula = box(length=3.5, height=3.5, width=3.5, 
                material=materials.rough, color=(252,158,2), frame=f)

# Ejes de coordenadas
arrow(pos=(-18, -18, -2), axis=(0,5), color=color.green, frame=f)
arrow(pos=(-18, -18, -2), axis=(5,0), color=color.red, frame=f)

# Soportes para resortes (estética, estrictamente)
box(pos=(0,0,-2.5), length=40, height=40, width=1, 
         material=materials.wood, color=(252,158,2),frame=f)

cx1 = box(length=2, height=5, width=4, material=materials.wood, frame=f)
cx2 = box(length=2, height=5, width=4, material=materials.wood, frame=f)

cy1 = box(length=2, height=5, width=4, axis=(0,1,0),
          material=materials.wood, frame=f)

cy2 = box(length=2, height=5, width=4, axis=(0,-1,0),
          material=materials.wood, frame=f)

# Rieles y soportes
curve(pos=[(-18,18),(18,18),(18,-18),(-18,-18),(-18,18)], 
      color=(128,128,128), radius=0.5, frame=f)
            
curve(pos=[(-18,18,0),(-18,18,-2)], color=(128,128,128), radius=0.5, frame=f)
curve(pos=[(18,18,0),(18,18,-2)], color=(128,128,128), radius=0.5, frame=f)
curve(pos=[(-18,-18,0),(-18,-18,-2)], color=(128,128,128), radius=0.5, frame=f)
curve(pos=[(18,-18,0),(18,-18,-2)], color=(128,128,128), radius=0.5, frame=f)

# Rotación final
f.axis = (1,1,0)
scene.forward = vector(-0.000913544, 0.956771, -0.290841)

def resetPosiciones():
    global lres
    # Mover todo a sus posiciones originales
    cx1.pos = vector(-18,0,0)
    cx2.pos = vector(18,0,0)
    cy1.pos = vector(0,-18,0)
    cy2.pos = vector(0,18,0)
    resorte_x1.pos = vector(l_res,0,0)
    resorte_x2.pos = vector(-l_res,0,0)
    resorte_y1.pos = vector(0,l_res,0)
    resorte_y2.pos = vector(0,-l_res,0)
    particula.pos = vector(0,0,0)

def calcularParametros():
    global w_x
    global w_y
    global k_x
    global k_y
    global m
    global t
    t = 0  
    w_x = math.sqrt(k_x / m) # frecuencia angular, x
    w_y = math.sqrt(k_y / m) # frecuencia angular, y

def setMasa(val):
    global m
    global lblMasa
    m = math.floor(val)
    lblMasa.text = "{0} kg".format(m)
    calcularParametros()
    limpiarCurvas()

def setKx(val):
    global k_x
    global lblKx
    global sliderKx
    k_x = math.floor(val)
    lblKx.text = "{0} N/m".format(k_x)
    sliderKx.value = k_x
    calcularParametros()
    limpiarCurvas()

def setKy(val):
    global k_y
    global lblKy
    global sliderKy
    k_y = math.floor(val)
    lblKy.text = "{0} N/m".format(k_y)
    sliderKy.value = k_y
    calcularParametros()
    limpiarCurvas()
    
def setXo(val):
    global xo
    global lblXo
    global sliderXo
    global t 
    t = 0
    xo = val
    limpiarCurvas()
    lblXo.text = "{0} m".format(xo)
    sliderXo.value = xo * 100
    
def setYo(val):
    global yo
    global lblYo
    global sliderYo
    global t
    t = 0
    yo = val
    limpiarCurvas()    
    lblYo.text = "{0} m".format(yo)
    sliderYo.value = yo * 100

def setVxo(val):
    global vxo
    global lblVxo
    global sliderVxo
    global t
    t = 0
    vxo = val
    limpiarCurvas()
    try: lblVxo.text = "{0:.2} m/s".format(vxo)
    except: lblVxo.text = "{0} m/s".format(vxo)
    sliderVxo.value = val

def setVyo(val):
    global vyo
    global lblVyo
    global sliderVyo
    global t
    t = 0
    vyo = val
    limpiarCurvas()
    try: lblVyo.text = "{0:.2} m/s".format(vyo)
    except: lblVyo.text = "{0} m/s".format(vyo)
    sliderVyo.value = val

def setCx(val):
    global cx
    global zeta_x
    global lblCx
    global sliderCx
    global t
    t = 0
    cx = val
    zeta_x = cx / (2*m*w_x)
    limpiarCurvas()    
    try: lblCx.text = "{0:.2} Ns/m".format(cx)
    except: lblCx.text = "{0} Ns/m".format(cx)
    sliderCx.value = val

def setCy(val):
    global cx
    global zeta_y
    global lblCy
    global sliderCy
    global t
    t = 0
    cy = val
    zeta_y = cy / (2*m*w_y)
    limpiarCurvas()    
    try: lblCy.text = "{0:.2} Ns/m".format(cy)
    except: lblCy.text = "{0} Ns/m".format(cy)
    sliderCy.value = val
        
def limpiarCurvas():
    global ls    
    global graf
    ls.visible = False
    del ls
    ls = curve(display=graf, color=color.blue)
    graf.forward = vector(0,0,-1)

# Preparar gráfico
graf = display(title="Curva de Lissajous", x=scene.x + scene.width + 8,
               y=scene.y, width=384, height=300,
               background=(255,255,255))
               
graf.userzoom = True
graf.userspin = True
graf.autoscale = True
graf.visible = False
graf.select()

# Agregar títulos y ejes al gráfico
ls = curve(display=graf)

# Crear controles
ctrls = controls(x=graf.x, y=graf.y + graf.height + 8, width=384,
                 height=382, range=100, title="Opciones")
                 
sliderMasa = slider(pos=(-55,80), length=100, axis=(1,0,0), width=5,
                    action=lambda: setMasa(sliderMasa.value), min=1, max=60)

label(display=ctrls.display, text="Masa:", pos=(-75,80), height=8)
lblMasa = label(display=ctrls.display, text="0 kg", pos=(70,80), height=8)

sliderKx = slider(pos=(-55,60), length=100, axis=(1,0,0), width=5,
                  action=lambda: setKx(sliderKx.value), min=1, max=1000)

label(display=ctrls.display, text="K (x):", pos=(-75,60), height=8)
lblKx = label(display=ctrls.display, text="0 N/m", pos=(70,60), height=8)

sliderKy = slider(pos=(-55,40), length=100, axis=(1,0,0), width=5,
                    action=lambda: setKy(sliderKy.value), min=1, max=1000)

label(display=ctrls.display, text="K (y):", pos=(-75,40), height=8)
lblKy = label(display=ctrls.display, text="0 N/m", pos=(70,40), height=8)

sliderCx = slider(pos=(-55,20), length=100, axis=(1,0,0), width=5,
                     action=lambda: setCx(sliderCx.value), 
                     min=0, max=200)

label(display=ctrls.display, text="Cx:", pos=(-75,20), height=8)
lblCx = label(display=ctrls.display, text="0 Ns/m", pos=(70,20), height=8)

sliderCy = slider(pos=(-55,0), length=100, axis=(1,0,0), width=5,
                     action=lambda: setCy(sliderCy.value), 
                     min=0, max=200)

label(display=ctrls.display, text="Cy:", pos=(-75,0), height=8)
lblCy = label(display=ctrls.display, text="0 Ns/m", pos=(70,0), height=8)

sliderXo = slider(pos=(-55,-20), length=100, axis=(1,0,0), width=5,
            action=lambda: setXo(math.ceil(sliderXo.value)/100),
            min=0, max=100, color=color.red)

label(display=ctrls.display, text="Xo:", pos=(-75,-20), height=8)
lblXo = label(display=ctrls.display, text="0 m", pos=(70,-20), height=8)

sliderYo = slider(pos=(-55,-40), length=100, axis=(1,0,0), width=5,
            action=lambda: setYo(math.ceil(sliderYo.value)/100),
            min=0,max=100, color=color.green)                    

label(display=ctrls.display, text="Yo:", pos=(-75,-40), height=8)
lblYo = label(display=ctrls.display, text="0 m", pos=(70,-40), height=8)

sliderVxo = slider(pos=(-55,-60), length=100, axis=(1,0,0), width=5,
                     action=lambda: setVxo(sliderVxo.value), 
                     min=0, max=30)
                     
label(display=ctrls.display, text="Vox:", pos=(-75,-60), height=8)
lblVxo = label(display=ctrls.display, text="0 m/s", pos=(70,-60), height=8)

sliderVyo = slider(pos=(-55,-80), length=100, axis=(1,0,0), width=5,
                     action=lambda: setVyo(sliderVyo.value), 
                     min=0, max=30)

label(display=ctrls.display, text="Voy:", pos=(-75,-80), height=8)
lblVyo = label(display=ctrls.display, text="0 m/s", pos=(70,-80), height=8)

# Seleccionar escena principal
scene.select()
scene.autoscale = False
resetPosiciones()    # ajustar posiciones iniciales (resortes y objetos)
setMasa(8)           # masa inicial
setKx(150)           # constante de resorte, x
setKy(300)           # constante de resorte, y
setXo(0.5)           # X inicial
setYo(0.1)           # Y inicial
setVxo(0)            # Vxo inicial
setVyo(0)            # Vyo inicial
setCx(0)             # Amortiguamiento inicial x (2*m*w_x) <- critico
setCy(0)             # Amortiguamiento inicial y
scene.visible = True
graf.visible = True

# Log de datos
if crear_log:
    tiempolocal = time.asctime( time.localtime(time.time()) )
    log_abierto = False

    try:
        log = open("sho2D-{0}.csv".format(tiempolocal), "w")
        log_abierto = True
        log.write("# Simulación - {0}\n".format(tiempolocal))
        log.write("######################################\n")
        log.write("# Masa: {0} kg\n".format(m))
        log.write("# Kx: {0} N/m, Ky: {1} N/m\n".format(k_x, k_y))
        log.write("# cx: {0} Ns/m, cy: {1} Ns/m\n".format(cx,cy))
        log.write("# Xo: {0} m, Yo: {1} m\n".format(xo, yo))
        log.write("# Vxo: {0} m/s, Vyo: {1} m/s\n".format(vxo, vyo))
        log.write("#######################################\n")
        print "Registrando datos a: sho2D-{0}.csv".format(tiempolocal)
    except:
        print ""
        print "ERROR: No fue posible abrir archivo para escritura."
        print ""
        print "La simulación correrá, sin embargo, no se guardará la tabla con los"
        print "datos resultantes. Para esto deberá correr la simulación desde otro"
        print "medio de almacenamiento."
        log_abierto = False
          
# Iterar indefinidamente
while 1:
    # Control de cps
    rate(100)

    # Leer controles
    if not crear_log: ctrls.interact()
    
    # Actualizar posiciones
    # X
    if (zeta_x  == 1): # Amortiguamiento crítico
        A = xo
        B = vxo + w_x*xo
        x = (A + B*t)*math.exp(-w_x*t)
    elif (zeta_x > 1): # Sobreamortiguado
        gamma_pos = -w_x * (zeta_x - math.sqrt((zeta_x**2) - 1))
        gamma_neg = -w_x * (zeta_x + math.sqrt((zeta_x**2) - 1))
        A = xo + (((xo*gamma_pos) - vxo)/(gamma_neg - gamma_pos))
        B = -(((gamma_pos*xo) - vxo)/(gamma_neg - gamma_pos))
        x = A*math.exp(gamma_pos*t) + B*math.exp(gamma_neg*t)
    elif (zeta_x >= 0) and (zeta_x < 1): # Infraamortiguado
        w_d = w_x * math.sqrt(1 - (zeta_x**2))
        A = xo
        B = (((zeta_x*w_x*xo) + vxo)/w_d)
        x = math.exp(-zeta_x*w_x*t)*((A*math.cos(w_d*t)) + (B*math.sin(w_d*t)))
        
    # Y
    if (zeta_y  == 1): # Amortiguamiento crítico
        A = yo
        B = vyo + w_y*yo
        y = (A + B*t)*math.exp(-w_y*t)
    elif (zeta_y > 1): # Sobreamortiguado
        gamma_pos = -w_y * (zeta_y - math.sqrt((zeta_y**2) - 1))
        gamma_neg = -w_y * (zeta_y + math.sqrt((zeta_y**2) - 1))
        A = yo + (((yo*gamma_pos) - vyo)/(gamma_neg - gamma_pos))
        B = -(((gamma_pos*yo) - vyo)/(gamma_neg - gamma_pos))
        y = A*math.exp(gamma_pos*t) + B*math.exp(gamma_neg*t)
    elif (zeta_y >= 0) and (zeta_y < 1): # Infraamortiguado
        w_d = w_y * math.sqrt(1 - (zeta_y**2))
        A = yo
        B = (((zeta_y*w_y*yo) + vyo)/w_d)
        y = math.exp(-zeta_y*w_y*t)*((A*math.cos(w_d*t)) + (B*math.sin(w_d*t)))
        
    # Guardar en archivo
    if crear_log:
        log.write("{0},{1},{2}\n".format(t,x,y))
        puntos_log -= 1
        if not puntos_log:
            log.close()
            print "Archivo cerrado. Continúa simulación..."
            crear_log = False
   
    # Mover partícula
    particula.pos = vector(x,y)

    # Comprimir resortes  
    resorte_x1.length = l_res - x
    resorte_x2.length = l_res + x
    resorte_y1.length = l_res - y
    resorte_y2.length = l_res + y

    # Girar resortes
    resorte_x1.axis = vector(-resorte_x1.x, y)
    resorte_x2.axis = vector(-resorte_x2.x, y)
    resorte_y1.axis = vector(x, -resorte_y1.y)
    resorte_y2.axis = vector(x, -resorte_y2.y)
    
    # Gráficos
    ls.append(pos=(x,y))

    # Incrementar reloj
    t += deltat

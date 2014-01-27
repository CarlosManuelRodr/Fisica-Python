#!/usr/bin/env python
#Encoding: utf-8

#=======================================================================================================
#description     : Simulador de un sistema que puede ser modelado con las ecuaciones de Volterra-Lotka.
#author          : Carlos Manuel Rodríguez
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#=======================================================================================================


from __future__ import division
from visual import *
from visual.controls import *
from math import *

# Condiciones iniciales y variables
nPresas = 50
nPred = 10

tableroXMax = 30
tableroXMin = -30
tableroYMax = 30
tableroYMin = -30
cps = 60

distMortal = 1

vidaMaxPresa = 400
vidaMaxPred = 200

tasaCrecPresas = 50
tasaCrecPred = 80

cteCrecPresa = 1.0
cteCrecPred = 0.4

running = True

# Vectores para dumpear datos
nDatos = 0
vPresas = []
vPred = []
vTiempos = []

# Clases : Estructura de datos con metodos asociados.
class Coord: 
	def __init__(self, coordX, coordY): #_init_ :  Constructor
		self.x = coordX #Self: Datos dentro de la clase
		self.y = coordY
	def Suma(self, x, y):
		# Suma coordenadas revisando que no se salga del tablero
		if self.x + x < tableroXMax and self.x + x > tableroXMin:
			self.x += x
		if self.y + y < tableroYMax and self.y + y > tableroYMin:
			self.y += y

class Presa:
	def __init__(self, posX, posY):
		self.coord = Coord(posX, posY)
		self.vida = vidaMaxPresa
		self.figura = sphere(pos = (self.coord.x, self.coord.y, 0), color = color.yellow, radius=1, coils=50)

class Predador:
	def __init__(self, posX, posY):
		self.coord = Coord(posX, posY)
		self.vida = vidaMaxPred
		self.figura = sphere(pos = (self.coord.x, self.coord.y, 0), color = color.blue, radius=1, coils=50)
	
		
# Crea listas con presas y depredadores
arrayPresas = []
arrayPred = []

for i in range(nPresas):
	posX = random.uniform(tableroXMin, tableroXMax)
	posY = random.uniform(tableroYMin, tableroYMax)
	arrayPresas.append(Presa(posX, posY)) #Append: anade elemento al vector
	
for i in range(nPred):
	posX = random.uniform(tableroXMin, tableroXMax)
	posY = random.uniform(tableroYMin, tableroYMax)
	arrayPred.append(Predador(posX, posY))


# Funciones auxiliares
def AppendDatos():
	global t
	global nPresas
	global nPred
	global nDatos
	global lsPresas
	global lsPred
	
	lsPresas.append(pos = (nDatos, nPresas))
	lsPred.append(pos = (nDatos, nPred))
	
	vTiempos.append(t)
	vPresas.append(nPresas)
	vPred.append(nPred)
	nDatos += 1

def MataPresa(i):
	global arrayPresas
	AppendDatos()
	
	arrayPresas[i].figura.visible = False
	del arrayPresas[i].figura
	del arrayPresas[i]

def MataPred(i):
	global arrayPred
	AppendDatos()
	
	arrayPred[i].figura.visible = False
	del arrayPred[i].figura
	del arrayPred[i]	
	
	
def Guardar():
	global running
	
	filePresas = open('presas.csv', 'w')
	filePred = open('pred.csv', 'w')
	for index in range(nDatos):
		filePresas.write('{0:3d}, {1:3d}\n'.format(vTiempos[index], vPresas[index]))
		filePred.write('{0:3d}, {1:3d}\n'.format(vTiempos[index], vPred[index]))
	filePresas.close()
	filePred.close()
	
# Controles
control = controls(title = 'Parametros', x = scene.width + 10, y = scene.y, width = 300, height = 300, range = 50)
boton = button( pos=(0,0), width=60, height=60, text='Guardar datos', action = lambda: Guardar() )

# Grafica
grafica = display(title="Animales", x=scene.x + scene.width + 8, y = control.y + control.width, width=384, height=300, background=(0, 0, 0))
grafica.autoscale = True
grafica.xmin = 0
scene.select()
lsPresas = curve(display=grafica, color = color.yellow)
lsPred = curve(display = grafica, color = color.red)

# Prepara main loop
crecPresas = 0
crecPred = 0
crecDepred = 0
t = 0
AppendDatos()

while running:
	rate(cps)	# Cuadros por segundo
	
	# Mueve aleatoriamente a las presas y depredadores
	for i in range(nPresas):
		randNumX = random.uniform(-1,1)
		randNumY = random.uniform(-1,1)
		arrayPresas[i].coord.Suma(randNumX, randNumY)
		arrayPresas[i].figura.pos = vector(arrayPresas[i].coord.x, arrayPresas[i].coord.y)
		
	for i in range(nPred):
		randNumX = random.uniform(-1,1)
		randNumY = random.uniform(-1,1)
		arrayPred[i].coord.Suma(randNumX, randNumY)
		arrayPred[i].figura.pos = vector(arrayPred[i].coord.x, arrayPred[i].coord.y)	

		
	# Revisa si depredadores y presas estan en contacto
	i = 0
	while i < nPresas:
		for j in range(nPred):
			if arrayPresas[i].coord.x + distMortal > arrayPred[j].coord.x and arrayPresas[i].coord.x - distMortal < arrayPred[j].coord.x:
				if arrayPresas[i].coord.y + distMortal > arrayPred[j].coord.y and arrayPresas[i].coord.y - distMortal < arrayPred[j].coord.y:
					print("Mata Presa")
					# Mata a presa
					MataPresa(i)
					nPresas -= 1
					i -= 1
					# Reestablece vida del Predador
					arrayPred[j].vida = vidaMaxPred
					
		i += 1

	
	# Quita unidad de vida a las presas
	i = 0
	while i < nPresas:
		arrayPresas[i].vida -= 1
		if arrayPresas[i].vida <= 0:
			MataPresa(i)
			nPresas -= 1
			AppendDatos()
		i += 1
		
	i = 0
	while i < nPred:
		arrayPred[i].vida -= 1
		if arrayPred[i].vida <= 0:
			MataPred(i)
			nPred -= 1
			AppendDatos()
		i += 1		
	i = 0
	
	# Nacen nuevas presas
	if crecPresas >= tasaCrecPresas:
		print("Nace presa")
		posX = random.uniform(tableroXMin, tableroXMax)
		posY = random.uniform(tableroYMin, tableroYMax)
		arrayPresas.append(Presa(posX, posY))
		crecPresas = 0
		nPresas += 1
		AppendDatos()
	else:
		crecPresas += cteCrecPresa*nPresas
		
	# Nacen nuevos Predadores	
	if crecPred >= tasaCrecPred:
		print("Nace predador")
		posX = random.uniform(tableroXMin, tableroXMax)
		posY = random.uniform(tableroYMin, tableroYMax)
		arrayPred.append(Predador(posX, posY))
		crecPred = 0
		nPred += 1
		AppendDatos()
	else:
		crecPred += cteCrecPred*nPred
		
		
	if nPresas <= 0 or nPred <= 0:
		running = False
		
	t += 1

if  nPresas <= 0:
	print("Extincion masiva")

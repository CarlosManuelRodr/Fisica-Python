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
nPresas = 3
nPred = 3
nDepred = 3

tableroXMax = 20
tableroXMin = -20
tableroYMax = 20
tableroYMin = -20
cps = 60

distMortal = 2

vidaMaxPresa = 400
vidaMaxPred = 250
vidaMaxDepred = 200

tasaCrecPresas = 50
tasaCrecPred = 80
tasaCrecDepred = 115

cteCrecPresa = 1.0
cteCrecPred = 0.35
cteCrecDepred = 0.3

running = True

# Vectores para dumpear datos
nDatos = 0
vPresas = []
vPred = []
vDepred = []
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

class Depredador:
	def __init__(self, posX, posY):
		self.coord = Coord(posX, posY)
		self.vida = vidaMaxDepred
		self.figura = sphere(pos = (self.coord.x, self.coord.y, 0), color = color.red, radius=1, coils=50)		
		
# Crea listas con presas y depredadores
arrayPresas = []
arrayPred = []
arrayDepred = []

for i in range(nPresas):
	posX = random.uniform(tableroXMin, tableroXMax)
	posY = random.uniform(tableroYMin, tableroYMax)
	arrayPresas.append(Presa(posX, posY)) #Append: anade elemento al vector
	
for i in range(nPred):
	posX = random.uniform(tableroXMin, tableroXMax)
	posY = random.uniform(tableroYMin, tableroYMax)
	arrayPred.append(Predador(posX, posY))

for i in range(nDepred):
	posX = random.uniform(tableroXMin, tableroXMax)
	posY = random.uniform(tableroYMin, tableroYMax)
	arrayDepred.append(Depredador(posX, posY))	

# Funciones auxiliares
def AppendDatos():
	global t
	global nPresas
	global nPred
	global nDepred
	global nDatos
	global lsPresas
	global lsPred
	global lsDepred
	
	lsPresas.append(pos = (nDatos, nPresas))
	lsPred.append(pos = (nDatos, nPred))
	lsDepred.append(pos = (nDatos, nDepred))
	
	vTiempos.append(t)
	vPresas.append(nPresas)
	vPred.append(nPred)
	vDepred.append(nDepred)
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
	
def MataDepred(i):
	global arrayDepred
	AppendDatos()
	
	arrayDepred[i].figura.visible = False
	del arrayDepred[i].figura
	del arrayDepred[i]
	
def Guardar():
	global running
	
	filePresas = open('presas.csv', 'w')
	filePred = open('pred.csv', 'w')
	fileDepred = open('depred.csv', 'w')
	for index in range(nDatos):
		filePresas.write('{0:3d}, {1:3d}\n'.format(vTiempos[index], vPresas[index]))
		filePred.write('{0:3d}, {1:3d}\n'.format(vTiempos[index], vPred[index]))
		fileDepred.write('{0:3d}, {1:3d}\n'.format(vTiempos[index], vDepred[index]))
	filePresas.close()
	filePred.close()
	fileDepred.close()
	
# Controles
control = controls(title = 'Parametros', x = scene.width + 10, y = scene.y, width = 300, height = 300, range = 50)
boton = button( pos=(0,0), width=60, height=60, text='Guardar datos', action = lambda: Guardar() )

# Grafica
grafica = display(title="Animales", x=scene.x + scene.width + 8, y = control.y + control.width, width=384, height=300, background=(0, 0, 0))
#grafica.autoscale = True
grafica.xmin = 0
scene.select()
lsPresas = curve(display=grafica, color = color.yellow)
lsPred = curve(display = grafica, color = color.blue)
lsDepred = curve(display = grafica, color = color.red)

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
		
	for i in range(nDepred):
		randNumX = random.uniform(-1,1)
		randNumY = random.uniform(-1,1)
		arrayDepred[i].coord.Suma(randNumX, randNumY)
		arrayDepred[i].figura.pos = vector(arrayDepred[i].coord.x, arrayDepred[i].coord.y)
		
	# Revisa si depredadores y presas estan en contacto
	i = 0
	j = 0
	while i < nPresas and nPresas != 0:
		while j < nPred and nPred != 0:
			if arrayPresas[i].coord.x + distMortal > arrayPred[j].coord.x and arrayPresas[i].coord.x - distMortal < arrayPred[j].coord.x:
				if arrayPresas[i].coord.y + distMortal > arrayPred[j].coord.y and arrayPresas[i].coord.y - distMortal < arrayPred[j].coord.y:
					print("Mata Presa")
					# Mata a presa
					MataPresa(i)
					nPresas -= 1
					i -= 1
					# Reestablece vida del Predador
					arrayPred[j].vida = vidaMaxPred
			j += 1
					
		i += 1
		

	i = 0
	j = 0
	while i < nPred and nPred != 0:
		while j < nDepred and nDepred != 0:
			if arrayPred[i].coord.x + distMortal > arrayDepred[j].coord.x and arrayPred[i].coord.x - distMortal < arrayDepred[j].coord.x:
				if arrayPred[i].coord.y + distMortal > arrayDepred[j].coord.y and arrayPred[i].coord.y - distMortal < arrayDepred[j].coord.y:
					print("Mata Predador!!!")
					# Mata a Predador
					MataPred(i)
					nPred -= 1
					i -= 1
					# Reestablece vida del Depredador
					arrayDepred[j].vida = vidaMaxDepred
			j += 1
					
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
	while i < nDepred:
		arrayDepred[i].vida -= 1
		if arrayDepred[i].vida <= 0:
			MataDepred(i)
			nDepred -= 1
			AppendDatos()
		i += 1
	
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
		if nPresas != 0:
			crecPresas += cteCrecPresa
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
		if nPred != 0:
			crecPred += cteCrecPred*nPred
		else:
			crecPred += cteCrecPred
		
	# Nacen nuevos depredadores
	if crecDepred >= tasaCrecDepred:
		print("Nace depredador")
		posX = random.uniform(tableroXMin, tableroXMax)
		posY = random.uniform(tableroYMin, tableroYMax)
		arrayDepred.append(Depredador(posX, posY))
		crecDepred = 0
		nDepred += 1
		AppendDatos()
	else:
		if nDepred != 0:
			crecDepred += cteCrecDepred*nDepred
		else:
			crecDepred += cteCrecDepred
		
		
	t += 1

if  nPresas <= 0:
	print("Extincion masiva")
#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#title           : discos_duros.py
#description     : Simulador de discos duros.
#author          : Carlos Manuel Rodríguez, Jose Ramón Palacios
#usage           : python discos_duros.py  [opciones]
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from __future__ import division
from random import *
from numpy import *
from visual import *
import sys

withVPython = True	# Switch de modo visual
iterations = 100	# Número de veces que el sistema agita las partículas
initParticles = 1	# Número inicial de partículas en el sistema
totalLimit = 1          # Número total de partículas que acepta el sistema
shakes = 2		# Intentos extras para agregar partículas
dfolder = ''            # Directorio para dumps
dumpall = False
makecrystal = False
ignoreiter = 0
boxlength = 20
crystaltype = 0
dumpcoefd = False
dsmax = 1
importfile = ''

# Argumentos
def usage():
    print 'Ejemplo de uso: python discos_duros.py [opciones]'
    print '--particles=5000    | Necesaria           | Partículas para simulación.'
    print '--iterations=10000  | Necesaria           | Veces que se mueven las partículas.'
    print '--dumpfolder=dump1  | Opcional=.          | Sub-directorio para almacenar datos.'
    print '--visual=False      | Opcional=True       | Modo visual (VPython).'
    print '--shakes=100        | Opcional=2          | Intentos para agregar partículas.'
    print '--dumpall=False     | Opcional=False      | Dumpear todos los datos.'
    print '--makecrystal=False | Opcional=cuad,triag | Crea arreglo cristalino.'
    print '--ignoreiter=0      | Opcional=1000       | Ignora calculo prob en n iteraciones.'
    print '--boxlength=20      | Opcional=20         | Tamaño de la caja.'
    print '--dumpcoefd=False   | Opcional=True       | Dumpea coeficiente de desorden.'
    print '--import=NULL       | Opcional=coord.csv  | Importa archivo de coordenadas.'
    print '--dsmax=1           | Opcional=0.5        | Movimiento máximo de partícula.'
    print ''
    sys.exit(2);

if len(sys.argv) < 2: usage()
for a in sys.argv:
    if a[-3:] != '.py':
        o = a.split('=')
        if len(o) != 2: usage()
        if o[0] == '--visual':
            if o[1] in ('True', 'true', 'y', 'yes'):
                withVPython = True
            elif o[1] in ('False', 'false', 'n', 'no'):
                withVPython = False
            else: usage()
        elif o[0] == '--particles':
            totalLimit = int(o[1])
            if totalLimit <= 1: usage()
        elif o[0] == '--iterations':
            iterations = int(o[1])
            if iterations < 0: usage()
        elif o[0] == '--dumpfolder':
            dfolder = o[1]
        elif o[0] == '--shakes':
            shakes = int(o[1])
            if shakes < 1 : usage()
        elif o[0] == '--dsmax':
            dsmax = float(o[1])
        elif o[0] == '--dumpall':
            if o[1] in ('True', 'true', 'y', 'yes'):
                dumpall = True
            elif o[1] in ('False', 'false', 'n', 'no'):
                dumpall = False
        elif o[0] == '--makecrystal':
            if o[1] in ('cuad', 'Cuad'):
                makecrystal = True
                crystaltype = 0
            if o[1] in ('triag', 'Triag'):
                makecrystal = True
                crystaltype = 1
            elif o[1] in ('False', 'false', 'n', 'no'):
                makecrystal = False
        elif o[0] == '--ignoreiter':
            ignoreiter = int(o[1])
        elif o[0] == '--boxlength':
            boxlength = int(o[1])
        elif o[0] == '--dumpcoefd':
            if o[1] in ('True', 'true', 'y', 'yes'):
                dumpcoefd = True
            elif o[1] in ('False', 'false', 'n', 'no'):
                dumpcoefd = False
        elif o[0] == '--import':
            importfile = o[1]
        else: usage()
    
# Reportar opciones seleccionadas
print 'Parámetros y opciones'
print '-------------------------------------'
print '* Partículas: {0}'.format(totalLimit)
print '* Modo visual: {0}'.format(withVPython)
print '* Iteraciones: {0}'.format(iterations)
print '* Shakes: {0}'.format(shakes)

# Clase contenedora de coordenadas y figura del disco
class disk:
    def __init__(self,X,Y,R):
        self.x = X
        self.y = Y
        if withVPython: self.obj = visual.sphere(pos=(X,Y,0),radius=R, color=color.blue)

# Clase que provee interacción con el sistema de partículas
class system:
    N = 0 			# Num de partículas
    sigma = 1 			# Diámetro de partículas
    l = sigma*boxlength        	# Ancho de caja
    ds = dsmax  		# Salto mínimo
    disks = []			# Lista con los discos
    tGrid = 0.5*sigma		# Tamaño de elemento del grid (para conteo de frecuencia)
    gridSize = int(l/tGrid)	# Tamaño total del grid (en sigmas)
    # Nótese la correción de índice (la resta -2). Esto es debido a que la función que detecta
    # la posición en la caja toma en cuenta el radio de la partícula, por lo tanto hay dos índices dentro del
    # grid en los cuales ninguna partícula podra caer.

    # Revisa si la partícula esta dentro de la caja
    def insideBox(self,coordX, coordY):
        if (coordX - (self.sigma/2)) < -self.l/2: return False
        if (coordX + (self.sigma/2)) > self.l/2: return False
        if (coordY - (self.sigma/2)) < -self.l/2: return False
        if (coordY + (self.sigma/2)) > self.l/2: return False
        return True

    # Cambia el color de la partícula si esta fuera de la caja (auxiliar)
    def diskOutside(self):
        for i in range(0, self.N):
           if(not self.insideBox(i)): 
               self.disks[i].obj.color = color.blue

    # Revisa si algun disco se traslapa
    def diskOverlap(self, coordX, coordY, index=-1):
        if(len(self.disks)==1): return False
        for i in range(0, len(self.disks)):
            if((i == index) and index != -1): continue
            if( ((self.disks[i].x-coordX)**2 + (self.disks[i].y-coordY)**2) < (self.sigma)**2 ):
                return True
        return False                    

    # Añade un número fijo de partículas al sistema
    def addParticles(self, n):
        tempX = uniform(-self.l/2,self.l/2)
        tempY = uniform(-self.l/2,self.l/2)
        while(len(self.disks) < n):
            if (not self.diskOverlap(tempX, tempY)) and self.insideBox(tempX, tempY):
                self.disks.append(disk(tempX, tempY,self.sigma/2))
            tempX = uniform(-self.l/2,self.l/2)
            tempY = uniform(-self.l/2,self.l/2)
        self.N = len(self.disks)

    # Intenta añadir partículas al sistema ('n' intentos)
    def tryToAddParticles(self, n, totalLimit):
        tempX = uniform(-self.l/2,self.l/2)
        tempY = uniform(-self.l/2,self.l/2)

        i = 0
        while((i < n) and (self.N < totalLimit)):
            if (not self.diskOverlap(tempX, tempY)) and self.insideBox(tempX, tempY):
                self.disks.append(disk(tempX, tempY,self.sigma/2))
                self.N += 1
            tempX = uniform(-self.l/2,self.l/2)
            tempY = uniform(-self.l/2,self.l/2)
            i += 1

    # Crea arreglo cristalino
    def makecrystal(self):
        if (totalLimit > self.l**2):
            print 'Demasiadas partículas. Máximo para tamaño de caja seleccionado: {0}'.format(self.l**2)
            sys.exit(2)
        nxy = int(self.sigma*math.sqrt(totalLimit))  # Cantidad de partículas por fila y por columna
        if floor(math.sqrt(totalLimit)) != math.sqrt(totalLimit): nxy += 1
        a = (self.l - nxy*self.sigma)/nxy # Factor de espaciamiento
        y = -self.l/2 + self.sigma/2
        for i in range(0, nxy):
            x = -self.l/2 + self.sigma/2
            for j in range(0, nxy):
                tx = x + j*a
                ty = y + i*a
                if(not self.diskOverlap(tx,ty) and self.insideBox(tx,ty)):
                    self.disks.append(disk(tx, ty, self.sigma/2))
                    self.N += 1
                if(self.N == totalLimit): return
                x += self.sigma
            y += self.sigma

    def maketriangcrystal(self):
        hfactor = math.sqrt(3.0)/2.0 # Factor de espaciamiento para arreglo triangular
	even = True  # Indicador de paridad
	corrf = 0.000001 # Correción de error en variable double
	y =  -self.l/2 + self.sigma/2
	while (y < self.l/2):
		if even:
        		x = -self.l/2 + self.sigma/2
		else:
			x = -self.l/2 + self.sigma
		even = not even  # Desplaza las filas impares medio sigma
		while (x < self.l/2):
			if(not self.diskOverlap(x,y) and self.insideBox(x,y)):
					self.disks.append(disk(x, y, self.sigma/2))
					self.N += 1
			if(self.N == totalLimit): return
			x += self.sigma
		y += hfactor*self.sigma+corrf
				
    # Mueve las partículas
    def shakeSystem(self):
        denied = 0
        for i in range(0, self.N):
            nPosX = uniform(-self.ds, self.ds)
            nPosY = uniform(-self.ds, self.ds)
            tx = self.disks[i].x + nPosX
            ty = self.disks[i].y + nPosY
            if( (not self.diskOverlap(tx,ty, i)) and self.insideBox(tx,ty) ):
                self.disks[i].x = tx
                self.disks[i].y = ty
                if withVPython:
                    self.disks[i].obj.pos = vector(self.disks[i].x, self.disks[i].y, 0)
            else:
                denied += 1
        return (self.N-denied)/self.N

    # Constructor predeterminado
    def __init__(self, particles):
        if(importfile in ('NULL', 'null', '')):
            if(not makecrystal):
                self.N = particles
                self.addParticles(self.N)
        else:
            data = [i.strip().split() for i in open(importfile).readlines()]
            for x in data:
                if(self.N == totalLimit): break
                self.disks.append(disk(float(x[0]), float(x[1]),self.sigma/2))
                self.N += 1

            global shakes
            shakes = 0

        # Genera grid y flatGrid
        if(self.tGrid < self.sigma/2): 
            self.gridSize = int(self.l/self.tGrid)-2	# Tamaño total del grid (en sigmas)

        self.grid = zeros((self.gridSize, self.gridSize))
        self.flatGrid = zeros(self.gridSize)


    # Aumenta el contador del grid segun la posición de las partículas
    def calcProb(self):
        for i in range(0, self.N):
            if(self.tGrid < self.sigma/2):
                tx = int((self.disks[i].x+(self.l/2)-(self.sigma/2)) / self.tGrid)
                ty = int((self.disks[i].y+(self.l/2)-(self.sigma/2)) / self.tGrid)
            else:
                tx = int((self.disks[i].x+(self.l/2)) / self.tGrid)
                ty = int((self.disks[i].y+(self.l/2)) / self.tGrid)
            
            self.grid[tx][ty] += 1

    # Realiza un promedio (2D) del grid
    def makeFlatGrid(self):
	for i in range(1, self.gridSize-1):
		for j in range(0, self.gridSize):
			self.flatGrid[j] += self.grid[i][j]
	for i in range(0, self.gridSize):
		self.flatGrid[i] /= self.gridSize

    # Hace corte de la sección a la mitad en el grid 3D
    def makeSliceFlatGrid(self):
	for i in range(0, self.gridSize):
		self.flatGrid[i] = self.grid[int(self.gridSize/2)][i]

    # Dumpea el flatGrid en un archivo (flatGrid es la sección 2D de corte del grid 3D)
    def dumpFlatGrid(self, limit):
        fname = 'flatGrid.csv'
        if dfolder != '': fname = dfolder + '/' + fname
	f = open(fname, 'w')
	for i in range(0, self.gridSize):
		f.write('{0}, {1}\n'.format(i, self.flatGrid[i]/(limit*self.tGrid**2)))
	f.close()

    # Guarda el grid en un archivo
    def dumpGrid(self, limit, name):
        fname = name + '.csv'
        gname = name + '_densidad.csv'
        if dfolder != '': 
            fname = dfolder + '/' + fname
            gname = dfolder + '/' + gname
        f = open(fname, 'w')
        g = open(gname, 'w')
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                f.write('{0}, {1}, {2}\n'.format(i, j, self.grid[i][j]/limit))
                g.write('{0}, {1}, {2}\n'.format(i, j, self.grid[i][j]/(limit*self.tGrid**2)))
        f.close()
        g.close()

# Se declara sistema
s = system(initParticles)

# Caja
if withVPython:
    visual.box(pos=(0,0,-1),axis=(1,0,0),height=s.l, width=0.2,length=s.l, material=materials.wood, color=color.white)
    visual.rate(500)

# Reportar opciones extras
print '* Sigma: {0}'.format(s.sigma)
print '* L: {0}*sigma'.format(s.l)
print '* Cuadrícula: {0}*sigma'.format(s.tGrid)
print ''

# Se añaden partículas al sistema
if makecrystal:
    if crystaltype == 0:
        s.makecrystal()
    else:
        s.maketriangcrystal()
else:
    for i in range(0, shakes):
        if(s.N != totalLimit):
            s.shakeSystem()
            s.calcProb()
            s.tryToAddParticles(200, totalLimit)
        p = (i/shakes)*100 + 1
        sys.stdout.write('\rShakes: %d%%, Particulas: {0}'.format(s.N) %p)
        sys.stdout.flush()

print('')
print('Se agregaron {0} particulas'.format(s.N))

#sys.exit(2)

modulus = iterations*0.01	# Controla la frecuencia con la que se actualiza el contador de avance
dumpIndex = 0			# Índice de archivos de salida
dumpMod = iterations / 10	# Controla el número de archivos de salida que se generarán
ignoreModulus = ignoreiter*0.01

# Loop principal
n = 0
if ignoreiter != 0:
    while n<= ignoreiter:
        s.shakeSystem()
        if(n % ignoreModulus == 0):
            t = (n/ignoreiter)*100
            sys.stdout.write('\rDesordenando: %d%%' %t)
            sys.stdout.flush()
        n += 1

print('')
n = 0
coefarray = []

while n < iterations:
    dfactor = s.shakeSystem()	# Mueve particulas   if n > ignoreiter:
    s.calcProb()	# Actualiza grid
    if dumpcoefd:
        coefarray.append(dfactor)
    
    if(n % modulus == 0):
        t = (n/iterations)*100
        sys.stdout.write('\rProgreso: %d%% Aceptacion: {0}'.format(dfactor) %t)
        sys.stdout.flush()
        
    if(n % dumpMod == 0 and dumpall):
        s.dumpGrid(iterations, 'dump_{0}'.format(dumpIndex))
        dumpIndex += 1
    n += 1

if(not dumpall):
    s.dumpGrid(iterations, 'dump')

s.makeFlatGrid()	# Se selecciona el tipo de corte antes de dumpear el flatGrid
s.dumpFlatGrid(iterations)

if dumpcoefd:
    i = 0
    f = open('coefd.csv', 'w')
    while i < len(coefarray):
        f.write('{0}, {1} \n'.format(i,coefarray[i]))
        i += 1
    f.close()
print ''

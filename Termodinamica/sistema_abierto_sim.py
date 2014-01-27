#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Simulador de un sistema termodinámico abierto.
#author          : Carlos Manuel Rodríguez
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from __future__ import division
from random import *
from numpy import *
from visual import *
from visual.graph import *
from visual.controls import *

# Variables y parámetros
dt = 0.01                  # Intervalo temporal
plotEnergy = True
movePiston = False
scene.width = 900
scene.height = 480
scene.title = 'Simulacion: Termodinamica'

# Clase contenedora de coordenadas y figura del disco
class disk:
    def __init__(self, X, Y, VX, VY, R, pColor):
        self.x = X
        self.y = Y
        self.vx = VX
        self.vy = VY
        self.obj = visual.sphere(pos=(X,Y,0),radius=R, color=pColor)

class system:
    N = 0 			# Num de partículas.
    sigma = 1 			# Diámetro de partículas.
    disks = []			# Lista con los discos.
    walls = [1,1,1,1]           # Izquierda, derecha, arriba, abajo. Paredes del sistema.
    wallArray = []              # Array con los objetos de muro
    
    def __init__(self, coordX, coordY, systemSize, systemColor=color.white, systemWalls = [], maxVel = 1):
        self.x = coordX
        self.y = coordY
        self.size = systemSize
        self.vMax = maxVel
        self.obj = box(pos=(coordX+systemSize/2, coordY+systemSize/2, -1), axis=(1,0,0), height=self.size, width=0.2,length=self.size, material=materials.wood, color=systemColor)
        wallSize = 1
        if (len(systemWalls) != 0):
             self.walls = systemWalls
        if (self.walls[0] == 1):
            self.wallArray.append(box(pos=(coordX-wallSize/2, coordY+systemSize/2, -0.5), axis=(1,0,0), height=self.size, width=1, length=1))
        if (self.walls[1] == 1):
            self.wallArray.append(box(pos=(coordX+systemSize, coordY+systemSize/2, -0.5), axis=(1,0,0), height=self.size, width=1, length=1))
        if (self.walls[2] == 1):
            self.wallArray.append(box(pos=(coordX+systemSize/2, coordY+systemSize, -0.5), axis=(0,1,0), height=self.size, width=1, length=1))
        if (self.walls[3] == 1):
            self.wallArray.append(box(pos=(coordX+systemSize/2, coordY, -0.5), axis=(0,1,0), height=self.size, width=1, length=1))

    def insideBox(self,coordX, coordY):
        if (coordX - (self.sigma/2)) < -self.size/2: return False
        if (coordX + (self.sigma/2)) > self.size/2: return False
        if (coordY - (self.sigma/2)) < -self.size/2: return False
        if (coordY + (self.sigma/2)) > self.size/2: return False
        return True

    def diskOverlap(self, coordX, coordY, index=-1):
        if(len(self.disks)==1): return False
        for i in range(0, len(self.disks)):
            if((i == index) and index != -1): continue
            if( ((self.disks[i].x-coordX)**2 + (self.disks[i].y-coordY)**2) < (self.sigma)**2 ):
                return True
        return False  

    def addParticles(self, n, partColor = color.blue):
        tempX = uniform(-self.size/2,self.size/2)
        tempY = uniform(-self.size/2,self.size/2)
        while(len(self.disks) < n):
            if (not self.diskOverlap(tempX, tempY)) and self.insideBox(tempX, tempY):
                self.disks.append(disk(tempX, tempY, uniform(-self.vMax, self.vMax), uniform(-self.vMax, self.vMax) ,self.sigma/2, partColor))
                index = len(self.disks)-1
                self.disks[index].obj.pos = vector(self.disks[index].x + self.size/2 + self.x, self.disks[index].y + self.size/2 + self.y, 0)
            tempX = uniform(-self.size/2,self.size/2)
            tempY = uniform(-self.size/2,self.size/2)
        self.N = len(self.disks)

    def moveParticles(self):
        for i in range(0, self.N):
            tempX = self.disks[i].x + self.disks[i].vx*dt
            tempY = self.disks[i].y + self.disks[i].vy*dt

            # Pared de la izquierda
            if (self.walls[0] == 1):
                if(tempX < -self.size/2):
                    self.disks[i].vx = -self.disks[i].vx
                    self.disks[i].x = -self.size/2

            # Pared de la derecha
            if (self.walls[1] == 1):
                if(tempX > self.size/2):
                    self.disks[i].vx = -self.disks[i].vx
                    self.disks[i].x = self.size/2

            # Pared de arriba
            if (self.walls[2] == 1):
                if(tempY > self.size/2):
                    self.disks[i].vy = -self.disks[i].vy
                    self.disks[i].y = self.size/2

            # Pared de abajo
            if (self.walls[3] == 1):
                if(tempY < -self.size/2):
                    self.disks[i].vy = -self.disks[i].vy
                    self.disks[i].y = -self.size/2

            self.disks[i].x = tempX
            self.disks[i].y = tempY
            self.disks[i].obj.pos = vector(self.disks[i].x + self.size/2 + self.x, self.disks[i].y + self.size/2 + self.y, 0)

    def getTotalEnergy(self):
        totEner = 0
        for i in range(0, self.N):
            totEner += self.disks[i].vx**2 + self.disks[i].vy**2
        return totEner


class piston:
    systemSize = 2
    sHeight = 1
    def __init__(self, coordX, coordY, myHeight):
        self.sHeight = myHeight
        self.x = coordX
        self.y = coordY
        self.obj1 = box(pos=(coordX+ self.systemSize/2, coordY + self.sHeight/2, -0.5), axis=(1,0,0), height=self.sHeight, width=0.2,length=self.systemSize, color=color.green)
        self.obj2 = cylinder(pos=(coordX+ self.systemSize/2, coordY + self.sHeight/2, -1), axis=(1,0,0), radius=0.7, length=7)

    def move(self, coordX, coordY):
        self.obj1.pos = vector(coordX+self.systemSize/2, coordY+self.sHeight/2, -0.5)
        self.obj2.pos = vector(coordX+self.systemSize/2, coordY+self.sHeight/2, -1)

class pistonSystem:
    movingPiston = False
    N = 0 			# Num de partículas.
    sigma = 1 			# Diámetro de partículas.
    disks = []			# Lista con los discos.
    walls = [1,1,1,1]           # Izquierda, derecha, arriba, abajo. Paredes del sistema.
    wallArray = []              # Array con los objetos de muro
    
    def __init__(self, coordX, coordY, systemSize, pistonWall, systemColor=color.white, systemWalls = [], maxVel = 1, maxPistonVel = 1):
        self.x = coordX
        self.y = coordY
        self.size = systemSize
        self.vMax = maxVel
        self.pistonVel = maxPistonVel
        self.obj = box(pos=(coordX+systemSize/2, coordY+systemSize/2, -1), axis=(1,0,0), height=self.size, width=0.2,length=self.size, material=materials.wood, color=systemColor)
        wallSize = 1
        if (len(systemWalls) != 0):
             self.walls = systemWalls
        self.walls[pistonWall] = 0
        if (self.walls[0] == 1):
            self.wallArray.append(box(pos=(coordX-wallSize/2, coordY+systemSize/2, -0.5), axis=(1,0,0), height=self.size, width=1, length=1))
        if (self.walls[1] == 1):
            self.wallArray.append(box(pos=(coordX+systemSize, coordY+systemSize/2, -0.5), axis=(1,0,0), height=self.size, width=1, length=1))
        if (self.walls[2] == 1):
            self.wallArray.append(box(pos=(coordX+systemSize/2, coordY+systemSize, -0.5), axis=(0,1,0), height=self.size, width=1, length=1))
        if (self.walls[3] == 1):
            self.wallArray.append(box(pos=(coordX+systemSize/2, coordY, -0.5), axis=(0,1,0), height=self.size, width=1, length=1))

        self.pistonPos = self.size/2
        self.objPiston = piston(coordX + self.pistonPos + self.size/2, coordY, systemSize)

    def getTotalEnergy(self):
        totEner = 0
        for i in range(0, self.N):
            totEner += self.disks[i].vx**2 + self.disks[i].vy**2
        return totEner

    def moveParticles(self):
        for i in range(0, self.N):
            tempX = self.disks[i].x + self.disks[i].vx*dt
            tempY = self.disks[i].y + self.disks[i].vy*dt
            hitsX = False
            hitsY = False
            
            # Pared de la izquierda
            if (self.walls[0] == 1):
                if(tempX < -self.size/2):
                    self.disks[i].vx = -self.disks[i].vx
                    self.disks[i].x = -self.size/2
                    hitsX = True

            # Pared de la derecha
            if (self.walls[1] == 1):
                if(tempX > self.size/2):
                    self.disks[i].vx = -self.disks[i].vx
                    self.disks[i].x = self.size/2
                    hitsX = True

            # Pared de arriba
            if (self.walls[2] == 1):
                if(tempY > self.size/2):
                    self.disks[i].vy = -self.disks[i].vy
                    self.disks[i].y = self.size/2
                    hitsY = True

            # Pared de abajo
            if (self.walls[3] == 1):
                if(tempY < -self.size/2):
                    self.disks[i].vy = -self.disks[i].vy
                    self.disks[i].y = -self.size/2
                    hitsY = True

            # Pistón
            if(tempX > self.pistonPos):
                self.disks[i].vx = -self.disks[i].vx
                if(self.movingPiston):
                    self.disks[i].vx -= self.pistonVel
                self.disks[i].x = self.pistonPos - dt*self.pistonVel
                hitsX = True

            if(not hitsX):
                self.disks[i].x = tempX
            if(not hitsY):
                self.disks[i].y = tempY
            self.disks[i].obj.pos = vector(self.disks[i].x + self.size/2 + self.x, self.disks[i].y + self.size/2 + self.y, 0)

    def movePiston(self):
        self.movingPiston = True
        if(self.pistonPos >= -self.size/2 + 0.2):
            self.pistonPos -= dt*self.pistonVel
        else:
            self.pistonVel = 0
        self.objPiston.move(self.x + self.pistonPos + self.size/2, self.y)

    def insideBox(self,coordX, coordY):
        if (coordX - (self.sigma/2)) < -self.size/2: return False
        if (coordX + (self.sigma/2)) > self.size/2: return False
        if (coordY - (self.sigma/2)) < -self.size/2: return False
        if (coordY + (self.sigma/2)) > self.size/2: return False
        return True

    def diskOverlap(self, coordX, coordY, index=-1):
        if(len(self.disks)==1): return False
        for i in range(0, len(self.disks)):
            if((i == index) and index != -1): continue
            if( ((self.disks[i].x-coordX)**2 + (self.disks[i].y-coordY)**2) < (self.sigma)**2 ):
                return True
        return False  

    def addParticles(self, n, partColor = color.blue):
        tempX = uniform(-self.size/2,self.size/2)
        tempY = uniform(-self.size/2,self.size/2)
        while(len(self.disks) < n):
            if (not self.diskOverlap(tempX, tempY)) and self.insideBox(tempX, tempY):
                self.disks.append(disk(tempX, tempY, uniform(-self.vMax, self.vMax), uniform(-self.vMax, self.vMax) ,self.sigma/4, partColor))
                index = len(self.disks)-1
                self.disks[index].obj.pos = vector(self.disks[index].x + self.size/2 + self.x, self.disks[index].y + self.size/2 + self.y, 0)
            tempX = uniform(-self.size/2,self.size/2)
            tempY = uniform(-self.size/2,self.size/2)
        self.N = len(self.disks)

def MoveP():
    global movePiston
    movePiston = not movePiston

def RemovePWalls():
    global s
    global p
    p.walls[0] = 0
    p.wallArray[0].visible = False
    s.wallArray[1].opacity = 0.5

def MovePandWall():
    MoveP()
    RemovePWalls()

def transferParticles():
    global s
    global p

    # Revisa si partículas de p entraron a s
    i = 0
    while(i < len(p.disks)):
        if(p.disks[i].x < -p.size/2):
            s.disks.append(p.disks[i])
            index = len(s.disks)-1
            s.disks[index].x = s.size/2
            s.disks[index].y = -s.size/2 + (p.size/s.size)*(s.disks[index].y+s.size/2)
            p.disks.pop(i)
            p.N -= 1
            s.N += 1
            i -= 1
        i += 1

# Declaración de sistema
s = system(-10,-10,20, color.blue)
p = pistonSystem(10, -10, 10, 1, color.red, maxPistonVel = 0.6)
s.addParticles(50, color.blue)
p.addParticles(60, color.red)

# Controles
control = controls(title = 'Parametros', x = scene.x+scene.width, y = scene.y, width = 400, height = 400, range = 50)
pistonButton = button(pos = (0,30), height = 15, width = 30, text = 'Mover Piston', action=lambda: MoveP())
wallsButton = button(pos = (0,10), height = 15, width = 30, text = 'Eliminar pared', action=lambda: RemovePWalls())
moveAllButton = button(pos = (0,-10), height = 15, width = 40, text = 'Introduce particulas', action=lambda: MovePandWall())

if plotEnergy:
    gd = gdisplay(x=scene.x, y=scene.y+scene.height, width=600, height=300, title='Energia', xtitle='t', ytitle='E')
    f1 = gcurve(color=color.cyan)
    f2 = gcurve(color=color.blue)
    f3 = gcurve(color=color.red)

t = 0
while True:
    visual.rate(500)
    s.moveParticles()
    p.moveParticles()
    transferParticles()
    if movePiston:
        p.movePiston()
    if plotEnergy:
        f1.plot(pos = (t, s.getTotalEnergy() + p.getTotalEnergy()))
        f2.plot(pos = (t, s.getTotalEnergy()))
        f3.plot(pos = (t, p.getTotalEnergy()))
    t += dt

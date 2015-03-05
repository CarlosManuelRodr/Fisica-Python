#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Grafica trayectoria de un proyectil en un medio resistente.
#author          : José Ramón Palacios, 2010 - palacios_barreda@hotmail.com
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from numpy import *
import pylab

# Parámetros
g = 9.81;
k = 2;
phi = 0.0;
v = 50.0;

# Posición de la partícula en función del tiempo
for n in range(15,90,15):
    # Iteramos sobre el valor del ángulo de disparo
    phi = radians(n);

    # Hallar tau mediante el método del punto fijo
    tau = 0.1; # Suposición inicial, basta con t > 0.
    tmp = 0;
    m = 0;
    ignorar = False;
    while (abs(tau - tmp) > 1e-4):
        tmp = tau;
        tau = ((k*v*sin(phi) + g)/(g*k))*(1 - exp(-k*tau));
        if (m > 10000):
            print u'Punto fijo no converge para phi = %d°' % n
            ignorar = True;
            break;
    
    # Calcular y graficar trayectoria
    if (ignorar==False):
        print u'tau=%.4f para phi=%.1f°' % (tau,degrees(phi))
        t = linspace(0,tau,100);
        x = (v*cos(phi)/k)*(1 - exp(-k*t));
        y = ((k*v*sin(phi) + g)/(k**2))*(1 - exp(-k*t)) - t*(g/k);    
        pylab.plot(x,y,label=u'$\phi ={0}$'.format(degrees(phi)));

# Detalles de la gráfica
pylab.xlabel('$x$ (m)');
pylab.ylabel('$y$ (m)');
pylab.title(u'Trayectoria de una partícula en un medio resistente: $F_R = kmv$');
pylab.grid(True);
pylab.axis('auto');
pylab.legend();
pylab.annotate('$k = 2$', xy=(2, 15), xytext=(2, 15), fontsize=14);
pylab.savefig('trayectoria.png', format='png');
pylab.show();
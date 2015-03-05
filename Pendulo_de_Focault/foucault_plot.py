#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
#description     : Graficador de trayectoria del péndulo de foucault.
#author          : José Ramón Palacios, 2010 - palacios_barreda@hotmail.com
#notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
#python_version  : 2.7  
#========================================================================================

from numpy import *
import pylab

# Parámetros
# Unidades SI
h = 0.01
A = 1;
g = 9.81;
l = 10;
omega = (2*pi)/(3600.*24.);
beta = 0;
tau = 1*120;
t = linspace(0,tau,tau*(1/h));

# Soluciones analíticas
for n in range(0,100,45):
    #Iteramos sobre el valor de la colatitud
    beta = radians(n);
    x = A*cos(sqrt(g/l)*t)*sin(omega*cos(beta)*t);
    y = A*cos(sqrt(g/l)*t)*cos(omega*cos(beta)*t);

    #Detalles de la gráfica
    pylab.plot(x,y,label=u'Colatitud = {0}°'.format(degrees(beta)));
    if(n==45):
        tx = x;
        ty = y;    

pylab.xlabel('$x$ (m)');
pylab.ylabel('$y$ (m)');
pylab.title(u'Trayectoria del Péndulo de Focault (t = {0} min)'.format(tau/60.));
pylab.grid(True);
pylab.axis('auto');
pylab.legend();
pylab.savefig('focault_trayectorias.png', format='png');
pylab.clf();

# Magnitud del vector de posición (estabilidad de solución)
pylab.plot(t, sqrt(x**2 + y**2),label=u'Magnitud del vector de posición');
pylab.xlabel('$t$ (s)');
pylab.ylabel('$r$ (m)');
pylab.title('$r = \sqrt{x^2 + y^2}$');
pylab.grid(True);
pylab.axis([0,amax(t),-5,10]);
pylab.legend();
pylab.savefig('focault_vecposicion_analitica.png', format='png');
pylab.clf();

# *******************************************************************
# Método numérico: Euler explícito/Forward Euler
# *******************************************************************
beta = radians(45);
tsize = tau/h;
xn = zeros(tsize);
yn = zeros(tsize); yn[0] = A;
energ = zeros(tsize);
vx = 0.;
vy = 0.;
energiaTot = 0.5*(vx**2 + vy**2) + 0.5*(g/l)*(xn[0]**2 + yn[0]**2);
error = zeros(tsize);
n = 1;
t = h;
while (n < tsize):
    # Calcular posiciones
    xn[n] = xn[n-1] + vx*h;
    yn[n] = yn[n-1] + vy*h;
    # Calcular velocidades (método de Euler)
    vx += h*( (-g/l)*xn[n] + (2*omega*sin(beta)/l)*xn[n]*vy + (2*omega*cos(beta))*vy );
    vy += h*( (-g/l)*yn[n] + (2*omega*sin(beta)/l)*yn[n]*vy - (2*omega*cos(beta))*vx );
    # Calcula energia
    error[n] = abs(0.5*(vx**2 + vy**2) + 0.5*(g/l)*(xn[n]**2 + yn[n]**2) - energiaTot)/energiaTot; 
    
    n += 1;
    t += h;

pylab.plot(xn,yn,label=u'Colatitud = {0}°'.format(degrees(beta)));
pylab.xlabel('$x$ (m)');
pylab.ylabel('$y$ (m)');
pylab.title(u'Trayectoria del Péndulo de Focault (t = {0} min)'.format(tau/60.));
pylab.grid(True);
pylab.axis('auto');
pylab.legend();
pylab.savefig('focault_trayectoria_euler.png', format='png');

# Magnitud del vector de posición (estabilidad de solución)
pylab.clf();
pylab.plot(sqrt(xn**2 + yn**2),label=u'Magnitud del vector de posición');
pylab.xlabel(u'Iteración');
pylab.ylabel('$r$ (m)');
pylab.title('$r = \sqrt{x^2 + y^2}$');
pylab.grid(True);
pylab.axis([0,tsize,-5,10]);
pylab.legend();
pylab.savefig('focault_vecposicion_euler.png', format='png');

# Comparación entre ambas soluciones

# Error
pylab.clf();
pylab.plot(error,label='$eTot - e$');
pylab.xlabel(u'Iteración');
pylab.ylabel('$eTot - e$ (m)');
pylab.title(u'Error relativo');
pylab.grid(True);
pylab.axis('auto');
pylab.legend();
pylab.savefig('focault_error_energy.png', format='png');
Simulador de péndulo doble
=========================

Realiza una simulación del sistema de péndulo doble. Utiliza el método de euler para resolver las ecuaciones.
* "pendulo_doble_sim.py": Simulador convencional del péndulo doble.
* "pendulo_doble_nModes.py": Simulador con parámetros iniciales correspondientes a los modos normales, que se calculan en "Calc_nModes.nb".
* "pendulo_doble_plot.py": Graficador de trayectorias de péndulo doble.

Instrucciones
=============

```
Modo de uso: python pendulo_doble_sim.py [opciones]
Ejemplo: python pendulo_doble_sim.py --th1init=1 --th2init=-0.7

--th1init=1        | Necesaria           | Angulo 1 inicial.
--th2init=1        | Necesaria           | Angulo 2 inicial.
--deltat=0.01      | Opcional            | Intervalo temporal en sim.
--m1=10            | Opcional            | Masa del cuerpo 1.
--m2=10            | Opcional            | Masa del cuerpo 2.
--length=20        | Opcional            | Longitud de las cuerdas.
--gravity=9.8      | Opcional            | Valor de la gravedad.
--ploterror=True   | Opcional=True,False | Graficar error numerico.
```
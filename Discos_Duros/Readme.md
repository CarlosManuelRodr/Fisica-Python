Simulador de discos duros
=========================

Realiza una simulación de partículas con movimiento aleatorio. Si se translapan, se rechaza el movimiento, en caso contrario se acepta.
El programa genera una salida de los valores de densidad. Para más información véase documento adjunto.

Instrucciones
=============

```
Ejemplo de uso: python discos_duros.py [opciones]
--particles=5000    | Necesaria           | Partículas para simulación.
--iterations=10000  | Necesaria           | Veces que se mueven las partículas.
--dumpfolder=dump1  | Opcional=.          | Sub-directorio para almacenar datos.
--visual=False      | Opcional=True       | Modo visual (VPython).
--shakes=100        | Opcional=2          | Intentos para agregar partículas.
--dumpall=False     | Opcional=False      | Dumpear todos los datos.
--makecrystal=False | Opcional=cuad,triag | Crea arreglo cristalino.
--ignoreiter=0      | Opcional=1000       | Ignora calculo prob en n iteraciones.
--boxlength=20      | Opcional=20         | Tamaño de la caja.
--dumpcoefd=False   | Opcional=True       | Dumpea coeficiente de desorden.
--import=NULL       | Opcional=coord.csv  | Importa archivo de coordenadas.
--dsmax=1           | Opcional=0.5        | Movimiento máximo de partícula.
```

Se incluye un script para crear un set de datos listo para graficar con el archivo de Mathematica "Plots.nb". Para ejecutar este script es necesario ejecutarlo en Linux o un sistema similar.
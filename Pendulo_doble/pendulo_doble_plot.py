# Encoding: utf-8
from numpy import *
import pylab
import sys
import wx
import wx.xrc
from threading import Thread 

# Condiciones iniciales de la simulacion
th1_init = 1
vth1_init = 0.0
th2_init = 1
vth2_init = 0.0

# Variables de la simulacion
m1 = 10
m2 = 10
l = 20
g = 9.81

#Parámetros
deltat = 0.001	# Intervalo de tiempo para cada paso en la simulacion
t = 0.0			# Contador de tiempo
tMax = 20
integrator = 1

# Parámetros opcionales
def usage():
    print 'Ejemplo de uso: pendulo_doble_sim.py [opciones]'
    print '--th1init=1        | Necesaria           | Angulo 1 inicial.'
    print '--th2init=1        | Necesaria           | Angulo 2 inicial.'
    print '--deltat=0.01      | Opcional            | Intervalo temporal en sim.'
    print '--m1=10            | Opcional            | Masa del cuerpo 1.'
    print '--m2=10            | Opcional            | Masa del cuerpo 2.'
    print '--length=20        | Opcional            | Longitud de las cuerdas.'
    print '--gravity=9.8      | Opcional            | Valor de la gravedad.'
    print '--ploterror=True   | Opcional=True,False | Graficar error numerico.'
    print '--integrator=RK    | Opcional=RK,E       | Integrador: Runge-Kutta o Euler.'
    print ''
    sys.exit(2);

if len(sys.argv) < 2: usage()
for a in sys.argv:
    if a[-3:] != '.py':
        o = a.split('=')
        if len(o) != 2: usage()
        if o[0] == '--th1init':
            th1_init = float((o[1]))
        elif o[0] == '--th2init':
            th2_init = float((o[1]))
        elif o[0] == '--deltat':
            deltat = float((o[1]))
            cps = 3.0/deltat
        elif o[0] == '--m1':
            m1 = float((o[1]))
        elif o[0] == '--m2':
            m2 = float((o[1]))
        elif o[0] == '--length':
            l = float((o[1]))
        elif o[0] == '--gravity':
            g = float((o[1]))
        elif o[0] == '--ploterror':
            if o[1] in ('True', 'true', 'y', 'yes'):
                plotError = True
            elif o[1] in ('False', 'false', 'n', 'no'):
                plotError = False
            else: usage()
        elif o[0] == '--integrator':
            if o[1] in ('RK', 'rk', 'Rk', 'rK'):
                integrator = 1
            elif o[1] in ('E', 'e', 'Euler', 'euler'):
                integrator = 0
            else: usage()
        else: usage()

# Asigna valores a variables de sim
th1 = th1_init
vth1 = vth1_init
th2 = th2_init
vth2 = vth2_init

th1Array = []
vth1Array = []
th2Array = []
vth2Array = []

i = 0
maxIter = tMax/deltat

# Crea gráfica.
fig = pylab.figure() 
fig.canvas.set_window_title('Grafica de espacio fase') 

def makeCalc():
	global i
	global th1
	global th2
	global vth1
	global vth2
	
	if integrator == 0:
		while i < maxIter:
			if m1 == 0 or m2 == 0:
				pass
			else:
				# Calcula posición de las masas por el método de Euler
				ecMov1 = -g*(m1+m2)*math.sin(th1)+g*m2*math.sin(th2)*math.cos(th1-th2)-l*m2*(vth2**2)*math.sin(th1-th2)-l*m2*(vth1**2)*math.sin(th1-th2)*math.cos(th1-th2)
				ecMov1 /= l*(m1+m2)-l*m2*(cos(th1-th2)**2)
				ecMov2 = (m1+m2)*l*(vth1**2)*math.sin(th1-th2)-(m1+m2)*g*math.sin(th2)+m2*l*(vth2**2)*math.sin(th1-th2)*math.cos(th1-th2)+(m1+m2)*g*math.sin(th1)*math.cos(th1-th2)
				ecMov2 /= l*(m1+m2)-l*m2*(cos(th1-th2)**2)
				vth1 += deltat*ecMov1
				vth2 += deltat*ecMov2
				th1 += deltat*vth1
				th2 += deltat*vth2
				
			th1Array.append(th1)
			vth1Array.append(vth1)
			th2Array.append(th2)
			vth2Array.append(vth2)
			
			i += 1
	else:
		while i < maxIter:
			if m1 == 0 or m2 == 0:
				pass
			else:
				# Calcula posición de las masas por el método de Runge-Kutta		
				den = l*(2*m1+m2-m2*cos(2*(th1-th2)));
				k11 = -g*(2*m1+m2)*sin(th1)-m2*g*sin(th1-2*th2)-2*sin(th1-th2)*m2*(l*(pow(vth2,2)+pow(vth1,2)*cos(th1-th2)));
				k11 /= den;
				k11 *= deltat;
				k21 = 2*sin(th1-th2)*(g*(m1+m2)*cos(th1)+l*(pow(vth2,2)*m2*cos(th1-th2)+pow(vth1,2)*(m1+m2)));
				k21 /= den;
				k21 *= deltat;

				den = l*(2*m1+m2-m2*cos(2*(th1 + k11/2.0 - (th2 + k21/2.0))));
				k12 = -g*(2*m1+m2)*sin(th1 + k11/2.0)-m2*g*sin(th1 + k11/2.0-2*(th2 + k21/2.0))-2*sin(th1 + k11/2.0-(th2 + k21/2.0))*m2*(l*(pow(vth2,2)+pow(vth1,2)*cos(th1 + k11/2.0-(th2 + k21/2.0))));
				k12 /= den;
				k12 *= deltat;
				k22 = 2*sin((th1 + k11/2.0)-(th2 + k21/2.0))*(g*(m1+m2)*cos((th1 + k11/2.0))+l*(pow(vth2,2)*m2*cos((th1 + k11/2.0)-(th2 + k21/2.0))+pow(vth1,2)*(m1+m2)));
				k22 /= den;
				k22 *= deltat;

				den = l*(2*m1+m2-m2*cos(2*(th1 + k12/2.0 - (th2 + k22/2.0))));
				k13 = -g*(2*m1+m2)*sin(th1 + k12/2.0)-m2*g*sin(th1 + k12/2.0-2*(th2 + k22/2.0))-2*sin(th1 + k12/2.0-(th2 + k22/2.0))*m2*(l*(pow(vth2,2)+pow(vth1,2)*cos(th1 + k12/2.0-(th2 + k22/2.0))));
				k13 /= den;
				k13 *= deltat;
				k23 = 2*sin((th1 + k12/2.0)-(th2 + k22/2.0))*(g*(m1+m2)*cos((th1 + k12/2.0))+l*(pow(vth2,2)*m2*cos((th1 + k12/2.0)-(th2 + k22/2.0))+pow(vth1,2)*(m1+m2)));
				k23 /= den;
				k23 *= deltat;

				den = l*(2*m1+m2-m2*cos(2*(th1 + k13/2.0 - (th2 + k23/2.0))));
				k14 = -g*(2*m1+m2)*sin(th1 + k13/2.0)-m2*g*sin(th1 + k13/2.0-2*(th2 + k23/2.0))-2*sin(th1 + k13/2.0-(th2 + k23/2.0))*m2*(l*(pow(vth2,2)+pow(vth1,2)*cos(th1 + k13/2.0-(th2 + k23/2.0))));
				k14 /= den;
				k14 *= deltat;
				k24 = 2*sin((th1 + k13/2.0)-(th2 + k23/2.0))*(g*(m1+m2)*cos((th1 + k13/2.0))+l*(pow(vth2,2)*m2*cos((th1 + k13/2.0)-(th2 + k23/2.0))+pow(vth1,2)*(m1+m2)));
				k24 /= den;
				k24 *= deltat;

				vth1 += (k11/6) + (k12/3) + (k13/3) + (k14/6)
				vth2 += (k21/6) + (k22/3) + (k23/3) + (k24/6)
				th1 += deltat*vth1;
				th2 += deltat*vth2;
				
			th1Array.append(th1)
			vth1Array.append(vth1)
			th2Array.append(th2)
			vth2Array.append(vth2)
			
			i += 1

# Ventana WX que se encarga de mostrar progreso.
class MainThread(Thread): 
   def __init__(self): 
      Thread.__init__(self) 

   def run(self):
	  makeCalc()

class DiagProgress ( wx.Dialog ):
	
	initCalc = False
	fps = 0
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Cargando grafica..", pos = wx.DefaultPosition, size = wx.Size( 431,91 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		mainBoxxy = wx.BoxSizer( wx.VERTICAL )
		
		progressBoxxy = wx.BoxSizer( wx.VERTICAL )
		
		self.progressBar = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		progressBoxxy.Add( self.progressBar, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		mainBoxxy.Add( progressBoxxy, 2, wx.EXPAND, 5 )
		
		textBoxxy = wx.BoxSizer( wx.VERTICAL )
		
		self.textProgress = wx.StaticText( self, wx.ID_ANY, u"Graficando: 0 %", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.textProgress.Wrap( -1 )
		textBoxxy.Add( self.textProgress, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		mainBoxxy.Add( textBoxxy, 1, wx.EXPAND, 5 )
		
		self.SetSizer( mainBoxxy )
		self.Layout()
		
		self.Centre( wx.BOTH )
		self.Bind( wx.EVT_UPDATE_UI, self.MakeCalc )
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		
	def OnCloseWindow(self, evt):
		self.Destroy()
		
	def MakeCalc( self, event ):
		if self.initCalc == False:
			t = MainThread() 
			t.start()
			self.initCalc = True
		else:
			if(self.fps % 5 == 0):
				prog = int((i/maxIter)*100)
				self.progressBar.SetValue(prog)
				self.textProgress.SetLabel(u"Graficando: {0} %".format(prog))
		self.fps += 1
		
		if(i == maxIter):
			self.Close()

# Abre ventana WX
ex = wx.App()
frame = DiagProgress(None)
frame.Show(True)
ex.MainLoop()
			
# Crea gráfica
pylab.plot(th1Array,vth1Array, 'r')
pylab.plot(th2Array,vth2Array, 'b')
pylab.xlabel('$\\theta$');
pylab.ylabel('$v$');
pylab.title(u'Espacio fase');
pylab.grid(True);
pylab.axis('auto');
pylab.show();

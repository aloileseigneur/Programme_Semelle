# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import serial
from random import randint


# Create object serial port
ser = serial.Serial(port = "/dev/ttyUSB0",baudrate=230400,timeout=1) # configuration du port série

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################
pg.setConfigOption('background','w')
pg.setConfigOption('foreground', 'k')

win = pg.GraphicsWindow(title="Signal from serial port", size = (1920,1080)) # creates a window





## droite
p = win.addPlot(title="Semelles Gauche")  # creates empty space for the plot in the window
p.setYRange(0,1000)
p.setLabel(axis='left', text='Pression(Pa)')
p.setLabel(axis='bottom', text='Temps')
color_blue = QtGui.QColor(0, 0, 255)
color_aqua = QtGui.QColor(0, 255, 255)
color_red = QtGui.QColor(255, 0, 0)
color_black = QtGui.QColor(0, 0, 0)
color_green = QtGui.QColor(0, 255, 0)
pen_blue = pg.mkPen(color_blue, width=3)
pen_red = pg.mkPen(color_red, width=3)
pen_aqua = pg.mkPen(color_aqua, width=3)
pen_black = pg.mkPen(color_black, width=3)
pen_green = pg.mkPen(color_green, width=3)
curveTi = p.plot(pen = pen_blue)                        # create an empty "plot" (a curve to plot)
curveTe = p.plot(pen = pen_red)
curveMi = p.plot(pen = pen_aqua)                        # create an empty "plot" (a curve to plot)
curveMe = p.plot(pen = pen_black)
curveDt = p.plot(pen = pen_green)                       # create an empty "plot" (a curve to plot)
##gauche

p1 = win.addPlot(title="Semelles Droite")
p1.setYRange(0,1000)
p1.setLabel(axis='left', text='Pression(Pa)')
p1.setLabel(axis='bottom', text='Temps')
color_blue1 = QtGui.QColor(0, 0, 255)
color_aqua1 = QtGui.QColor(0, 255, 255)
color_red1 = QtGui.QColor(255, 0, 0)
color_black1 = QtGui.QColor(0, 0, 0)
color_green1 = QtGui.QColor(0, 255, 0)
pen_blue1 = pg.mkPen(color_blue, width=3)
pen_red1 = pg.mkPen(color_red, width=3)
pen_aqua1 = pg.mkPen(color_aqua, width=3)
pen_black1 = pg.mkPen(color_black, width=3)
pen_green1 = pg.mkPen(color_green, width=3)
curveTiD = p1.plot(pen = pen_blue)                        # create an empty "plot" (a curve to plot)
curveTeD = p1.plot(pen = pen_red)
curveMiD = p1.plot(pen = pen_aqua)                        # create an empty "plot" (a curve to plot)
curveMeD = p1.plot(pen = pen_black)
curveDtD = p1.plot(pen = pen_green) 



windowWidth = 500                    # width of the window displaying the curve
Ti = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
Te = linspace(0,0,windowWidth)
Mi = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
Me = linspace(0,0,windowWidth)
Dt = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
Ti1 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
Te1 = linspace(0,0,windowWidth)
Mi1 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
Me1 = linspace(0,0,windowWidth)
Dt1 = linspace(0,0,windowWidth)
ptr = 0  
ptr1 = 0                    # set first x position

# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global curveTi, curveTe, curveMi, curveMe, curveDt, ptr,ptr1, Ti, Te, Mi, Me, Dt, curveTiD, curveTeD, curveMiD, curveMeD, curveDtD, Ti1, Te1, Mi1, Me1, Dt1  
    Ti[:-1] = Ti[1:]  
    Te[:-1] = Te[1:]
    Mi[:-1] = Mi[1:]
    Me[:-1] = Me[1:]
    Dt[:-1] = Dt[1:]
    Ti1[:-1] = Ti1[1:]  
    Te1[:-1] = Te1[1:]
    Mi1[:-1] = Mi1[1:]
    Me1[:-1] = Me1[1:]
    Dt1[:-1] = Dt1[1:]  
     
    receive = ser.read(22)  #reception de 22 bytes 
    receivehex = receive.hex() # conversion en héxadecimal
    liste = str(receivehex)

##gauche
    if liste[2:3]=='0':
        print(liste)
        int_talonig = int(liste[6:9], 16)  # shift data in the temporal mean 1 sample left
        print(liste[6:9])                  
        int_taloneg = int(liste[9:11], 16)# shift data in the temporal mean 1 sample left
        print(liste[9:11])
        int_millieuig = int(liste[11:14], 16) # shift data in the temporal mean 1 sample left
        print(liste[11:14])                   
        int_millieueg = int(liste[14:16], 16)# shift data in the temporal mean 1 sample left
        print(liste[14:16])
        int_doigtg = int(liste[16:18], 16) # shift data in the temporal mean 1 sample left
        print(liste[16:18])
        valueg = int_talonig               # read line (single value) from the serial port
        valueg1 = int_taloneg
        valueg2 = int_millieuig              # read line (single value) from the serial port
        valueg3 = int_millieueg
        valueg4 = int_doigtg 

        Ti[-1] = float(valueg)                 # vector containing the instantaneous values      
        Te[-1] = float(valueg1)
        Mi[-1] = float(valueg2)                 # vector containing the instantaneous values      
        Me[-1] = float(valueg3)
        Dt[-1] = float(valueg4)                 # vector containing the instantaneous values      
    
    ptr += 1                              # update x position for displaying the curve
    curveTi.setData(Ti)     
    curveTe.setData(Te)
    curveMi.setData(Mi)     
    curveMe.setData(Me)
    curveDt.setData(Dt)
                    # set the curve with this data
    curveTi.setPos(ptr,0)                   # set x position in the graph to 0
    curveTe.setPos(ptr,0)
    curveMi.setPos(ptr,0)                   # set x position in the graph to 0
    curveMe.setPos(ptr,0)
    curveDt.setPos(ptr,0) 

##droit
    if liste[2:3]=='1':
        print(liste)
        int_taloni = int(liste[6:9], 16)  # shift data in the temporal mean 1 sample left
        print(liste[6:9])                  
        int_talone = int(liste[9:11], 16)# shift data in the temporal mean 1 sample left
        print(liste[9:11])
        int_millieui = int(liste[11:14], 16) # shift data in the temporal mean 1 sample left
        print(liste[11:14])                   
        int_millieue = int(liste[14:16], 16)# shift data in the temporal mean 1 sample left
        print(liste[14:16])
        int_doigt = int(liste[16:18], 16) # shift data in the temporal mean 1 sample left
        print(liste[16:18])
        value = int_taloni               # read line (single value) from the serial port
        value1 = int_talone
        value2 = int_millieui               # read line (single value) from the serial port
        value3 = int_millieue
        value4 = int_doigt              # read line (single value) from the serial port
        
        Ti1[-1] = float(value)                 # vector containing the instantaneous values      
        Te1[-1] = float(value1)
        Mi1[-1] = float(value2)                 # vector containing the instantaneous values      
        Me1[-1] = float(value3)
        Dt1[-1] = float(value4)                 # vector containing the instantaneous values      
        
    ptr1 += 1                              # update x position for displaying the curve
    curveTiD.setData(Ti1)     
    curveTeD.setData(Te1)
    curveMiD.setData(Mi1)     
    curveMeD.setData(Me1)
    curveDtD.setData(Dt1)       # set the curve with this data
                    
    curveTiD.setPos(ptr1,0)                   # set x position in the graph to 0
    curveTeD.setPos(ptr1,0)
    curveMiD.setPos(ptr1,0)                   # set x position in the graph to 0
    curveMeD.setPos(ptr1,0)
    curveDtD.setPos(ptr1,0)                   # set x position in the graph to 0               
    QtGui.QApplication.processEvents()    # you MUST process the plot now

### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
while True: 
    update()
### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
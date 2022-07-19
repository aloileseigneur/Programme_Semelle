
from random import randint
from pyqtgraph.Qt import QtGui,  QtWidgets
import pyqtgraph as pg
import serial
from MainWindow import *
from numpy import linspace
from PyQt5.QtCore import QThread


ser = serial.Serial(port = "/dev/ttyUSB0",baudrate=230400,timeout=1) # configuration du port série

class Window(Ui_MainWindow):
    pg.setConfigOption('background','w')
    pg.setConfigOption('foreground', 'k')

     

    def __init__(self,window):
        super().__init__()
        self.setupUi(window)
        
        self.windowWidth = 500                    # width of the window displaying the curve
        self.Ti = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Te = linspace(0,0,self.windowWidth)
        self.Mi = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Me = linspace(0,0,self.windowWidth)
        self.Dt = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Ti1 = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Te1 = linspace(0,0,self.windowWidth)
        self.Mi1 = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Me1 = linspace(0,0,self.windowWidth)
        self.Dt1 = linspace(0,0,self.windowWidth)
        
        self.ptr = 0  
        self.ptr1 = 0
        
        self.p = self.graphicsView.addPlot(title="Semelles Gauche")
        self.p.setYRange(0,1000)
        self.p.setLabel(axis='left', text='Pression(Pa)')
        self.p.setLabel(axis='bottom', text='Temps')
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
        self.curveTi = self.p.plot(pen = pen_blue)                        # create an empty "plot" (a curve to plot)
        self.curveTe = self.p.plot(pen = pen_red)
        self.curveMi = self.p.plot(pen = pen_aqua)                        # create an empty "plot" (a curve to plot)
        self.curveMe = self.p.plot(pen = pen_black)
        self.curveDt = self.p.plot(pen = pen_green)

        self.p1 = self.graphicsView.addPlot(title="Semelles Droite")
        self.p1.setYRange(0,1000)
        self.p1.setLabel(axis='left', text='Pression(Pa)')
        self.p1.setLabel(axis='bottom', text='Temps')
        color_blue1 = QtGui.QColor(0, 0, 255)
        color_aqua1 = QtGui.QColor(0, 255, 255)
        color_red1 = QtGui.QColor(255, 0, 0)
        color_black1 = QtGui.QColor(0, 0, 0)
        color_green1 = QtGui.QColor(0, 255, 0)
        pen_blue1 = pg.mkPen(color_blue1, width=3)
        pen_red1 = pg.mkPen(color_red1, width=3)
        pen_aqua1 = pg.mkPen(color_aqua1, width=3)
        pen_black1 = pg.mkPen(color_black1, width=3)
        pen_green1 = pg.mkPen(color_green1, width=3)
        self.curveTiD = self.p1.plot(pen = pen_blue1)                        # create an empty "plot" (a curve to plot)
        self.curveTeD = self.p1.plot(pen = pen_red1)
        self.curveMiD = self.p1.plot(pen = pen_aqua1)                        # create an empty "plot" (a curve to plot)
        self.curveMeD = self.p1.plot(pen = pen_black1)
        self.curveDtD = self.p1.plot(pen = pen_green1)


        self.serial = Serial(self)
        self.serial.start()
        # self.update = Update(self)
        #self.update.start()

    def __del__(self):
        #self.update.terminate()
        self.serial.terminate()
        # self.update.wait()
        self.serial.wait()
    
        
class Serial(QThread):
    def __init__(self,parent):
        super(Serial,self).__init__()
        self._parent = parent

        self.windowWidth = 500                    # width of the window displaying the curve
        self.Ti = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Te = linspace(0,0,self.windowWidth)
        self.Mi = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Me = linspace(0,0,self.windowWidth)
        self.Dt = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Ti1 = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Te1 = linspace(0,0,self.windowWidth)
        self.Mi1 = linspace(0,0,self.windowWidth)          # create array that will contain the relevant time series     
        self.Me1 = linspace(0,0,self.windowWidth)
        self.Dt1 = linspace(0,0,self.windowWidth)
        
        self.ptr = 0  
        self.ptr1 = 0 

    def setgui(self, gui):
        self.gui = gui
       

    def run(self):
        while True:

            # ################test valeurs###################
            # int_taloni = randint(0,100)            
            # int_talone = randint(0,100)
            # int_millieui = randint(0,100)             
            # int_millieue = randint(0,100)
            # int_doigt = randint(0,100) 


            # value = int_taloni              
            # value1 = int_talone
            # value2 = int_millieui               
            # value3 = int_millieue
            # value4 = int_doigt
            # ###############################################
            self.Ti[:-1] = self.Ti[1:]  
            self.Te[:-1] = self.Te[1:]
            self.Mi[:-1] = self.Mi[1:]
            self.Me[:-1] = self.Me[1:]
            self.Dt[:-1] = self.Dt[1:]
            self.Ti1[:-1] = self.Ti1[1:]  
            self.Te1[:-1] = self.Te1[1:]
            self.Mi1[:-1] = self.Mi1[1:]
            self.Me1[:-1] = self.Me1[1:]
            self.Dt1[:-1] = self.Dt1[1:]  
            
            receive = ser.read(22)  #reception de 22 bytes 
            receivehex = receive.hex() # conversion en héxadecimal
            liste = str(receivehex)
            print(liste)
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
                


               
                
                self.Ti1[-1] = float(value)                 # vector containing the instantaneous values      
                self.Te1[-1] = float(value1)
                self.Mi1[-1] = float(value2)                 # vector containing the instantaneous values      
                self.Me1[-1] = float(value3)
                self.Dt1[-1] = float(value4)  

            self.ptr1 += 1                              # update x position for displaying the curve
            self._parent.curveTiD.setData(self.Ti1)     
            self._parent.curveTeD.setData(self.Te1)
            self._parent.curveMiD.setData(self.Mi1)     
            self._parent.curveMeD.setData(self.Me1)
            self._parent.curveDtD.setData(self.Dt1)       
                            
            self._parent.curveTiD.setPos(self.ptr1,0)                   # set x position in the graph to 0
            self._parent.curveTeD.setPos(self.ptr1,0)
            self._parent.curveMiD.setPos(self.ptr1,0)                   # set x position in the graph to 0
            self._parent.curveMeD.setPos(self.ptr1,0)
            self._parent.curveDtD.setPos(self.ptr1,0)
                                # create an empty "plot" (a curve to plot)
            ##gauche

            

            

            # ###############test valeurs###################
            # int_taloni = randint(0,100)            
            # int_talone = randint(0,100)
            # int_millieui = randint(0,100)             
            # int_millieue = randint(0,100)
            # int_doigt = randint(0,100) 


            # valueg = int_taloni              
            # valueg1 = int_talone
            # valueg2 = int_millieui               
            # valueg3 = int_millieue
            # valueg4 = int_doigt
            # ###############################################


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

                

                self.Ti[-1] = float(valueg)                 # vector containing the instantaneous values      
                self.Te[-1] = float(valueg1)
                self.Mi[-1] = float(valueg2)                 # vector containing the instantaneous values      
                self.Me[-1] = float(valueg3)
                self.Dt[-1] = float(valueg4)

            self.ptr += 1                              # update x position for displaying the curve
            self._parent.curveTi.setData(self.Ti)     
            self._parent.curveTe.setData(self.Te)
            self._parent.curveMi.setData(self.Mi)     
            self._parent.curveMe.setData(self.Me)
            self._parent.curveDt.setData(self.Dt)
                                                              # set the curve with this data
            self._parent.curveTi.setPos(self.ptr,0)                   # set x position in the graph to 0
            self._parent.curveTe.setPos(self.ptr,0)
            self._parent.curveMi.setPos(self.ptr,0)                   # set x position in the graph to 0
            self._parent.curveMe.setPos(self.ptr,0)
            self._parent.curveDt.setPos(self.ptr,0)




app = QtWidgets.QApplication([])
MainWindow = QtWidgets.QMainWindow()

ui = Window(MainWindow)
MainWindow.show()
app.exec()



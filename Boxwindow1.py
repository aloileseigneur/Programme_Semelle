from random import randint
from pyqtgraph.Qt import QtGui,  QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
import serial
from MainWindow import *
from secondwindow import *
from numpy import linspace
from PyQt5.QtCore import QThread

ser = serial.Serial(port = "/dev/ttyUSB0",baudrate=230400,timeout=1) # configuration du port série

class Window(Ui_MainWindow, Ui_Form):
    pg.setConfigOption('background','w')
    pg.setConfigOption('foreground', 'k')

     

    def __init__(self,window, secondwindow):
        super().__init__()
        self.setupUi(window)
        
        

        self.windowWidth = 600                  # width of the window displaying the curve
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
        self.p.setYRange(0, 1000, padding=0, update=True)
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

        self.p1 = self.graphicsView.addPlot(title="Semelles Gauche")
        self.p1.setYRange(0, 1000, padding=0, update=True)
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
        self.curveMiD = self.p1.plot(pen = pen_black1)                        # create an empty "plot" (a curve to plot)
        self.curveMeD = self.p1.plot(pen = pen_aqua1)
        self.curveDtD = self.p1.plot(pen = pen_green1)
        
        self.pushButton.clicked.connect(lambda:self.montrer())
        self.pushButton_2.clicked.connect(lambda:self.cacher())
        self.pushButton_4.clicked.connect(lambda:self.enregistrer())

        self.actionAvanc.triggered.connect(lambda:self.opensecond())
        

        self.vert_1.show()
        self.vert_2.show()
        self.vert_3.show()
        self.vert_4.show()
        self.vert_5.show()
        self.rouge_1.hide()
        self.rouge_2.hide()
        self.rouge_3.hide()
        self.rouge_4.hide()
        self.rouge_5.hide()
        

        

        self.serial = Serial(self)
        self.serial.start()

    def __del__(self):
        self.serial.terminate()
        self.serial.wait()

    def montrer(self):
        self.pushButton_3.hide()
            
    def cacher(self):
        self.pushButton_3.show()
    
    def opensecond(self):
            self.secondwindow = QtWidgets.QMainWindow()
            self.ui2 = Ui_Form()
            self.ui2.setupUi(self.secondwindow)
            self.secondwindow.show()
        
    def enregistrer(self):
        self.exporter = pg.exporters.ImageExporter() #Juste avant les exportateurs pg.QtGui.QApplication.processEvents()Appel!
        self.exporter.parameters()['width'] = 100 
        self.exporter.export("test.png ")
        print("exported")


class Serial(QThread,Ui_Form):
    def __init__(self,parent):
        super(Serial,self).__init__()
        self._parent = parent
        

        self.windowWidth = 600                    # width of the window displaying the curve
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
        self.cpt=0

    def setgui(self, gui):
        self.gui = gui
       

    def run(self):
        while True:

            
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

            # ################test valeurs###################
            # int_taloni = 500      
            # int_talone = 400
            # int_millieui = 300             
            # int_millieue = 200
            # int_doigt = 100

            # value = int_taloni              
            # value1 = int_talone
            # value2 = int_millieui               
            # value3 = int_millieue
            # value4 = int_doigt
            # ###############################################   
            
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
                value2 = int_millieui            # read line (single value) from the serial port
                value3 = int_millieue
                value4 = int_doigt              # read line (single value) from the serial port
                
         
                self.Ti1[-1] = float(value)                 # vector containing the instantaneous values      
                self.Te1[-1] = float(value1)
                self.Mi1[-1] = float(value2)                 # vector containing the instantaneous values      
                self.Me1[-1] = float(value3)
                self.Dt1[-1] = float(value4) 

                if int_doigt >= 200  :
                    self._parent.rouge_11.show()
                    self._parent.vert_11.hide()
                else:
                    self._parent.rouge_11.hide()
                    self._parent.vert_11.show()

                if int_millieui >= 200  :
                    self._parent.rouge_13.show()
                    self._parent.vert_13.hide()
                else:
                    self._parent.rouge_13.hide()
                    self._parent.vert_13.show()

                if int_millieue >= 200 :
                    self._parent.rouge_12.show()
                    self._parent.vert_12.hide()
                else:
                    self._parent.rouge_12.hide()
                    self._parent.vert_12.show()

                if int_taloni >= 200 :
                    self._parent.rouge_14.show()
                    self._parent.vert_14.hide()
                else:
                    self._parent.rouge_14.hide()
                    self._parent.vert_14.show()

                if int_talone >= 200 :
                    self._parent.rouge_15.show()
                    self._parent.vert_15.hide()
                else:
                    self._parent.rouge_15.hide()
                    self._parent.vert_15.show()

      

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
            # int_taloni = 100          
            # int_talone = 200
            # int_millieui = 300             
            # int_millieue = 400
            # int_doigt = 500


            # valueg = int_taloni              
            # valueg1 = int_talone
            # valueg2 = int_millieui               
            # valueg3 = int_millieue
            # valueg4 = int_doigt
            # ###############################################


            if liste[2:3]=='0':
                int_talonig = int(liste[6:9], 16)  # shift data in the temporal mean 1 sample left
                print(liste[6:9])                                     
                int_taloneg = int(liste[9:11], 16)# shift data in the temporal mean 1 sample left
                print(liste[9:11])
                int_millieuig = int(liste[14:16], 16) # shift data in the temporal mean 1 sample left
                print(liste[14:16])                   
                int_millieueg = int(liste[11:14], 16)# shift data in the temporal mean 1 sample left
                print(liste[11:14])
                int_doigtg = int(liste[16:18], 16) # shift data in the temporal mean 1 sample left
                print(liste[16:18])
                valueg = int_talonig               # read line (single value) from the serial port
                valueg1 = int_taloneg
                valueg2 = int_millieuig            # read line (single value) from the serial port
                valueg3 = int_millieueg
                valueg4 = int_doigtg 

                self.Ti[-1] = float(valueg)                 # vector containing the instantaneous values      
                self.Te[-1] = float(valueg1)
                self.Mi[-1] = float(valueg2)                 # vector containing the instantaneous values      
                self.Me[-1] = float(valueg3)
                self.Dt[-1] = float(valueg4)

                if int_doigtg >= 200  :
                    self._parent.rouge_1.show()
                    self._parent.vert_1.hide()
                else:
                    self._parent.rouge_1.hide()
                    self._parent.vert_1.show()

                if int_millieuig >= 200  :
                    self._parent.rouge_2.show()
                    self._parent.vert_2.hide()
                else:
                    self._parent.rouge_2.hide()
                    self._parent.vert_2.show()

                if int_millieueg >= 200 :
                    self._parent.rouge_3.show()
                    self._parent.vert_3.hide()
                else:
                    self._parent.rouge_3.hide()
                    self._parent.vert_3.show()

                if int_talonig >= 200 :
                    self._parent.rouge_4.show()
                    self._parent.vert_4.hide()
                else:
                    self._parent.rouge_4.hide()
                    self._parent.vert_4.show()

                if int_taloneg >= 200 :
                    self._parent.rouge_5.show()
                    self._parent.vert_5.hide()
                else:
                    self._parent.rouge_5.hide()
                    self._parent.vert_5.show()

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
secondwindow = QtWidgets.QWidget()

ui = Window(MainWindow, secondwindow)
MainWindow.show()
app.exec()



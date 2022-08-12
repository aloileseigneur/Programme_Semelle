from random import randint
from pyqtgraph.Qt import QtGui,  QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
import serial
from SoleWindow import *
from secondwindow import *
from numpy import linspace
from PyQt5.QtCore import QThread
import csv
import time
import threading
import faulthandler; faulthandler.enable()

############# sudo chmod a+rw /dev/ttyUSB0 ################### pour ouvrir le port
############# pyuic5 -x application.ui -o application.py ########## pour convertir
############ pyrcc5 test.qrc -o test_rc.py ################ 



# ser = serial.Serial(port = "/dev/ttyUSB0",baudrate=230400,timeout=1) # configuration du port série

class Window(Ui_MainWindow):
    pg.setConfigOption('background','w')
    pg.setConfigOption('foreground', 'k')

     

    def __init__(self,window):
        super().__init__()
        self.setupUi(window)
      
        
        self.pushButton_4.clicked.connect(lambda:self.enregistrer())
        self.actionWii.triggered.connect(lambda:self.secondwindow())

        self.green_1.show()
        self.green_2.show()
        self.green_3.show()
        self.green_4.show()
        self.green_5.show()
        self.red_1.hide()
        self.red_2.hide()
        self.red_3.hide()
        self.red_4.hide()
        self.red_5.hide()
        

    
        self.serial = Serial(self)
        self.serial.start(priority = 1)

    def __del__(self):
        self.serial.terminate()
        self.serial.wait()

    def secondwindow(self):
        
        self.window = QtWidgets.QWidget()
        self.ui = Ui_wiiwindow()
        self.ui.setupUi(self.window)
        self.window.show()

    
    # def enregistrer(self):
    #     self.exporter = pg.exporters.ImageExporter() #Juste avant les exportateurs pg.QtGui.QApplication.processEvents()Appel!
    #     self.exporter.parameters()['width'] = 100 
    #     self.exporter.export("test.png ")
    #     print("exported")


class Serial(QThread):
     
    def __init__(self,parent):
        super(Serial,self).__init__()
        self._parent = parent
        

        self.windowWidth = 300                   # width of the window displaying the curve
        self.Ti = linspace(0,0,self.windowWidth,endpoint=False)          # create array that will contain the relevant time series     
        self.Te = linspace(0,0,self.windowWidth,endpoint=False)
        self.Mi = linspace(0,0,self.windowWidth,endpoint=False)          # create array that will contain the relevant time series     
        self.Me = linspace(0,0,self.windowWidth,endpoint=False)
        self.Dt = linspace(0,0,self.windowWidth,endpoint=False)          # create array that will contain the relevant time series     
        self.Ti1 = linspace(0,0,self.windowWidth,endpoint=False)          # create array that will contain the relevant time series     
        self.Te1 = linspace(0,0,self.windowWidth,endpoint=False)
        self.Mi1 = linspace(0,0,self.windowWidth,endpoint=False)          # create array that will contain the relevant time series     
        self.Me1 = linspace(0,0,self.windowWidth,endpoint=False)
        self.Dt1 = linspace(0,0,self.windowWidth,endpoint=False)

        self.ptr= 0
        self.ptr1= 0

        self.p = self._parent.graphicsView.addPlot(title="Semelles Gauche")
        self.p.setYRange(0, 500, padding=0, update=True)
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

        self.p1 = self._parent.graphicsView_2.addPlot(title="Semelles Droite")
        self.p1.setYRange(0, 500, padding=0, update=True)
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
        self.curveMiD = self.p1.plot(pen = pen_aqua1)
        self.curveMeD = self.p1.plot(pen = pen_black1)                        # create an empty "plot" (a curve to plot)
        self.curveDtD = self.p1.plot(pen = pen_green1)

       


    def setgui(self, gui):
        self.gui = gui
    
    def rightsole(self,F1, F2, F3, F4, F5):

        Mx = (F1*3 + F2*2 + F3*3,5 + F4*1,2 + F5*1,6)
        My = (F1*10 + F2*3,2 + F3*4,2 + F4*8,5 + F5*9,2)

        Fz = F1 + F2 + F3 + F4 + F5

        Coorx = Mx / Fz
        Coory = My / Fz

    def leftsole(self,F1, F2, F3, F4, F5):

        Mx = (F1*2,7 + F2*2,2 + F3*3,4 + F4*1,1 + F5*1,1)
        My = (F1*9,5 + F2*3,2 + F3*4,6 + F4*8,3 + F5*8,8)

        Fz = F1 + F2 + F3 + F4 + F5

        Coorx = Mx / Fz
        Coory = My / Fz






    def rightcsvfile(self, list, time, int_Rheel_inter, int_Rheel_ext, int_Rmiddle_inter, int_Rmiddle_ext,int_Rfinger):

            fielnames = ['temps', 'int_Rheel_inter','int_Rheel_ext','int_Rmiddle_inter','int_Rmiddle_ext','int_Rfinger']
            dictionnary=dict(zip(fielnames,[time, int_Rheel_inter,int_Rheel_ext,int_Rmiddle_inter,int_Rmiddle_ext,int_Rfinger]))
            list.append(dictionnary)
            print(list)
            with open ('semelleD.csv', 'w', newline='') as f:
                
                thewriter= csv.DictWriter(f, fieldnames = fielnames)
                count = 0
                thewriter.writeheader()
                for elmt in list:
                    count+=1
                    thewriter.writerow(elmt)
                
                print (count)
                
            
            

    def leftcsvfile(self, list2, time2, int_Lheel_inter, int_Lheel_ext, int_Lmiddle_inter,int_Lmiddle_ext, int_Lfinger ):
        
        
        fielnames2 = ['time2', 'int_Lheel_inter','int_Lheel_ext','int_Lmiddle_inter','int_Lmiddle_ext','int_Lfinger']
        dictionnary2=dict(zip(fielnames2,[time2, int_Lheel_inter,int_Lheel_ext,int_Lmiddle_inter,int_Lmiddle_ext,int_Lfinger]))
        list2.append(dictionnary2)
        print(list2)
        with open ('semelleG.csv', 'w', newline='') as f:
            
            thewriter= csv.DictWriter(f, fieldnames = fielnames2)
            count2 = 0
            thewriter.writeheader()
            for elmt in list2:
                count2+=1
                thewriter.writerow(elmt)
            
            print (count2)
             

    def run(self):
        Pamax = 200


        firsttimeR = True
        firsttimeL = True

        list = []
        list2 = []
        time1 = 0
        time2 = 0


        while True:
            

            self.ptr1 += 1 
            self.ptr += 1 
            self.curveTiD.setData(self.Ti1)     
            self.curveTeD.setData(self.Te1)
            self.curveMiD.setData(self.Mi1)     
            self.curveMeD.setData(self.Me1)
            self.curveDtD.setData(self.Dt1)   
            self.curveTi.setData(self.Ti)     
            self.curveTe.setData(self.Te)           # set the curve with this data
            self.curveMi.setData(self.Mi)     
            self.curveMe.setData(self.Me)
            self.curveDt.setData(self.Dt)


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
                int_Rheel_inter = int(liste[6:9], 16)  # shift data in the temporal mean 1 sample left
                if firsttimeR:
                    varRheel_inter = int_Rheel_inter
                int_Rheel_inter = int_Rheel_inter - varRheel_inter
                r_heel_inter = str(int_Rheel_inter)
                self._parent.lineEdit_8.setText(r_heel_inter)
                print(liste[6:9])                  
                int_Rheel_ext = int(liste[9:11], 16)  # shift data in the temporal mean 1 sample left                
                if firsttimeR:
                    varRheel_ext = int_Rheel_ext
                int_Rheel_ext = int_Rheel_ext - varRheel_ext
                # int_Rheel_ext = int_Rheel_ext + max_Rheel_ext

                # if int_Rheel_ext >= 254 and max_Rheel_ext == 0:
                #     max_Rheel_ext = 254

                # if int_Rheel_ext ==255 and max_Rheel_ext ==254:
                #     max_Rheel_ext = 0

                r_heel_ext = str(int_Rheel_ext)
                self._parent.lineEdit_10.setText(r_heel_ext)
                print(liste[9:11])
                int_Rmiddle_ext = int(liste[11:14], 16)  # shift data in the temporal mean 1 sample left
                if firsttimeR:
                    varRmiddle_ext = int_Rmiddle_ext
                    
                int_Rmiddle_ext = int_Rmiddle_ext - varRmiddle_ext

                r_middle_ext = str(int_Rmiddle_ext)
                self._parent.lineEdit_9.setText(r_middle_ext)
                print(liste[11:14])                   
                int_Rmiddle_inter = int(liste[14:16], 16) # shift data in the temporal mean 1 sample left
                if firsttimeR:
                    varRmiddle_inter = int_Rmiddle_inter
                    
                int_Rmiddle_inter = int_Rmiddle_inter - varRmiddle_inter
                
                r_middle_inter = str(int_Rmiddle_inter)
                self._parent.lineEdit_7.setText(r_middle_inter)
                print(liste[14:16])
                int_Rfinger = int(liste[16:18], 16)  # shift data in the temporal mean 1 sample left
                if firsttimeR:
                    varRfinger = int_Rfinger
                    firsttimeR = False
                int_Rfinger = int_Rfinger - varRfinger
                
                r_finger = str(int_Rfinger)
                self._parent.lineEdit_6.setText(r_finger)
                print(liste[16:18])

                value = int_Rheel_inter               # read line (single value) from the serial port
                value1 = int_Rheel_ext
                value2 = int_Rmiddle_inter           # read line (single value) from the serial port
                value3 = int_Rmiddle_ext
                value4 = int_Rfinger             # read line (single value) from the serial port
                
         
                self.Ti1[-1] = float(value)                 # vector containing the instantaneous values      
                self.Te1[-1] = float(value1)
                self.Mi1[-1] = float(value2)                 # vector containing the instantaneous values      
                self.Me1[-1] = float(value3)
                self.Dt1[-1] = float(value4) 
                
                if int_Rfinger >= Pamax  :
                    self._parent.red_11.show()
                    self._parent.green_11.hide()
                else:
                    self._parent.red_11.hide()
                    self._parent.green_11.show()

                if int_Rmiddle_ext >= Pamax  :
                    self._parent.red_13.show()
                    self._parent.green_13.hide()
                else:
                    self._parent.red_13.hide()
                    self._parent.green_13.show()

                if int_Rmiddle_inter >= Pamax :
                    self._parent.red_12.show()
                    self._parent.green_12.hide()
                else:
                    self._parent.red_12.hide()
                    self._parent.green_12.show()

                if int_Rheel_inter >= Pamax :
                    self._parent.red_14.show()
                    self._parent.green_14.hide()
                else:
                    self._parent.red_14.hide()
                    self._parent.green_14.show()

                if int_Rheel_ext >= Pamax :
                    self._parent.red_15.show()
                    self._parent.green_15.hide()
                else:
                    self._parent.red_15.hide()
                    self._parent.green_15.show()

                #############point central##################
                # self.f11 = int_Rfinger
                # self.f12 = int_Rmiddle_ext
                # self.f13 = int_Rmiddle_inter
                # self.f14 = int_Rheel_ext
                # self.f15 = int_Rheel_inter
                
                # self.mx_R = self.f11*-0.03*20 + self.f12*0.02*100 + self.f13*-0.035*100 + self.f14*0.012*100 + self.f15*-0.016*100
                # self.my_R = self.f11*-0.10*20 + self.f12*-0.032*100 + self.f13*-0.042*100 + self.f14*0.085*100 + self.f15*0.092*100

                # self.fz_R = (self.f11 + self.f12 + self.f13 + self.f14 + self.f15)
                # print(self.fz_R)
                # if self.fz_R != 0:
                #     self.cox_R = self.mx_R / self.fz_R
                #     self.coy_R = self.my_R / self.fz_R
                # else:
                #     self.cox_R = 0
                #     self.coy_R = 0
                

                # self.defx_R=1740
                # self.defy_R=346
                
                # self.coorfinalx_R = self.defx_R + int(self.cox_R)
                # self.coorfinaly_R = self.defy_R + int(self.coy_R)
                # print('R', self.coorfinalx_R)
                # print('R', self.coorfinaly_R)
                # self._parent.right_cross.move(self.coorfinalx_R, self.coorfinaly_R)

                ###################csvfile#######################
                # temps_ref = time.time()
                # t1 = threading.Thread(target = self.rightcsvfile(list, time1, int_Rheel_inter, int_Rheel_ext, int_Rmiddle_inter, int_Rmiddle_ext, int_Rfinger), args = ())
                # t1.start()
                # t1.join()
                
                # temp = time.time() - temps_ref

                # time1 = time1 + temp
                # print(time1)

                                                           
                                    
         





            if liste[2:3]=='0':
                int_Lheel_inter = int(liste[6:9], 16)  # shift data in the temporal mean 1 sample left
                if firsttimeL:
                    varLheel_inter = int_Lheel_inter
                    
                int_Lheel_inter = int_Lheel_inter - varLheel_inter
                l_heel_int = str(int_Lheel_inter)
                self._parent.lineEdit_5.setText(l_heel_int)
                print(liste[6:9])                                     
                int_Lheel_ext = int(liste[9:11], 16)# shift data in the temporal mean 1 sample left
                if firsttimeL:
                    varLheel_ext = int_Lheel_ext
                    
                int_Lheel_ext = int_Lheel_ext - varLheel_ext
                l_heel_ext = str(int_Lheel_ext)
                self._parent.lineEdit_2.setText(l_heel_ext)
                print(liste[9:11])
                int_Lmiddle_inter = int(liste[14:16], 16) # shift data in the temporal mean 1 sample left
                if firsttimeL:
                    varLmiddle_inter = int_Lmiddle_inter
                    
                int_Lmiddle_inter = int_Lmiddle_inter - varLmiddle_inter

                l_middle_inter = str(int_Lmiddle_inter)
                self._parent.lineEdit_4.setText(l_middle_inter)
                print(liste[14:16])
                                   
                int_Lmiddle_ext = int(liste[11:14], 16)# shift data in the temporal mean 1 sample left
                if firsttimeL:
                    varLmiddle_ext = int_Lmiddle_ext
                    
                int_Lmiddle_ext = int_Lmiddle_ext - varLmiddle_ext

                # int_Lmiddle_ext = int_Lmiddle_ext + max_Lmiddle_ext
               
                # if int_Lmiddle_ext >= 254 and max_Lmiddle_ext == 0:
                #     max_Lmiddle_ext = 254
                #     print('bonjour')
                # if int_Lmiddle_ext <= 254 and max_Lmiddle_ext ==254:
                #     max_Lmiddle_ext = 0

                
                l_middle_ext = str(int_Lmiddle_ext)
                self._parent.lineEdit_1.setText(l_middle_ext)
                print(liste[11:14])

                int_Lfinger = int(liste[16:18], 16) # shift data in the temporal mean 1 sample left
                if firsttimeL:
                    varLfinger = int_Lfinger
                    firsttimeL = False
                int_Lfinger = int_Lfinger - varLfinger
                l_finger = str(int_Lfinger)
                self._parent.lineEdit_3.setText(l_finger)
                print(liste[16:18])

                valueg = int_Lheel_inter               # read line (single value) from the serial port
                valueg1 = int_Lheel_ext
                valueg2 = int_Lmiddle_inter            # read line (single value) from the serial port
                valueg3 = int_Lmiddle_ext
                valueg4 = int_Lfinger 

                self.Ti[-1] = float(valueg)                 # vector containing the instantaneous values      
                self.Te[-1] = float(valueg1)
                self.Mi[-1] = float(valueg2)                 # vector containing the instantaneous values      
                self.Me[-1] = float(valueg3)
                self.Dt[-1] = float(valueg4)

                if int_Lfinger >= Pamax  :
                    self._parent.red_1.show()
                    self._parent.green_1.hide()
                else:
                    self._parent.red_1.hide()
                    self._parent.green_1.show()

                if int_Lmiddle_inter >= Pamax  :
                    self._parent.red_2.show()
                    self._parent.green_2.hide()
                else:
                    self._parent.red_2.hide()
                    self._parent.green_2.show()

                if int_Lmiddle_ext >= Pamax :
                    self._parent.red_3.show()
                    self._parent.green_3.hide()
                else:
                    self._parent.red_3.hide()
                    self._parent.green_3.show()

                if int_Lheel_inter >= Pamax :
                    self._parent.red_4.show()
                    self._parent.green_4.hide()
                else:
                    self._parent.red_4.hide()
                    self._parent.green_4.show()

                if int_Lheel_ext >= Pamax :
                    self._parent.red_5.show()
                    self._parent.green_5.hide()
                else:
                    self._parent.red_5.hide()
                    self._parent.green_5.show()

                #############point central##################
                # self.f1 = int_Lfinger
                # self.f2 = int_Lmiddle_ext
                # self.f3 = int_Lmiddle_inter
                # self.f4 = int_Lheel_ext
                # self.f5 = int_Lheel_inter

                # self.mx_L = self.f1*0.27*2 + self.f2*-0.22*8 + self.f3*3.4*8 + self.f4*-1.1*8 + self.f5*1.1*8
                # self.my_L = self.f1*-9.5*2 + self.f2*-3.2*8 + self.f3*-4.6*8 + self.f4*8.3*8 + self.f5*8.8*8

                # self.fz_L = self.f1 + self.f2 + self.f3 + self.f4 + self.f5
                # print(self.fz_L)
                # self.cox_L = foo(self.mx_L , self.fz_L)
                # self.coy_L = foo(self.my_L , self.fz_L)
                
                # self.defx_L=1430
                # self.defy_L=346
                
                # self.coorfinalx_L = self.defx_L + int(self.cox_L)
                # self.coorfinaly_L = self.defy_L + int(self.coy_L)

                # print('L', self.coorfinalx_L)
                # print('L', self.coorfinaly_L)

                # self._parent.left_cross.move(self.coorfinalx_L, self. coorfinaly_L)

                #############csvfile##################
                # temps_ref2 = time.time()
                # t2 = threading.Thread(target = self.leftcsvfile(list2, time2, int_Lheel_inter, int_Lheel_inter, int_Lmiddle_inter,int_Lmiddle_ext, int_Lfinger ), args = ())
                # t2.start()
                # t2.join()         
                # temp2 = time.time() - temps_ref2
                # time2 = time2 + temp2

                



app = QtWidgets.QApplication([])
MainWindow = QtWidgets.QMainWindow()

ui = Window(MainWindow)
MainWindow.show()
app.exec()





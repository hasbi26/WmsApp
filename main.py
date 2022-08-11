from concurrent.futures import thread
from sqlite3 import connect
import sys,psutil,threading,time,urllib.request
import serial
import time # Optional (required if using time.sleep() below)
import requests


from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QGroupBox, QVBoxLayout, QGridLayout,QMainWindow, QLabel
from AnalogGaugeWidget import AnalogGaugeWidget
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtCore import *

class Window(QMainWindow) :

    def __init__(self) :
            super().__init__()

            
            # self.serialPort = '/dev/pts/2'
            self.serialPort = '/dev/ttyACM0'
            self.baudRate = 9600

            self.setWindowTitle("Water Monitor System")  
            height = 300
            width = 773
        # setting  the fixed width of window
            self.setFixedWidth(width)
            self.setFixedHeight(height)
        # creating a label widget
            self.label_1 = QLabel("Data Input : ", self)
            self.InternetStatus = QLabel("Internet Connected : ", self)
            self.ProsesorSuhu = QLabel("Proc. Temp : ", self)
            self.RamUsage = QLabel("Proc. Usage : ", self)
            self.Date = QLabel("Jam : ", self)
            self.LabelDate = QLabel("", self)
            
            self.LabelTempPros = QLabel("0.0", self)
            self.LabelProsUsage = QLabel("", self)

            self.led = QLabel(self)
            self.Internetled = QLabel(self)
            
            # self.tacoPh = QLabel("Sensor PH", self)
            self.tacoPh = AnalogGaugeWidget(self)
            self.tacoPh.resize(170,170)
            self.tacoPh.setMinimumHeight(200)
            self.tacoPh.units = "PH"
            self.tacoPh.setGaugeTheme(7)
            self.tacoPh.scalaCount = 9
            self.tacoPh.setMaxValue(9)
            self.tacoPh.updateValue(0)

            self.tacoSuhu = AnalogGaugeWidget(self)
            self.tacoSuhu.resize(170,170)
            self.tacoSuhu.setMinimumHeight(200)
            self.tacoSuhu.units = "C"
            self.tacoSuhu.setGaugeTheme(5)
            self.tacoSuhu.scalaCount = 9
            self.tacoSuhu.setMaxValue(100)
            self.tacoSuhu.updateValue(0)

            self.tacoTds = AnalogGaugeWidget(self)
            self.tacoTds.resize(170,170)
            self.tacoTds.setMinimumHeight(200)
            self.tacoTds.units = "PPM"
            self.tacoTds.setGaugeTheme(6)
            self.tacoTds.scalaCount = 9
            self.tacoTds.setMaxValue(1500)
            self.tacoTds.updateValue(0)

            # print("ph",self.tacoPh)
            # print("suhu",self.tacoSuhu)

            self.framePh = QLabel("", self)
            self.frameSuhu = QLabel("", self)
            self.frameTds = QLabel("", self)

            self.LabelstatusPh = QLabel("PH Air : ", self)
            self.DatastatusPh = QLabel("Netral ", self)

            self.LabelstatusSuhu = QLabel("Temp Air: ", self)
            self.DatastatusSuhu = QLabel("Normal ", self)

            self.LabelstatusTds = QLabel("Kerjenihan Air: ", self)
            self.DatastatusTds = QLabel("Jernih ", self)

        # moving position
            self.label_1.move(8, 6)
            self.InternetStatus.move(140, 6)
            self.ProsesorSuhu.move(335, 6)
            self.RamUsage.move(468, 6)
            self.Date.move(615, 6)
            self.LabelDate.move(660, 6)
            
            self.LabelTempPros.move(425, 12)
            self.LabelProsUsage.move(563, 12)
            
            self.led.move(105, 17)
            self.Internetled.move(305, 17)

            self.LabelstatusPh.move(8, 250)
            self.DatastatusPh.move(90, 250)

            self.LabelstatusSuhu.move(260, 250)
            self.DatastatusSuhu.move(350, 250)

            self.LabelstatusTds.move(513, 250)
            self.DatastatusTds.move(625, 250)

            self.tacoPh.move(40, 50)
            self.tacoSuhu.move(300, 50)
            self.tacoTds.move(560, 50)

            self.framePh.move(8, 49)
            self.frameSuhu.move(260, 49)
            self.frameTds.move(513, 49)
        # setting up the border
            self.label_1.setStyleSheet("border :1px solid black;")
            self.InternetStatus.setStyleSheet("border :1px solid black;")
            self.ProsesorSuhu.setStyleSheet("border :1px solid black;")
            self.RamUsage.setStyleSheet("border :1px solid black;")
            self.Date.setStyleSheet("border :1px solid black;")
            
            self.led.setStyleSheet("border :1px solid black; border-radius:10px; background-color: #f00505;")
            self.Internetled.setStyleSheet("border :1px solid black; border-radius:10px; background-color: #f00505;")
            
            self.LabelstatusPh.setStyleSheet("border :1px solid black;")
            self.DatastatusPh.setStyleSheet("font-weight: bold; color: green")

            self.LabelstatusSuhu.setStyleSheet("border :1px solid black;")
            self.DatastatusSuhu.setStyleSheet("font-weight: bold; color: green")

            self.LabelstatusTds.setStyleSheet("border :1px solid black;")
            self.DatastatusTds.setStyleSheet("font-weight: bold; color: green")

            # self.tacoPh.setStyleSheet("border :1px solid black;")
            self.framePh.setStyleSheet("border :1px solid black;")
            self.frameSuhu.setStyleSheet("border :1px solid black;")
            self.frameTds.setStyleSheet("border :1px solid black;")


        # resizing label
            self.label_1.resize(130, 40)
            self.InternetStatus.resize(190, 40)
            self.ProsesorSuhu.resize(130, 40)
            self.RamUsage.resize(145, 40)
            self.Date.resize(147, 40)
            self.LabelDate.resize(150, 40)
            # self.LabelTempPros
            self.led.resize(20, 20)
            self.Internetled.resize(20, 20)
            
            self.LabelstatusPh.resize(250, 40)
            self.DatastatusPh.resize(250, 40)

            self.LabelstatusSuhu.resize(250, 40)
            self.DatastatusSuhu.resize(250, 40)

            self.LabelstatusTds.resize(250, 40)
            self.DatastatusTds.resize(250, 40)

            # self.tacoPh.resize(250, 150)
            self.frameSuhu.resize(250, 195)
            self.frameTds.resize(250, 195)
            self.framePh.resize(250, 195)

  
            self.show()

            # print(self.get_cpu_temp())

    def timer1(self):
         trid1 = threading.Thread(target=window.thread1())
         trid1.start()

    def thread1(self):
        current_time = QTime.currentTime()
        text1 = current_time.toString()
        self.LabelDate.setText(text1)

    def timer2(Self):
        trid2 = threading.Thread(target=window.thread2())
        trid2.start()

    def thread2(self):
        t = psutil.sensors_temperatures()
        z = psutil.cpu_percent(interval=1, percpu=False)
        self.LabelProsUsage.setText(str(z))
        for x in ['amdgpu', 'amdgpu', 'scpi_sensors']:
            if x in t:
                self.LabelTempPros.setText(str(t[x][0].current))


    def Inet(Self):
        trid3 = threading.Thread(target=window.thread3())
        trid3.start()

    def thread3(self):
        if self.InternetCheck()== True :
            # print("on")
            self.Internetled.setStyleSheet("border :1px solid black; border-radius:10px; background-color: #08c93c;")

        else :
            self.Internetled.setStyleSheet("border :1px solid black; border-radius:10px; background-color: #f00505;")
            # print("off")


    def srl(Self):
        trid4 = threading.Thread(target=window.thread4())
        trid4.start()

    def thread4(self) :
        if self.CheckSerial()== True :
            # print("connect")
            self.led.setStyleSheet("border :1px solid black; border-radius:10px; background-color: #08c93c;")
            try:
                with serial.Serial(self.serialPort, self.baudRate) as ser: 
                    rawvalue = ser.read_until(b'\r') 
                    value = rawvalue.decode('ascii')
                    print("value =",value)
                    lenghtValue = value.split(",")
                    if len(lenghtValue) == 3 :
                        ph = lenghtValue[0]
                        tds = lenghtValue[1]
                        temp = lenghtValue[2]

                        self.tacoTds.updateValue(float(tds))
                        self.tacoPh.updateValue(float(ph))
                        self.tacoSuhu.updateValue(float(temp))

                        

                        if float(ph) < 6 : 
                            # prfloat("")
                            self.DatastatusPh.setText("Asam") #= QLabel("Netral ", self)
                        elif float(ph) > 7 :
                            self.DatastatusPh.setText("Basa") #= QLabel("Netral ", self)
                        else :
                            self.DatastatusPh.setText("Netral") #= QLabel("Netral ", self)

                        if float(tds) <= 150 : 
                            # prfloat("")
                            self.DatastatusTds.setText("Jernih") #= QLabel("Netral ", self)
                        elif float(tds) >= 1000 :
                            self.DatastatusTds.setText("Sangat Keruh") #= QLabel("Netral ", self)
                        else :
                            self.DatastatusTds.setText("Keruh") #= QLabel("Netral ", self)

                        if float(temp) <= 20 : 
                            # prfloat("")
                            self.DatastatusSuhu.setText("Dingin") #= QLabel("Netral ", self)
                        elif float(temp) >= 30 :
                            self.DatastatusSuhu.setText("Panas") #= QLabel("Netral ", self)
                        else :
                            self.DatastatusSuhu.setText("Suhu Normal") #= QLabel("Netral ", self)

                        
                        if self.InternetCheck()== True :
                            #print("internet aktif")

                            print("ph=", ph, "ppm=", tds, "temperature=", temp)

                            ppmurl = 'https://wmsapp.pythonanywhere.com/wmsapp/'
                            myobj = {'value': tds }
                            x = requests.post(ppmurl, data = myobj)
                            
                            Turl = 'http://wmsapp.pythonanywhere.com/temperature/'
                            Tmyobj = {'Tvalue': temp}
                            Tx = requests.post(Turl, data = Tmyobj)

                            Purl = 'http://wmsapp.pythonanywhere.com/ph/'
                            Pmyobj = {'Pvalue': ph}
                            Px = requests.post(Purl, data = Pmyobj)

                            print(Tx.text)

                            print(Px.text)

                            print(x.text)




            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                print('oops')    

                    # print("tds = ",tds, "ph =", ph, "temp = ", temp)

        else :
            print("not")
            self.led.setStyleSheet("border :1px solid black; border-radius:10px; background-color: #f00505;")



    def showtime(self):
        print("s")        

        # ser = serial.Serial(port='/dev/pts/2', baudrate=9600)

        # while (True):

        #         if (ser.inWaiting() > 0):
        #              # read the bytes and convert from binary array to ASCII
        #             data_str = ser.read(ser.inWaiting()).decode('ascii') 
        #             # print the incoming string without putting a new-line
        #             # ('\n') automatically after every print()
        #             print(data_str, end='') 

        #         time.sleep(0.01) 
    def InternetCheck(self):
        try:
            urllib.request.urlopen('http://google.com') #Python 3.x
            return True
        except:
            return False
    def CheckSerial(self) :
        try :
            ser = serial.Serial(port=self.serialPort, baudrate=self.baudRate)
            # self.ser
            return True
        except :
            return False


if __name__ == "__main__" :
    App = QApplication(sys.argv)
    # GaugeTDS = AnalogGaugeWidget()
    # GaugeSuhu = AnalogGaugeWidget()
    window = Window()
    # GaugePh = AnalogGaugeWidget(window)

    # timer = QTimer(window)
    # timer.timeout.connect(window.showtime)
    # timer.start()



    tmr1 = QTimer(window)
    tmr1.timeout.connect(window.timer1)
    tmr1.start(1000)


    tmr2 = QTimer(window)
    tmr2.timeout.connect(window.timer2)
    tmr2.start(1200)


    tmr3 = QTimer(window)
    tmr3.timeout.connect(window.Inet)
    tmr3.start(1100)

    tmr4 = QTimer(window)
    tmr4.timeout.connect(window.srl)
    tmr4.start(2000)

    sys.exit(App.exec())
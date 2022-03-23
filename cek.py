import serial
from datetime import datetime
from datetime import date
import time
import requests


ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

while (True):

    if (ser.inWaiting() > 0):
    
        now = datetime.now()
        today = date.today()
        temperature = 0
        ppm = 0
        hari = today.strftime("%B %d, %Y")

        current_time = now.strftime("%H:%M:%S")
        data_str = ser.read(ser.inWaiting()).decode('ascii') 

        # print(data_str)

        raw = data_str.split(",", 1)
        temperature = raw[0]
        ppm = raw[1]

        print(temperature, ppm)
     
        url = 'https://wmsapp.pythonanywhere.com/wmsapp/'
        myobj = {
          'value': ppm
                    }
        x = requests.post(url, data = myobj)

        Turl = 'http://wmsapp.pythonanywhere.com/temperature/'
        Tmyobj = {
          'Tvalue': temperature
                    }
        Tx = requests.post(Turl, data = Tmyobj)


        print(Tx.text)
        print(x.text)


    time.sleep(0.01) 

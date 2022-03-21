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

        hari = today.strftime("%B %d, %Y")

        current_time = now.strftime("%H:%M:%S")
        # read the bytes and convert from binary array to ASCII
        data_str = ser.read(ser.inWaiting()).decode('ascii') 
        # print the incoming string without putting a new-line
        # ('\n') automatically after every print()
        # value = data_str,end=''
        # print(value) 
        # print(current_time) 
        url = 'https://wmsapp.pythonanywhere.com/wmsapp/'
        myobj = {
          'value': data_str,
          'tanggal' : hari,
          'jam' : current_time
                    }
        x = requests.post(url, data = myobj)


        print(x.text)

    # Put the rest of your code you want here
    
    # Optional, but recommended: sleep 10 ms (0.01 sec) once per loop to let 
    # other threads on your PC run during this time. 
    time.sleep(0.01) 

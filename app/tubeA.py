import serial
import math
import requests
import json
import time
import RPi.GPIO as GPIO

# defining pins
sound1 = 23
sound2 = 24
sound3 = 22
tubeA = 18
tubeB = 16
lock = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

# defining url & headers
url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube&user_id=1'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
}

header2 = {"User-Agent": "/", "Content-Type": "application/json"}

def process_tubeA():
    state = False
    doorStatus = False
    def button_callback(channel):
        print("Button was pushed!")
        state = True
    # reading request
    x = requests.get(url, headers=headers)
    print(x.status_code)
    print(x.text)

    # deserialising json
    x = json.loads(x.text)
    p_id = x['Patient_ID']
    print('Result: ', x['Result'])
    print('Patient Name: ', x['Patient Name'])
    print('Tube Name: ', x['Tube Name'])
    print('Patient ID: ', x['Patient_ID'])
    print('Treatement in Joule: ', x['Treatment Dose (in Joule)'])

                # BUTTON CONDITION
    if (GPIO.input(19) == GPIO.LOW):
            state = True


    while (state == True):
        # initiating session
        s = requests.Session()
        print("Button was pushed!")
        # turning sound 1 on
        GPIO.output(23, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(23, GPIO.LOW)
        time.sleep(10)

        # reading Sensor Data
        ser1 = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
        # turning sound 2 on
        GPIO.output(24, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(24, GPIO.LOW)

        # calibrating input reading to millis
        val = float(x['Treatment Dose (in Joule)']) / 3.6

        reading1 = []
        b = 0


        def sum_reading1(x):
            a = 0
            for i in x:
                a = a + i

            return '%.016f' % a


        # initiating sensor read
        while True:
            # Lock
            if ((GPIO.input(17) == GPIO.HIGH)):
                doorStatus = False
            else:
                doorStatus = True
            while doorStatus == False:
                GPIO.output(18, GPIO.LOW)
                reading1.append(0)
                print('Paused')
                if ((GPIO.input(17) == GPIO.LOW)):  # lock
                    break
            else:
                # turning TUBE A ON
                GPIO.output(18, GPIO.HIGH)
                ser1.write(b'getirradiance\r')
                line = ser1.readline()
                line = line.decode()
                line = float(line)
                if (line > 0):
                    reading1.append(line)
                    b = b + 1
                    total_value1 = sum_reading1(reading1)
                    print(b, '. ', 'Val:', val, 'Current Reading: ', '%.016f' % line, '|', 'Total Raddiance:',
                        (float(total_value1)))

                    write_url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube_complete&user_id={0}&operation={1}&reading={2}&status=ok'.format(
                        p_id, 'Running', str(total_value1))
                    #                   r = s.post(write_url, headers=header2, stream=True)
                    #                   print(r.status_code)

                    # http write
                    #                   write_url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube_complete&user_id={0}&operation={1}&reading={2}&status=ok'.format(p_id,'Running',str(total_value1))
                    #
                    #                   ##sending data
                    #                   r = requests.post(url=write_url, headers=header2)
                    #                   print(r.status_code)
                    #                   print(r.text)

                    if (float(total_value1) >= val):
                        print('line: ', '%.016f' % line)

                        # http write
                        write_url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube_complete&user_id={0}&operation={1}&reading={2}&status=ok'.format(
                            p_id, 'Completed', str(total_value1))
                        r = requests.post(url=write_url, headers=header2)
                        print(r.status_code)
                        print(r.text)
                        print('Threshold reached')
                        ser1.close()  # close port

                        # turning TUBE A OFF
                        GPIO.output(18, GPIO.LOW)

                        # turning sound 3 on
                        GPIO.output(22, GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(22, GPIO.LOW)
                        state = False
                        print(state)
                        print('Threshold reached')
                        break
                else:
                    time.sleep(1)
                    pass
                time.sleep(1)

        


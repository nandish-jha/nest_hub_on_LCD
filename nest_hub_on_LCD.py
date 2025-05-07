import board
import psutil
import datetime
import lcd_driver
import adafruit_dht
from time import sleep
from gpiozero import Button

state = 1
button2 = Button(27)
button1 = Button(22)

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D24)

disp = lcd_driver.lcd()

print("Running on the LCD")

while True:
    try:
        temp = sensor.temperature
        humi = sensor.humidity
    
    except RuntimeError as error:
        error.args[0]
        continue
    
    except Exception as error:
        sensor.exit()
        raise error
    
    date_n_time_texts = str(datetime.datetime.now())
    
    date_text = "Date: " + date_n_time_texts[8:10] + date_n_time_texts[4:8] + date_n_time_texts[0:4]
    time_text = "Time: " + date_n_time_texts[11:21]
    
    if humi == None:
        humi_level = "wait..."
    elif 0 < humi < 30:
        humi_level = "Dry"
    elif 30 < humi < 60:
        humi_level = "Comfi"
    elif 60 < humi:
        humi_level = "Humid"
    atmo_text = str(temp) + " C and " + humi_level
    
    if button1.is_pressed:
        disp.clear()
        state = state - 1
        if state == 0:
            state = 3
        sleep(0.2)
    elif button2.is_pressed:
        disp.clear()
        state = state + 1
        if state == 4:
            state = 1
        sleep(0.2)

    if state == 1:
        disp.display_line(time_text, 1)
        disp.display_line("<3     P1     2>", 2)
    elif state == 2:
        disp.display_line(date_text, 1)
        disp.display_line("<1     P2     3>", 2)
    elif state == 3:
        disp.display_line(atmo_text, 1)
        disp.display_line("<2     P3     1>", 2)

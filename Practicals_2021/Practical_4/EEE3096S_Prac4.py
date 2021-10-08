from time import time
import busio
import digitalio
import board
# import os
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
import datetime
import threading

chan1 = 0
chan2 = 0
btn_TimeStep = 8
step = 10
timeStart = None


def setup():
    global chan1, chan2, timeStart
    GPIO.setmode(GPIO.BCM)
 # Input button setup with event detection
    GPIO.setup(btn_TimeStep,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(btn_TimeStep,GPIO.FALLING, callback = setTimeStep, bouncetime = 200)
 # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
 # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
 # create an analog input channel on pins 1 and 2
    chan1 = AnalogIn(mcp, MCP.P1)
    chan2 = AnalogIn(mcp, MCP.P2)
 
 #Setup Column heads
    print("{0:<12}{1:<15}{2:<10}{3:<15}".format("Runtime","Temp Reading","Temp","Light Reading"))
 #Fetch time corresponding with the start up of the program
    timeStart = datetime.datetime.now

    pass

def display(step):
    #********************************************************************************************************
 # Initiate time thread
    global timeThread
    timeThread = threading.Timer(step, display)
    timeThread.daemon = True
    timeThread.start()
 # Fetch sensor data
 #   dRun = ((timeStart - datetime.datetime.now))
    Temp_ADC = chan2.value
    Temp = "{0:2.2f} C".format(chan2.voltage)
    Light_ADC = chan1.value
    print("{0:<12}{1:<15}{2:<10}{3:<15}".format("***",Temp_ADC,Temp,Light_ADC))

 # Button IRQ handling
def setTimeStep(channel):
    global step
    if step == 10:
        step = 5
    elif step == 5:
        step = 1
    else:
        step = 10
    pass
    timeThread.join()
    display(step)

if __name__ == "__main__":
#    try:
#     # Call setup function
#        setup()
#        display(step)
#        while True:  
#            pass
#    except Exception as e:
#        print(e)
#    finally:
#        GPIO.cleanup()
    setup()
    display(step)
    while True:
        pass

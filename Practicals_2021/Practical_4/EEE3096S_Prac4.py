import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
import datetime
import threading

chan1 = 0
chan2 = 0
btn_TimeStep = 23
step = 10
timeStart = None
timeThread = None


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
    timeStart = datetime.datetime.now()

    pass

 # Button IRQ handling
def setTimeStep(channel):
    global step #, timeThread
    if step == 10:
        step = 5
    elif step == 5:
        step = 1
    else:
        step = 10
    pass
#    timeThread.join()
#    display()

def display():
    #********************************************************************************************************
 # Initiate time thread
    global timeThread, step
    timeThread = threading.Timer(step, display)
    timeThread.daemon = True
    timeThread.start()
 # Runtime calculation
    dur = (datetime.datetime.now() - timeStart)
    durString = "{0:3.0f}s".format(dur.seconds)
 # Fetch sensor data
    Temp_ADC = chan1.value
    #Calculate temperature by defining the MCP9700 Temperature vs. Output voltage plot as (y = mx + c)
    Temp = "{0:2.2f} C".format(100*(chan1.voltage-0.5))
    Light_ADC = chan2.value
    print("{0:<12}{1:<15}{2:<10}{3:<15}".format(durString,Temp_ADC,Temp,Light_ADC))

if __name__ == "__main__":
    try:
     # Call setup function
        setup()
        display()
        while True:  
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()

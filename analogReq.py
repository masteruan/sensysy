# Python script
# Date: 27 Giugno
# sudo python analogReq.py
#

import time
import httplib
import subprocess
import Adafruit_ADS1x15
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_DHT

from neopixel import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

tempo = 6
# PIR
sum = 0
medium = 0
sum2 = 0
medium2 = 0

# LED strip configuration:
LED_COUNT      = 2      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/$
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor$
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()


adc = Adafruit_ADS1x15.ADS1115()

sensor = Adafruit_DHT.DHT11
dhtPin = 23 #23

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 2/3

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2 # default -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 3

# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/arialn.ttf",22)

# Obtain IP
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )
#print ip
font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/arialn.ttf",30)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Write two lines of text.
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.text((x, top + 24), " " + str(IP),  font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(2)
print('Reading PIR')
for i in range (10):
    values = adc.read_adc(1, gain = GAIN)
    int(values)
    sum += values
    time.sleep(0.2)
medium = sum/10
while True:
    values2 = adc.read_adc(1, gain=GAIN)
    int(values2)
    if (values2 > medium + 500):
        print("start")
        font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/arialn.ttf",30)
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Write two lines of text.
        image = Image.new('1', (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        draw.text((x, top + 24), "  Air OK", font=font, fill=255)
        disp.image(image)
        disp.display()
        for i in range (2):
            strip.setPixelColorRGB(i, 255, 255, 255)
            strip.show()
        time.sleep(3)
        try:
        	#humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtPin)
            print("OK_DHT")
            print(temperature)
            print(humidity)
            if temperature is None:
                humidity = str(30)
                temperature = str(25)
            except:
    	    humidity = str(30)
    	    temperature = str(25)

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Read the specified ADC channel using the previously set gain value.
        value = adc.read_adc(0, gain=GAIN)

        # Write two lines of text.
        image = Image.new('1', (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        #draw.text((x, top),         "IP: " + str(IP),  font=font, fill=255)
        draw.text((x, top + 10),     "Temp: " + str(temperature) + "C", font=font, fill=255)
        draw.text((x, top + 40),     "Humi:  " + str(humidity) + "%", font=font, fill=255)
        #draw.text((x, top + 44),    "Air: OK", font=font, fill=255)
        #draw.text((x, top + 44),    "Analog: " + str(value), font=font, fill=255)
        #draw.text((x, top + 60),    "FabLab rules!", font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(8)

        def printText(txt):
            lines = txt.split('\n')
            for line in lines:
                print line.strip()
        httpServ = httplib.HTTPConnection("beta.joule40.com", 80)
        httpServ.connect()
        httpServ.request("GET", "/wp-content/themes/wpbootstrap/check_consumption.php?id_smartobject=2&temperatura="+temperature+"&umidita="+humidity+"&aria=20&presenza=1")
        response = httpServ.getresponse()
        result = response.read()

        # simulation
        #result = "value=12332341"
        if response.status == httplib.OK:
            print "Output from HTML request:"
            print (result)
            r = result
            slices = [r[0:6], r[6:7], r[7:8], r[8:9], r[9:10], r[10:11], r[11:12], r[12:13], r[13:14]]

            # Immagini OLED
            # Prima Riscaldamento
            image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Heating.jpg').convert('1')
            if slices[1] == '1':
                print ("neopixel bianco")
                for i in range (2):
                    strip.setPixelColorRGB(i, 255, 255, 255) # white

            elif slices[1] == '2':
                print ("neopixel arancione")
                for i in range (2):
                    strip.setPixelColorRGB(i, 255, 100, 0) # orange

            elif slices[1] == '3':
                print ("neopixel rosso")
                for i in range (2):
                    strip.setPixelColorRGB(i, 255, 0, 0) # red
            disp.image(image)
            strip.show()
            disp.display()
            time.sleep(tempo)
            # Secondo Riscald caldo sanit
            if slices[2] == '4':
                print("Riscaldamento")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Hot.jpg').convert('1')
                if slices[2] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[2] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[2] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

            # Terza Acqua fredda
            if slices[3] == '4':
                print("Fredda")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Cold.jpg').convert('1')
                if slices[3] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[3] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[3] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

            # Quarta acqua tecnica
            if slices[4] == '4':
                print ("Tecnica")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Tec.jpg').convert('1')
                if slices[4] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[4] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[4] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

            # Quinto Riscaldamento contabilizzato
            if slices[5] == '4':
                print("Riscaldamento")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Direct.jpg').convert('1')
                if slices[5] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[5] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[5] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

            # Sesto raffreddamento
            if slices[6] == '4':
                print("Raffreddamento")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Cooling.jpg').convert('1')
                if slices[6] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[6] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[6] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

            # Settimo Electric
            if slices[7] == '4':
                print("Electric")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Electric.jpg').convert('1')
                if slices[7] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[7] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[7] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

            # Ottavo ASC
            if slices[8] == '4':
                print("ASC")
            else:
                image = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/imm/Asc.jpg').convert('1')
                if slices[8] == '1':
                    print ("neopixel bianco")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 255, 255) # white

                elif slices[8] == '2':
                    print ("neopixel arancione")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 100, 0) # orange

                elif slices[8] == '3':
                    print ("neopixel rosso")
                    for i in range (2):
                        strip.setPixelColorRGB(i, 255, 0, 0) # red
                disp.image(image)
                strip.show()
                disp.display()
                time.sleep(tempo)

        httpServ.close()
        disp.clear()
        disp.display()
        for i in range (2):
            strip.setPixelColorRGB(i, 0, 0, 0)
            strip.show()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtPin)
    else:
        print("stop")
        for i in range (2):
            strip.setPixelColorRGB(i, 0, 0, 0)
            strip.show()
            disp.clear()
            disp.display()
        time.sleep(1)
# fine

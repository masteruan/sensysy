import time
import httplib


import Adafruit_ADS1x15
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_DHT

from neopixel import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Led configuration
# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/$
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor$
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

import subprocess
# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

sensor = Adafruit_DHT.DHT11
dhtPin = 17 #23

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))


# Initialize library.
#disp.begin()

# Clear display.
#disp.clear()
#disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
#width = disp.width
#height = disp.height
#image = Image.new('1', (width, height))

# Get drawing object to draw on image.
#draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
#padding = 0 #default -2
#top = padding
#bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 3

# Load default font.
font = ImageFont.load_default()
#font = ImageFont.truetype("arialn.ttf",18)

# Obtain IP
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )

while True:

    humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtPin)
    humidity = str(humidity) #int(hmidity)
    temperature = str(temperature) #int(temperature)

    # Draw a black filled box to clear the image.
#    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Read the specified ADC channel using the previously set gain value.
#    value = adc.read_adc(0, gain=GAIN)

    # Write two lines of text.

#    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
#    draw.text((x, top+16),    "Temp is: " + str(temperature) + " C", font=font, fill=255)
#    draw.text((x, top+30),    "Humi is: " + str(humidity) + " %", font=font, fill=255)
#    draw.text((x, top+46),    "Analog: " + str(value), font=font, fill=255)
    #draw.text((x, top+46),    "FabLab rules!", font=font, fill=255)

    # Display image.
#    disp.image(image)
#    disp.display()
#   time.sleep(.1)

    def printText(txt):
        lines = txt.split('\n')
        for line in lines:
            print line.strip()
    httpServ = httplib.HTTPConnection("beta.joule40.com", 80)
    #httpServ = httplib.HTTPConnection("api.thingspeak.com", 80)
    httpServ.connect()
    httpServ.request("GET", "/wp-content/themes/wpbootstrap/check_consumption.php?id_smartobject=2&temperatura="+temperature+"&umidita="+humidity+"&aria=20&presenza=1")
    #httpServ.request("GET", "/update?api_key=7JUW5OPBI90Q3S2N&field1=33")

    response = httpServ.getresponse()
    result = response.read()
    if response.status == httplib.OK:
        print "Output from HTML request"
        print (result)
        r = result
        slices = [r[0:6], r[6:7], r[7:8], r[8:9], r[9:10], r[10:11], r[11:12], r[12:13], r[13:14]]

        # Neopixel
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

        if result == "value=44444444":
            print "Il valore: 44444444"
            image = Image.open('icon44444444.jpg').convert('1')
        elif result == "value=14444414":
            print "Il valore: 14444414"
            image = Image.open('icon14444414.jpg').convert('1')

    httpServ.close()
    disp.image(image)
    disp.display()
    strip.show()
    time.sleep(5)

import serial
import Adafruit_SSD1306
import Adafruit_GPIO.SPI as SPI

import time 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

font = ImageFont.load_default()
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

def main():
    disp.begin()
    draw.rectangle((0,0,128,64),outline=0,fill=0) #Clear the display
    while 1:
        f = open("test1.txt","r")
        #take sarial data from txt file
        title = f.read()
        artist = f.read()
        album = f.read()
        track = f.read()
        draw.text((5,5), str(title),  font=font, fill=255)
        draw.text((5,25), str(artist),  font=font, fill=255)
        draw.text((5,45), str(album),  font=font, fill=255)
        draw.text((5,60),  str(track),  font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()
        draw.rectangle((0,0,128,64),outline=0,fill=0) #Clear the display
        f.close()


if __name__ == '__main__':
    main()

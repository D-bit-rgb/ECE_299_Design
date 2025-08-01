
from machine import Pin, SPI
# Download the ssd1306.py driver to your project directory
# You can use: wget https://raw.githubusercontent.com/micropython/micropython/master/drivers/display/ssd1306.py

from ssd1306 import SSD1306_SPI

# SPI shared lines
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

# Shared DC and RES pins
dc = Pin(20)
res = Pin(21)

# Individual CS pins
cs1 = Pin(7)
cs2 = Pin(22)

# Individual displays
oled1 = SSD1306_SPI(128, 64, spi, dc, res, cs1)
oled2 = SSD1306_SPI(128, 64, spi, dc, res, cs2)

# Bridged Display class
class BridgedOLED:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.width = 256
        self.height = 64

    def fill(self, color):
        self.left.fill(color)
        self.right.fill(color)

    def pixel(self, x, y, color):
        if x < 128:
            self.left.pixel(x, y, color)
        else:
            self.right.pixel(x - 128, y, color)

    def text(self, string, x, y, color=1):
        for i, char in enumerate(string):
            px = x + i * 8
            if px + 8 <= 128:
                self.left.text(char, px, y, color)
            elif px >= 128:
                self.right.text(char, px - 128, y, color)
            else:
                pass

    def show(self):
        self.left.show()
        self.right.show()

# Instantiate and test
display = BridgedOLED(oled1, oled2)
display.fill(0)
display.text("LEFT SIDE", 10, 10)
display.text("RIGHT SIDE", 140, 10)
display.show()

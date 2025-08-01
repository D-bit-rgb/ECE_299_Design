from machine import Pin, SPI
from ssd1306_dual import SSD1306_DualSPI
from time

#Initialization

spi = SPI(0, sck=Pin(18), mosi=Pin(19))
dc = Pin(20)
res = Pin(21)
cs1 = Pin(17) #screen 1
cs2 = Pin(5)  #screen 2

display = SSD1306_DualSPI(256, 64, spi, dc, res, cs1, cs2)

#main

display.fill(0)
display.text("Time: "time.local_time, 0, 10)
display.text("Mode: Clock", 0, 30)
display.text("Freq: 98.5", 140, 10)

display.show()
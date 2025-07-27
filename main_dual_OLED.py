from machine import Pin, SPI
from ssd1306_dual import SSD1306_DualSPI


#Initialization


spi = SPI(0, sck=Pin(18), mosi=Pin(19))
dc = Pin(20)
res = Pin(21)
cs1 = Pin(17)  # First screen
cs2 = Pin(5)   # Second screen

display = SSD1306_DualSPI(256, 64, spi, dc, res, cs1, cs2)

##################################################################

#main file for display

display.fill(0)
display.text("World", 130, 20)
display.text("Hello", 0, 20)

display.show()

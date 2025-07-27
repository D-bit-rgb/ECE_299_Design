
from machine import Pin, SPI
from display import SSD1306_DualSPI
from radio import Radio
import time

# Setup SPI Display
spi = SPI(0, sck=Pin(18), mosi=Pin(19))
dc = Pin(20)
res = Pin(21)
cs1 = Pin(17)
cs2 = Pin(5)

display = SSD1306_DualSPI(256, 64, spi, dc, res, cs1, cs2)

# Setup buttons
btn_mode = Pin(0, Pin.IN, Pin.PULL_UP)
btn_select = Pin(1, Pin.IN, Pin.PULL_UP)
btn_up = Pin(2, Pin.IN, Pin.PULL_UP)
btn_down = Pin(3, Pin.IN, Pin.PULL_UP)

last_mode = 1
mode = 0
alarm_time = [6, 30]  # 6:30 AM
alarm_active = False

# Setup radio
fm = Radio(101.9, 2, False)

def draw_clock():
    now = time.localtime()
    display.text("Time: {:02d}:{:02d}".format(now[3], now[4]), 10, 10)
    if alarm_active:
        display.text("Alarm: {:02d}:{:02d}".format(*alarm_time), 140, 10)

def draw_alarm_set():
    display.text("Set Alarm:", 10, 10)
    display.text("Hour: {:02d}".format(alarm_time[0]), 10, 30)
    display.text("Min : {:02d}".format(alarm_time[1]), 140, 30)

def draw_radio():
    display.text("FM Radio", 10, 10)
    display.text("Freq: {:.1f}".format(fm.Frequency), 10, 30)
    display.text("Vol: {}".format(fm.Volume), 140, 30)

while True:
    # Mode button
    current_mode = btn_mode.value()
    if last_mode == 1 and current_mode == 0:
        mode = (mode + 1) % 4
        time.sleep(0.25)
    last_mode = current_mode

    display.fill(0)

    if mode == 0:  # Clock
        draw_clock()
    elif mode == 1:  # Alarm Set
        draw_alarm_set()
        if not btn_up.value():
            alarm_time[0] = (alarm_time[0] + 1) % 24
            time.sleep(0.2)
        if not btn_down.value():
            alarm_time[1] = (alarm_time[1] + 1) % 60
            time.sleep(0.2)
        if not btn_select.value():
            alarm_active = not alarm_active
            time.sleep(0.2)
    elif mode == 2:  # Radio
        draw_radio()
        if not btn_up.value():
            fm.SetVolume((fm.Volume + 1) % 16)
            fm.ProgramRadio()
            time.sleep(0.2)
        if not btn_down.value():
            fm.SetVolume((fm.Volume - 1) % 16)
            fm.ProgramRadio()
            time.sleep(0.2)
    elif mode == 3:  # Alarm check
        now = time.localtime()
        if alarm_active and (now[3], now[4]) == tuple(alarm_time):
            display.text("WAKE UP!", 80, 25)
        else:
            display.text("No Alarm Now", 80, 25)

    display.show()
    time.sleep(0.05)

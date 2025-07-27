
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

last_button_state_btn_mode = 1  # Start unpressed
last_button_state_btn_select = 1  # Start unpressed
last_button_state_btn_up = 1  # Start unpressed
last_button_state_btn_down = 1  # Start unpressed

last_mode = 1
mode = 0
alarm_time = [6, 30]  # 6:30 AM
alarm_active = False

# Setup radio
fm = Radio(101.9, 2, False)

def button_pressed(button, last_state):
    current_state = button.value()
    if last_state == 1 and current_state == 0:
        time.sleep(0.05)
        if button.value() == 0:
            return True, 0
    return False, current_state

def draw_clock():
    now = time.localtime()
    display.text("Time: {:02d}:{:02d}".format(now[3], now[4]), 10, 10)
    if alarm_active:
        display.text("Alarm: {:02d}:{:02d}".format(*alarm_time), 140, 10)
        display.text("Mode: Clock", 10, 50)

def draw_alarm_set():
    display.text("Set Alarm:", 10, 10)
    display.text("Hour: {:02d}".format(alarm_time[0]), 10, 30)
    display.text("Min : {:02d}".format(alarm_time[1]), 140, 30)
    display.text("Mode: Alarm Set", 10, 50)

def draw_radio():
    display.text("FM Radio", 10, 10)
    display.text("Freq: {:.1f}".format(fm.Frequency), 10, 30)
    display.text("Vol: {}".format(fm.Volume), 140, 30)
    display.text("Mode: Radio", 10, 50)

while True:
    # Mode button
    
    print(mode)
    
    mode = 0

    pressed_mode, last_button_state_btn_mode = button_pressed(btn_mode, last_button_state_btn_mode)
    if pressed_mode:
        mode = (mode + 1)  # Cycle through 0 to 3
        if mode > 3:
            mode = 0

    display.fill(0)

    if mode == 0:  # Clock
        draw_clock()
        print(mode)


    elif mode == 1:  # Alarm Set
        draw_alarm_set()

        pressed_up, last_button_state_btn_up = button_pressed(btn_up, last_button_state_btn_up)
        pressed_down, last_button_state_btn_down = button_pressed(btn_down, last_button_state_btn_down)
        
        if pressed_up and last_button_state_btn_up:
            alarm_time[0] = (alarm_time[0] + 1) % 24
            time.sleep(0.2)

        if pressed_down and last_button_state_btn_down:
            alarm_time[1] = (alarm_time[1] + 1) % 60
            time.sleep(0.2)

        if button_pressed(btn_select, last_button_state_btn_select)[0]:
            alarm_active = not alarm_active
            time.sleep(0.2)


    elif mode == 2:  # Radio
        draw_radio()
        if button_pressed(btn_up, last_button_state_btn_up)[0]:
            fm.SetVolume((fm.Volume + 1) % 16)
            fm.ProgramRadio()
            time.sleep(0.2)
        if button_pressed(btn_down, last_button_state_btn_down)[0]:
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

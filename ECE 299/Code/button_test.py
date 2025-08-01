# button_test.py
from machine import Pin
import time

# Define GPIO pins for the buttons
button_pins = [0, 3, 6, 7]

# Create Pin objects with internal pull-ups
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]
last_states = [1] * len(buttons)

print("Button test running. Press any button...")
print("Button 1 (GPIO {0}) pressed")
while True:
    for i, btn in enumerate(buttons):
        state = btn.value()
        if state == 0 and last_states[i] == 1:  # falling edge = button pressed
            print(f"Button {i} (GPIO {button_pins[i]}) pressed")
        last_states[i] = state
    time.sleep(0.01)

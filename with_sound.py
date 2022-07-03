import os
from playsound import playsound
import neopixel
import board

from adafruit_led_animation.animation.pulse import Pulse

from adafruit_led_animation.color import AMBER

pixel_pin = board.D21
pixel_num = 28
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness = .1, pixel_order=neopixel.GRB, auto_write = False)
pulse = Pulse(pixels, speed = 0.1, color = AMBER, period = 3)

while True:
      playsound.playsound("Happy_Voice.wav")
      pulse.animate()
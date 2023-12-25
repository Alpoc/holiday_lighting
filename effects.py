import board
import collections
import neopixel
from rainbowio import colorwheel
import random
import time
import numpy as np
import math
import datetime

PIXEL_PIN = board.D21 # gpio number, D21 is pin 40
global NUM_PIXELS
NUM_PIXELS = 200
BRIGHTNESS = 1 # 0.0 - 1
PIXEL_ORDER = neopixel.RGB
# PIXEL_ORDER = neopixel.BRG

OFF = (0, 0, 0)

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, pixel_order=PIXEL_ORDER, brightness=BRIGHTNESS, auto_write=False)

def off():
    pixels.fill(OFF)
    pixels.show()


def keep_running(start_time, run_time=None):
    """
    Check if the program is intended to keep runnning.
    -1 run time to keep running indefinetly.
    args:
        start_time: when the program started
        run_time: seconds the program is intended to run for
    """
    if run_time and run_time > 0:
        now = time.time() - start_time
        seconds = int(now % 60)
        if seconds > run_time:
            return False
    return True


def color_cycle(sleep_time, colors, run_count):
    """ cycle through colors.
        supply a single color for a pulse.
        args:
            colors: the colors to cycle through
            sleep_time: how fast the effect runs
            run_count: how many times the effect should run
    """
    for _ in range(0, run_count):
        for color in colors:
            pixels.fill(color)
            pixels.show()
            time.sleep(sleep_time)


def color_cycle_fade(sleep_time, colors, run_count):
    """ cycle through colors fading in and out.
        supply a single color for a pulse.
        args:
            colors: the colors to cycle through
            sleep_time: how fast the effect runs
            run_count: how many times the effect should run
    """
    for _ in range(0, run_count):
        for color in colors:

            for brightness in np.arange(0, 1, 0.1):
                pixels.brightness = brightness / 10
                pixels.fill(color)
                pixels.show()
                time.sleep(sleep_time)

            for brightness in np.arange(1, 10, 0.2):
                pixels.brightness = brightness / 10
                pixels.fill(color)
                pixels.show()
                time.sleep(sleep_time)

            for brightness in np.arange(10, 1, -0.2):
                pixels.brightness = brightness / 10
                pixels.fill(color)
                pixels.show()
                time.sleep(sleep_time)
    pixels.brightness = BRIGHTNESS


def timed_fill(sleep_time, colors, run_count=None):
    """
    fill the strand from start to finish
    args:
        colors: the colors to cycle through
        sleep_time: how fast the effect runs
        run_count: how many times the effect should run
    """
    for _ in range(0, run_count):
        for color in colors:
            for i in range(NUM_PIXELS):
                pixels[i] = color
                time.sleep(sleep_time)
                pixels.show()
        time.sleep(sleep_time)


def single_down(sleep_time=0, color_list=None, run_count=None):
    """
    light up a single led down the chain sequentially.
    args:
        sleep_time: how fast it goes down the chain
        single_color: if you dont want random color specify the color here
        run_time: number of times the effect should run
    """
    start_time = time.time()
    if sleep_time == -1:
        random.uniform(0.05, 0)
    color = color_list
    for _ in range(0, run_count):
        if not color_list:
            rand_color = random.randint(0, 255)
            color_list = [colorwheel(rand_color)]
        for color in color_list:
            for i in range(NUM_PIXELS):
                pixels[i] = color
                if i > 0:
                    pixels[i - 1] = OFF
                elif i == 0:
                    pixels[NUM_PIXELS - 1] = OFF
                pixels.show()
                time.sleep(sleep_time)


def rainbow_cycle(sleep_time, run_time=None):
    start_time = time.time()
    while keep_running(start_time, run_time):
        for j in range(255):
            for i in range(NUM_PIXELS):
                rc_index = (i * 256 // NUM_PIXELS) + j
                pixels[i] = colorwheel(rc_index & 255)
            pixels.show()
            time.sleep(sleep_time)


def create_filled_collection(colors, width):
    color_collection = []
    color = 0
    duplicate = 1
    for i in range(NUM_PIXELS):
        if color >= len(colors):
            color = 0
        color_collection.append(colors[color])
        if duplicate < width:
            duplicate += 1
        else:
            color += 1
            duplicate = 1
    color_col = collections.deque(color_collection)
    return color_col

def color_wave_full(sleep_time, colors, width=None, run_time=None):
    """
    itterate the colors down the chain
    TODO: make this a linked list so that we may itterate through longer widths
    args:
        sleep_time: speed of the loop
        colors: list of colors to loop through
        width: number of same color in a row
        run_time: how long in seconds the effect should run for
    """
    start_time = time.time()
    color_col = create_filled_collection(colors, width)

    while keep_running(start_time, run_time):
        for i in range(NUM_PIXELS):
            pixels[i] = color_col[i]
        pixels.show()
        time.sleep(sleep_time)
        color_col.rotate(1)


def left_right_shift(color_list, width, shift_amount, run_time):
    """
    move back and forth
    args:
        sleep_time: speed of the loop
        colors: list of colors to loop through
        width: number of same color in a row
        run_time: how long in seconds the effect should run for
    """
    start_time = time.time()
    color_col = create_filled_collection(color_list, width)
    shift_direction = 1
    shift_count = 0
    sleep_time = 0.05
    while keep_running(start_time, run_time):
        for i in range(NUM_PIXELS):
            pixels[i] = color_col[i]
        pixels.show()
        time.sleep(sleep_time)
        color_col.rotate(shift_direction)
        shift_count += shift_direction
        if abs(shift_count) >= shift_amount:
            shift_direction *= -1


def water_waves(color_list, width, shift_amount, run_time):
    """
    two steps forward 1 step back. trying to make an beach wave effect.
    args:
        colors: list of colors to loop through
        width: number of same color in a row
        shift_amount: amount to move forward and back
        run_time: how long in seconds the effect should run for
    """
    start_time = time.time()
    color_col = create_filled_collection(color_list, width)
    shift_direction = 1
    shift_count = 0
    shift_amount_neg = round(shift_amount *-1 *.6)
    velocity_sleep = initial_sleep = 0.05
    while keep_running(start_time, run_time):
        for i in range(NUM_PIXELS):
            pixels[i] = color_col[i]
        pixels.show()
        velocity_sleep += 0.007

        time.sleep(velocity_sleep)
        color_col.rotate(shift_direction)

        shift_count += shift_direction
        if shift_count >= shift_amount:
            shift_direction *= -1
            shift_count = 0
            velocity_sleep = initial_sleep
        elif shift_count <= shift_amount_neg:
            shift_direction *= -1
            shift_count = 0
            velocity_sleep = initial_sleep
        choice = random.randint(0, 6)


def single_down_fill(color_list):
    """
    send a single light down the strand filling the end when it hits a light or the end.

    args:
        color_list: list of colors to use
    """
    import itertools
    fill_stop = NUM_PIXELS - 1
    color_iter = itertools.cycle(iter(color_list))
    while fill_stop > 0:
        color = next(color_iter)
        for x in range(NUM_PIXELS):
            pixels[x] = color
            if x > 0:
                pixels[x - 1] = OFF
            if x == fill_stop:
                fill_stop -= 1
                break
            pixels.show()

class Pixel():
    def __init__(self, color):
        self.location = random.randint(0, NUM_PIXELS - 1)
        self.color = color
        self.brightness_divisor = 1
        self.set_pixel()

    def lower_brightness(self):
        if math.isinf(self.brightness_divisor):
            return
        if self.brightness_divisor == 9:
            x = math.inf
        self.color = tuple(x/self.brightness_divisor for x in self.color)
        self.brightness_divisor += 1
        self.set_pixel()

    def set_pixel(self):
        print(self.location)
        print(self.color)
        print()
        pixels[self.location] = self.color


def fireworks(colors, run_time=60):
    """
    Burst outwards from random location(s)

    args:
        colors: list of colors
        run_time: duration of time to run in seconds
    """
    #pixels.fill(colors[-1])
    #pixels[120] = colors[0]
    #for x in range(1, 10):
    #    color_choice = colors[0]
    #    if x == 9:
    #        x = math.inf
    #    else:
    #        x = x**1.1
    #    print(x)
    #    color = tuple([y/x for y in color_choice])
    #    print(str(color))
    #    pixels.fill(color)
    #    pixels.show()
    #    time.sleep(0.2)
    #exit()

    while keep_running(time.time(), run_time):
        origins = [Pixel(random.choice(colors))] * random.randint(1, 1)
        explosions = origins
        width = 5
        for origin in origins:
            origin.location = 120
        pixels.show()
        current_width = 1
        while current_width < width:
            for pixel in origins:
                pixel_right_local = pixel.location - current_width
                pixel_left_local = pixel.location + current_width
                if pixel_right_local > 0:
                    left_pixel = Pixel(color=pixel.color)
                    left_pixel.location = pixel_right_local
                    left_pixel.set_pixel()
                    explosions.append(left_pixel)
                if pixel_left_local < NUM_PIXELS:
                    right_pixel = Pixel(color=pixel.color)
                    right_pixel.location = pixel_left_local
                    explosions.append(right_pixel)
                    right_pixel.set_pixel()
                current_width += 1
            pixels.show()
            for pixel in explosions:
                pixel.lower_brightness()
                pixel.set_pixel()

            pixels.show()
        while len(explosions) > 0:
            for pixel in explosions:
                if math.isinf(pixel.brightness_divisor):
                    explosions.remove(pixel)
                else:
                    pixel.lower_brightness()
                pixels.show()


def no_effects():
    """
    Do not run effects while sleeping, only soft glow for night light.
    Turn off lights during the daytime
    """
    off = 9
    start = 16
    end = 20

    current_hour = datetime.datetime.today().hour
    while end < current_hour or current_hour < start:
        print(f'current time: {current_hour}')
        if off < current_hour < start:
            print('turning lights off')
            pixels.brightness = 0
        else:
            pixels.brightness = 0.05
            print('nightlight mode')
        pixels.fill((255, 150, 10))
        pixels.show()
        time.sleep(60 * 10)
        current_hour = datetime.datetime.today().hour
    print('turning lights on')
    pixels.brightness = BRIGHTNESS

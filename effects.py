import board
import collections
import neopixel
from rainbowio import colorwheel
import random
import time
import numpy as np


PIXEL_PIN = board.D21 # gpio number, D21 is pin 40
global NUM_PIXELS
NUM_PIXELS = 150
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

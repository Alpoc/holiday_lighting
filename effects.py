import board
import collections
import neopixel
from rainbowio import colorwheel
import random
import time


PIXEL_PIN = board.D21 # gpio number, D21 is pin 40
global NUM_PIXELS
NUM_PIXELS = 200
BRIGHTNESS = 1 # 0.0 - 1
PIXEL_ORDER = neopixel.RGB
# PIXEL_ORDER = neopixel.BRG

global pixels
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, pixel_order=PIXEL_ORDER, brightness=BRIGHTNESS, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 69, 0)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)

colors = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, ORANGE, WHITE]


def off():
    pixels.fill(OFF)
    pixels.show()


def keep_running(start_time, run_time=None):
    """
    Check if the program is intended to keep runnning.
    """
    if run_time:
        now = time.time() - start_time
        seconds = int(now % 60)
        if seconds > run_time:
            return False
    return True


def color_cycle(sleep_time, colors, run_count):
    for _ in range(0, run_count):
        for color in colors:
            pixels.fill(color)
            pixels.show()
            time.sleep(sleep_time)

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

    while keep_running(start_time, run_time):
        for i in range(NUM_PIXELS):
            pixels[i] = color_col[i]
        pixels.show()
        time.sleep(sleep_time)
        color_col.rotate(1)


def rainbow_cycle(sleep_time, run_time=None):
    start_time = time.time()
    while keep_running(start_time, run_time):
        for j in range(255):
            for i in range(NUM_PIXELS):
                rc_index = (i * 256 // NUM_PIXELS) + j
                pixels[i] = colorwheel(rc_index & 255)
            pixels.show()
            time.sleep(sleep_time)

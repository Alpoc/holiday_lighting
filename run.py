import board
import neopixel
import time
from rainbowio import colorwheel
import collections

pixel_pin = board.D21 # gpio number, D21 is pin 40
num_pixels = 600
BRIGHTNESS = 1 # 0.0 - 1
#PIXEL_ORDER = neopixel.RGB
PIXEL_ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, pixel_order=PIXEL_ORDER, brightness=BRIGHTNESS, auto_write=False)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 69, 0)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def color_wave_full(wait, colors, width=None):
    """
    itterate the colors down the chain
    TODO: make this a linked list so that we may itterate through longer widths
    args:
        wait: speed of the loop
        colors: list of colors to loop through
        width: number of same color in a row
    """
    # Cycle through provided colors down the chain
    color_collection = []
    color = 0
    duplicate = 1
    for i in range(num_pixels):
        if color >= len(colors):
            color = 0
        color_collection.append(colors[color])
        if duplicate < width:
            duplicate += 1
        else:
            color += 1
            duplicate = 1
    color_col = collections.deque(color_collection)
    
    while True:
        for i in range(num_pixels):
            pixels[i] = color_col[i]
        pixels.show()
        time.sleep(wait)
        color_col.rotate(1)

def off():
    pixels.fill(OFF)
    pixels.show()


def single_down():
    for i in range(num_pixels):
        pixels[i] = RED
        if i > 1:
            pixels[i - 1] = OFF
        pixels.show()
        time.sleep(0.2)

print('starting')
#single_down()
print('done')
#while True:
#pixels.fill(GREEN)
#pixels.show()
#pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    #time.sleep(1)
    #pixels.fill(GREEN)
    #pixels.show()
    #time.sleep(1)
    #pixels.fill(BLUE)
    #pixels.show()
    #time.sleep(1)

    #color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    #color_chase(YELLOW, 0.1)
    #color_chase(GREEN, 0.1)
    #color_chase(CYAN, 0.1)
    #color_chase(BLUE, 0.1)
    #color_chase(PURPLE, 0.1)

    #rainbow_cycle(0)  # Increase the number to slow down the rainbow
    #color_wave_full(0.2, [RED, WHITE, BLUE])
    #off()
#color_wave_full(0.05, [RED, WHITE, BLUE], 3) 
color_wave_full(0.025, [ORANGE, OFF], 10)
#color_wave_full(0.05, [YELLOW, BLUE], 3)




import argparse
import random
import effects
from datetime import datetime

# A good source for colors https://americanpartylights.com/rgb/
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
ORANGE = (255, 30, 0)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 20, 147)
GOLD = (255, 90, 0)
DEEP_ORANGE = (70, 10, 0)

# COLOR PACKS
HALLOWEEN = [ORANGE, OFF]
FOURTH_OF_JULY = [RED, WHITE, BLUE]
VALENTINES = [RED, OFF, WHITE]
UKRAINE = [BLUE, YELLOW]
EASTER = [PINK, GREEN, PURPLE, YELLOW]
COLOR_PACKS = [HALLOWEEN, FOURTH_OF_JULY, VALENTINES, EASTER]
CHRISTMAS = [RED, GREEN]
WHITE_GOLD = [WHITE, GOLD]
THANKSGIVINGS = [RED, YELLOW, GREEN, DEEP_ORANGE]
SAINT_PATRICKS = [GREEN, WHITE]
RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE]


def get_holiday():
    cur_month = datetime.today().month
    cur_day = datetime.today().day
    if cur_month == 1 or (cur_month == 12 and cur_day > 26):
        return [WHITE_GOLD]
    if cur_month == 2:
        return [VALENTINES]
    elif cur_month == 5:
        return [EASTER]
    elif cur_month == 3:
        return [SAINT_PATRICKS]
    elif cur_month == 7:
        return [FOURTH_OF_JULY]
    elif cur_month == 10:
        return [HALLOWEEN]
    elif cur_month == 11:
        return [THANKSGIVINGS]
    elif cur_month == 12:
        return [CHRISTMAS, WHITE_GOLD, THANKSGIVINGS]
    else:
        return random.choice([UKRAINE, RAINBOW])


def random_effects():
    previous_choice = None
    choice = random.randint(0, 9)
    while True:
        while choice == previous_choice:
            choice = random.randint(0, 9)
        
        color_pack = get_holiday()
        color_pack = random.choice(color_pack)
        #choice = 8
        if choice == 0:
            print("single_down")
            effects.single_down(0, color_pack, run_count=10)
        elif choice == 1:
            print("full wave random width")
            width = random.randint(3, 10)
            effects.color_wave_full(0.5, color_pack, width, run_time=20)
        elif choice == 2:
            print("timed fill")
            effects.timed_fill(0.005, color_pack, run_count=10)
        elif choice == 3:
            print('color cycle')
            effects.color_cycle(1, color_pack, run_count=len(color_pack)*10)
        elif choice == 4:
            print('left_right_shift')
            effects.left_right_shift(color_pack, 5, 18, 58)
        elif choice == 5:
            print('water_waves')
            effects.water_waves(color_pack, width=5, shift_amount=18, run_time=58)
        elif choice == 6:
            print('color_cycle_fade')
            effects.color_cycle_fade(0.005, color_pack, 20)
        elif choice == 7:
            print('single_down_fill')
            effects.single_down_fast(color_pack)
        elif choice == 88:
            # fireworks currently does not work
            print('fireworks')
            effects.fireworks(color_pack, run_time=60)
        elif choice == 98:
            print('single_fill_fast')
            effects.single_fill_fast(color_pack)
            #effects.single_down_fill(color_pack)
        elif choice == 9:
            print('sleeping')
            effects.no_effects()

        previous_choice = choice

if __name__ == '__main__':
    print("starting program")
    parser = argparse.ArgumentParser()
    # parser.add_argument()
    args = parser.parse_args()
    random_effects()
    # effects.water_waves(EASTER, 5, 18, -1)
    print("ending program")

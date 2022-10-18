import argparse
import random
import effects

# A good source for colors https://americanpartylights.com/rgb/
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
ORANGE = (255, 69, 0)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255,20,147)

# COLOR PACKS
HALLOWEEN = [ORANGE, OFF]
FOURTH_OF_JULY = [RED, WHITE, BLUE]
VALENTINES = [RED, OFF, WHITE]
UKRAINE = [BLUE, YELLOW]
EASTER = [PINK, GREEN, PURPLE, YELLOW]
COLOR_PACKS = [HALLOWEEN, FOURTH_OF_JULY, VALENTINES, EASTER]

def random_effects():

    while True:
        # effects.off()
        choice = random.randint(0, 6)
        #color_pack = random.choice(COLOR_PACKS)
        #random.shuffle(color_pack)
        color_pack = HALLOWEEN
        if choice == 0:
            print("single_down")
            effects.single_down(0, color_pack, run_count=1)
        elif choice == 1:
            print("full wave random width")
            width = random.randint(3, 10)
            effects.color_wave_full(0.05, color_pack, width, run_time=30)
        elif choice == 2:
            print("timed fill")
            effects.timed_fill(0.005, color_pack, run_count=3)
        elif choice == 3:
            print('color cycle')
            effects.color_cycle(1, color_pack, run_count=len(color_pack))
        elif choice == 4:
            print('left_right_shift')
            effects.left_right_shift(color_pack, 5, 18, 60)
        elif choice == 5:
            print('water_waves')
            effects.water_waves(color_pack, 5, 18, 60)
        elif choice == 6:
            print('color_cycle_fade')
            effects.color_cycle_fade(0.005, color_pack, 20)


if __name__ == '__main__':
    print("starting program")
    parser = argparse.ArgumentParser()
    # parser.add_argument()
    args = parser.parse_args()
    random_effects()
    # effects.water_waves(EASTER, 5, 18, -1)
    print("ending program")

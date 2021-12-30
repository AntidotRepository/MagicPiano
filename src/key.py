import math
import mido
import time

class Key():
    def __init__(self, a_key, a_strip_leds):
        self.my_leds = dict()
        self.my_strip_leds = a_strip_leds
        self.is_white = True
        
        if isinstance(a_key, dict):
            self.is_white = True
            self.start = math.floor(a_key["start"])
            self.end = math.floor(a_key["end"] - 1)

            # Calculate 1st led as might not be fully bright
            self.my_leds[self.start] = (a_key["start"] - self.start)

            # If integer, we set it to 1
            if self.my_leds[self.start] == 0:
                self.my_leds[self.start] = 1

            # Calculate full leds
            for i in range(self.start + 1, self.end + 1):
                self.my_leds[i] = 1

            # Calculate last led as might be not fully bright
            self.my_leds[self.end + 1] = 1 - (a_key["end"] - 1 - self.end)
        else:
            self.is_white = False
            self.start = a_key    # Just for free mode
            self.end = a_key      # Just for free mode
            self.my_leds[a_key] = 1

    def light_on(self, a_color):
        for led, brightness in self.my_leds.items():
            self.my_strip_leds.my_leds[led].add_brightness(brightness, a_color)

    def light_off(self, a_color):
        for led, brightness in self.my_leds.items():
            self.my_strip_leds.my_leds[led].rem_brightness(brightness, a_color)

    def free_light_on(self, a_color):
        for led, brightness in self.my_leds.items():
            self.my_strip_leds.my_leds[led].add_brightness(brightness, a_color)
        for i in range(1, 6):  # How many LEDs do we want to play with each side of the note
            self.my_strip_leds.my_leds[self.start - i].add_brightness(brightness - (i * 0.1), a_color)
            self.my_strip_leds.my_leds[self.end + i].add_brightness(brightness - (i * 0.1), a_color)
            self.my_strip_leds.strip.show()
            time.sleep(0.05)
            self.my_strip_leds.my_leds[self.start - i].rem_brightness(brightness - (i * 0.1), a_color)
            self.my_strip_leds.my_leds[self.end + i].rem_brightness(brightness - (i * 0.1), a_color)
            self.my_strip_leds.strip.show()
            time.sleep(0.05)

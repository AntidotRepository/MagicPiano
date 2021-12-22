import math
import mido


class Key():
    def __init__(self, a_key, a_strip_leds):
        self.my_leds = dict()
        self.my_strip_leds = a_strip_leds
        self.is_white = True
        
        if isinstance(a_key, dict):
            self.is_white = True
            start = math.floor(a_key["start"])
            end = math.floor(a_key["end"] - 1)

            # Calculate 1st led as might not be fully bright
            self.my_leds[start] = (a_key["start"] - start)

            # If integer, we set it to 1
            if self.my_leds[start] == 0:
                self.my_leds[start] = 1

            # Calculate full leds
            for i in range(start + 1, end + 1):
                self.my_leds[i] = 1

            # Calculate last led as might be not fully bright
            self.my_leds[end + 1] = 1 - (a_key["end"] - 1 - end)
        else:
            self.is_white = False
            self.my_leds[a_key] = 1

    def light_on(self, a_color):
        for led, brightness in self.my_leds.items():
            self.my_strip_leds[led].add_brightness(brightness, a_color)

    def light_off(self, a_color):
        for led, brightness in self.my_leds.items():
            self.my_strip_leds[led].rem_brightness(brightness, a_color)

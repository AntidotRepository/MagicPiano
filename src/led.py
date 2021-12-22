from rpi_ws281x import *
from globales import mColor
class Led:
    def __init__(self, strip, idx):
        self.strip = strip
        self.brightness = 0
        self.my_Color = mColor(0, 0, 0)
        self.idx = idx

    def add_brightness(self, brightness, a_color):
        """ brightness comprised between 0 (off) and 1 (on)
        """
        self.my_Color.r += int(a_color.r * brightness)
        self.my_Color.g += int(a_color.g * brightness)
        self.my_Color.b += int(a_color.b * brightness) 
        self.update()

    def rem_brightness(self, brightness, a_color):
        """ brightness comprised between 0 (off) and 1 (on)
        """
        self.my_Color.r -= int(a_color.r * brightness)
        self.my_Color.g -= int(a_color.g * brightness)
        self.my_Color.b -= int(a_color.b * brightness) 
        self.update()

    def update(self):
        if self.my_Color.r < 0:
            self.my_Color.r = 0
        if self.my_Color.g < 0:
            self.my_Color.g = 0
        if self.my_Color.b < 0:
            self.my_Color.b = 0
        r = self.my_Color.r
        g = self.my_Color.g
        b = self.my_Color.b
        self.strip.setPixelColor(self.idx, Color(r, g, b))

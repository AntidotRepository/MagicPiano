from rpi_ws281x import *


class Led:
    def __init__(self, strip, idx):
        self.strip = strip
        self.brightness = 0
        self.r = 0
        self.g = 0
        self.b = 0
        self.idx = idx

    def add_brightness(self, brightness, r, g, b):
        """ brightness comprised between 0 (off) and 1 (on)
        """
        self.r += int(r * brightness)
        self.g += int(g * brightness)
        self.b += int(b * brightness) 
        self.update()

    def rem_brightness(self, brightness, r, g, b):
        """ brightness comprised between 0 (off) and 1 (on)
        """
        self.r -= int(r * brightness)
        self.g -= int(g * brightness)
        self.b -= int(b * brightness) 
        self.update()

    def update(self):
        self.strip.setPixelColor(self.idx, Color(self.r, self.g, self.b))

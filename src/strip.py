from rpi_ws281x import *
from led import Led
import time
from key import Key
import globales

# LED strip configuration:
LED_COUNT      = 200      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Strip:
    def __init__(self):
        # Create the strip
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                            LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
                          
        # Attach LEDs to the strip  
        self.my_leds = list()

        for a_led in range(0, LED_COUNT):
            self.my_leds.append(Led(self.strip, a_led))
        self.strip.begin()

        # Turn off the strip
        for a_led in self.my_leds:
            a_led.update()
        self.strip.show()

        self.my_keys = list()
        # Create keys
        for a_key in globales.keys:
            self.my_keys.append(Key(a_key, self.my_leds))

from rpi_ws281x import *
import time
import random
import math


# LED strip configuration:
LED_COUNT      = 200      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
color_on = Color(50, 10, 10)
color_off = Color(0, 0, 0)

MAX_PIANO_LEDS = 175

N_WHITE_KEYS = 52
N_BLACK_KEYS = 36

LEDS_PER_KEY = 3.3661

white_keys = list()

for a_led in range(0, MAX_PIANO_LEDS):
    strip.setPixelColor(a_led, color_off)

strip.show()


for a_led in range(0, MAX_PIANO_LEDS):
    strip.setPixelColor(a_led, color_off)

i = 0
start = 0
end = 0
inp = ''
for i in range(0, N_WHITE_KEYS):
    inp = ""
    while inp != 'v':
        print("leds:")
        inp = input()

        if inp != 'v':
            w = float(inp)
            end = start + w

            for a_led in range(0, MAX_PIANO_LEDS):
                strip.setPixelColor(a_led, color_off)

            r = (1 - (start % 1) * 0.94) * 50
            strip.setPixelColor(math.floor(start), Color(round(r), 0, 0))

            r = (end % 1) * 0.94 * 50
            strip.setPixelColor(math.floor(end), Color(round(r), 0, 0))

            for j in range(math.ceil(start), math.floor(end)):
                strip.setPixelColor(j, Color(50, 0, 0))
            strip.show()

        if inp == 'v':
            end = start + w
            print("start: {}, w: {}, end: {}".format(start, w, end))
            white_keys.append({"start": start, "end": end})
            start = end

# Store the values in a dict
# After the loop, print the whole dict
print(white_keys)

from rpi_ws281x import *
import time


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


# for i in range(0, MAX_PIANO_LEDS):
#     strip.setPixelColor(i+1, color_on)
#     strip.show()
#     time.sleep(0.001)

inp = ""

start = 0
end = 0

for a_led in range(0, MAX_PIANO_LEDS):
    strip.setPixelColor(a_led, color_off)

keys = list()

while inp is not "e":
    print("cmd:")
    inp = input()
    if inp is "+":
        # Add more leds
        end += 1
    if inp is "-":
        # remove leds
        end -= 1

    print("s = {}".format(start))
    print("e = {}".format(end))

    if inp is " ":
        keys.append((start, end))
        start = end
        end = start
        print("=> start: {}".format(start))
        print("=> end: {}".format(end))

    for a_led in range(0, MAX_PIANO_LEDS):
        strip.setPixelColor(a_led, color_off)
    for a_led in range(start, end):
        strip.setPixelColor(a_led, color_on)
    strip.show()

for e in keys:
    print(e)

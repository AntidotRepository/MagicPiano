from argparse import ArgumentParser
import mido
import time
import math

from rpi_ws281x import *


# LED strip configuration:
LED_COUNT      = 200      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

MIDI_INPUT = 'Alesis Recital:Alesis Recital MIDI 1 20:0'

keys = [
    {'start': 0, 'end': 3.0},        # 1
    3,                               # 2
    {'start': 4.0, 'end': 6.5},      # 3
    {'start': 6.5, 'end': 9.0},      # 4
    9,                               # 5
    {'start': 10.0, 'end': 13.0},    # 6
    13,                              # 7
    {'start': 14.0, 'end': 16.8},    # 8
    {'start': 16.8, 'end': 19.8},    # 9
    19,                              # 10
    {'start': 20, 'end': 23.5},      # 11
    23,                              # 12
    {'start': 24, 'end': 26.5},      # 13
    27,                              # 14
    {'start': 28, 'end': 30.5},      # 15
    {'start': 30.5, 'end': 33.0},    # 16
    33,                              # 17
    {'start': 34.0, 'end': 37.5},    # 18
    37,                              # 19
    {'start': 38, 'end': 41.0},      # 20
    {'start': 41.0, 'end': 43.0},    # 21
    43,                              # 22
    {'start': 44.0, 'end': 47.0},    # 23
    47,                              # 24
    {'start': 48.0, 'end': 51.0},    # 25
    51,                              # 26
    {'start': 52.0, 'end': 54.5},    # 27
    {'start': 54.5, 'end': 57.5},    # 28
    57,                              # 29
    {'start': 58, 'end': 60.5},      # 30
    61,                              # 31
    {'start': 62, 'end': 64.5},      # 32
    {'start': 64.5, 'end': 67.5},    # 33
    67,                              # 34
    {'start': 68, 'end': 71.0},      # 35
    71,                              # 36
    {'start': 72.0, 'end': 74.0},    # 37
    74,                              # 38
    {'start': 75.0, 'end': 77.5},    # 39
    {'start': 77.5, 'end': 80.5},    # 40
    80,                              # 41
    {'start': 81, 'end': 83.5},      # 42
    84,                              # 43
    {'start': 85, 'end': 87.5},      # 44
    {'start': 87.5, 'end': 90.5},    # 45
    90,                              # 46
    {'start': 91, 'end': 94.5},      # 47
    94,                              # 48
    {'start': 95, 'end': 97.5},      # 49
    98,                              # 50
    {'start': 99, 'end': 101.5},     # 51
    {'start': 101.5, 'end': 104.5},  # 52
    104,                             # 53
    {'start': 105, 'end': 107.5},    # 54
    108,                             # 55
    {'start': 109, 'end': 111.5},    # 56
    {'start': 111.5, 'end': 114.5},  # 57
    114,                             # 58
    {'start': 115, 'end': 117.5},    # 59
    118,                             # 60
    {'start': 119, 'end': 121.5},    # 61
    122,                             # 62
    {'start': 123, 'end': 124.5},    # 63
    {'start': 124.5, 'end': 128.5},  # 64
    128,                             # 65
    {'start': 129, 'end': 132.0},    # 66
    132,                             # 67
    {'start': 133, 'end': 135.5},    # 68
    {'start': 135.5, 'end': 138.0},  # 69
    138,                             # 70
    {'start': 139.0, 'end': 142.0},  # 71
    142,                             # 72
    {'start': 143.0, 'end': 144.5},  # 73
    145,                             # 74
    {'start': 146, 'end': 148.5},    # 75
    {'start': 148.5, 'end': 151},    # 76
    151,                             # 77
    {'start': 152, 'end': 155.5},    # 78
    155,                             # 79
    {'start': 156, 'end': 158.5},    # 80
    {'start': 158.5, 'end': 161.5},  # 81
    161,                             # 82
    {'start': 162, 'end': 165.0},    # 83
    165,                             # 84
    {'start': 166.0, 'end': 169.0},  # 85
    169,                             # 86
    {'start': 170.0, 'end': 173.0},  # 87
    {'start': 173.0, 'end': 176.0}]  # 88



# 175 leds used
# 1st midi note: 21
# Last midi note: 108

MAX_PIANO_LEDS = 175
MIDI_1 = 21
MIDI_LAST = 108

LEDS_PER_NOTE = MAX_PIANO_LEDS / (MIDI_LAST - MIDI_1)


def turn_on(key):
    a_key = keys[key]
    if isinstance(a_key, dict):
        a_key = keys[key]
        start = a_key["start"]
        end = a_key["end"]
        for j in range(math.ceil(start), math.floor(end)):
            strip.setPixelColor(j, Color(50, 0, 0))
    else:
        strip.setPixelColor(a_key, Color(0, 50, 0))


def turn_off(key):
    a_key = keys[key]
    if isinstance(a_key, dict):
        start = a_key["start"]
        end = a_key["end"]
        for j in range(math.ceil(start), math.floor(end)):
            strip.setPixelColor(j, Color(0, 0, 0))
    else:
        strip.setPixelColor(a_key, Color(0, 0, 0))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode",
                        help="Playing mode:\n\
    - 0: Piano plays automatically\n\
    - 1: Piano waits for you to press the correct key\n\
    - 2: Piano waits for you to press and release the correct key\n\
    - 3: Piano doesn't wait for you")
    parser.add_argument("-f", "--file", dest="file", help="Midi file to play.")
    parser.add_argument("-s", "--speed", dest="speed", help="Speed of lecture",
                        default=1, type=float)
    args = parser.parse_args()
    print(args.file)

    mid = mido.MidiFile(args.file)
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                              LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    color_on = Color(50, 10, 10)
    color_off = Color(0, 0, 0)

    if args.mode == "0":
        with mido.open_output(MIDI_INPUT) as outport:
            t0 = time.time()
            for msg in mid:
                if not msg.is_meta:
                    t = msg.time - (time.time() - t0)
                    t0 = time.time()
                    print(msg.time)
                    print(t)
                    if t < 0:
                        t = 0
                    time.sleep(t / args.speed)
                    outport.send(msg)
                    if not msg.is_meta:
                        # if msg.type == 'note_on' or msg.type == 'note_off':
                        #     print("wait {}s".format(msg.time))
                        #     time.sleep(msg.time * args.speed)
                        # print(msg.type)
                        if msg.type == 'note_on':
                            key = msg.note - 21
                            print("{}: ON".format(key))
                            turn_on(key)
                        elif msg.type == 'note_off':
                            key = msg.note - 21
                            print("{}: OFF".format(key))
                            turn_off(key)

                        if msg.type == 'note_on' or msg.type == 'note_off':
                            strip.show()

    if args.mode == "1":
        notes_to_press = list()
        with mido.open_input(MIDI_INPUT) as inport:
            # for msg in mid:
            #     if not msg.is_meta:
            #         if msg.type == 'note_on' and msg.time < 0.01:
            #             # On store la note mais on ne bloque pas
            #             notes_to_press.append(msg.note)
            #             key = msg.note - 21
            #             print("{}: ON, time: {}".format(msg.note, msg.time))
            #             turn_on(key)
            #         elif msg.type == 'note_on' and msg.time > 0.01:
            #             # On bloque, on attend les notes et ensuite on store
            #             print(notes_to_press)
            #             while len(notes_to_press) > 0:
            #                 print("===============")
            #                 my_key = inport.receive()
            #                 print("You pressed: {}".format(my_key))
            #                 if my_key.note in notes_to_press and my_key.velocity != 0:
            #                     notes_to_press.remove(my_key.note)
            #                     print("Good key: {}".format(my_key.note))
            #             notes_to_press.append(msg.note)
            #             key = msg.note - 21
            #             print("after loop")
            #             print("{}: ON, time: {}".format(msg.note, msg.time))
            #             turn_on(key)
            #         elif msg.type == 'note_off' and msg.time < 0.01:
            #             key = msg.note - 21
            #             print("{}: OFF, time: {}".format(msg.note, msg.time))
            #             turn_off(key)

            #         strip.show()
            for msg in mid:
                if not msg.is_meta:
                    if msg.time > 0.2:
                        print("notes_to_press {}".format(msg.note))
                        while len(notes_to_press) > 0:
                            pressed = inport.receive()
                            print("You pressed {}".format(pressed))
                            if pressed.note in notes_to_press and pressed.velocity != 0:
                                notes_to_press.remove(pressed.note)
                                print("Removed {}".format(pressed.note))
                                turn_off(pressed.note - 21)

                    if msg.type == 'note_on':
                        notes_to_press.append(msg.note)
                        key = msg.note - 21
                        turn_on(key)

                    if msg.type == 'note_off':
                        key = msg.note - 21
                        turn_off(key)

                    strip.show()
    if args.mode == "2":
        with mido.open_input(MIDI_INPUT) as inport:
            for msg in mid:
                if not msg.is_meta:
                    if msg.type == 'note_on' or msg.type == 'note_off':
                        print("wait {}s".format(msg.time))
                        # time.sleep(msg.time * )
                    # print(msg.type)
                    if msg.type == 'note_on':
                        key = msg.note - 21
                        print("{}: ON".format(key))
                        turn_on(key)
                    elif msg.type == 'note_off':
                        key = msg.note - 21
                        print("{}: OFF".format(key))
                        turn_off(key)

                    if msg.type == 'note_on' or msg.type == 'note_off':
                        strip.show()
                        wrong_key = True
                        while wrong_key is True:
                            my_key = inport.receive()
                            print("Press {}".format(msg.note))
                            print("You pressed: {}".format(my_key))
                            if my_key.note == msg.note:
                                wrong_key = False
                                print("Good key")

    if args.mode == "3":
        with mido.open_input(MIDI_INPUT) as inport:
            for msg in mid:
                if not msg.is_meta:
                    if msg.type == 'note_on' or msg.type == 'note_off':
                        print("wait {}s".format(msg.time))
                        time.sleep(msg.time / args.speed)
                    # print(msg.type)
                    if msg.type == 'note_on':
                        key = msg.note - 21
                        print("{}: ON".format(key))
                        turn_on(key)
                    elif msg.type == 'note_off':
                        key = msg.note - 21
                        print("{}: OFF".format(key))
                        turn_off(key)

                    if msg.type == 'note_on' or msg.type == 'note_off':
                        strip.show()
                        # wrong_key = True
                        # while wrong_key is True:
                            # my_key = inport.receive()
                            # print("Press {}".format(msg.note))
                            # print("You pressed: {}".format(my_key))
                            # if my_key.note == msg.note:
                            #     wrong_key = False
                            #     print("Good key")
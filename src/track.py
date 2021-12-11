import mido
import time
from random import randrange

import observable

class Track():
    def __init__(self, a_strip, a_keys, a_track, ticks_per_beat, tempo, outport):
        self.my_strip = a_strip
        self.my_keys = a_keys
        self.my_track = a_track
        self.my_ticks_per_beat = ticks_per_beat
        self.my_tempo = tempo
        self.outport = outport

        self.r = randrange(255)
        self.g = randrange(255)
        self.b = randrange(255)

        print("New track: {}".format(self.my_track.name))

    def play(self):
        for a_msg in self.my_track:
            print(self.my_track.name)
            if not a_msg.is_meta:
                self.outport.send(a_msg)
            if a_msg.is_meta:
                if a_msg.type == "set_tempo":
                    self.my_tempo.set(a_msg.tempo)
            elif a_msg.type == "control_change":
                # if a_msg.control == 7:
                #     Volume = a_msg.value
                # Can be used for the pedal!!!
                # channel - control - value
                # print(msg)

                pass
                # Example
                # control_change channel=0 control=64 value=127 time=0.17164171666666664
            elif a_msg.type == "program_change":
                # channel - program
                # print(msg)
                pass
                # Example
                # program_change channel=0 program=0 time=0
            elif a_msg.type == "note_on":
                # channel - note - velocity
                # print(a_msg)
                # print("time: {}".format(msg.time))
                # print("ticks_per_beat: {}".format(mid.ticks_per_beat))
                # print("tempo: {}".format(tempo))
                try:
                    self.my_strip.my_keys[a_msg.note-21].light_on(self.r, self.g, self.b)
                except IndexError:
                    print("Index out of range: {}".format(a_msg.note))
                # Example
                # note_on channel=0 note=37 velocity=33 time=0
                # note_on channel=0 note=44 velocity=26 time=0.07142853333333334
            elif a_msg.type == "note_off":
                # channel - note - velocity
                # print(msg)
                pass
                # Example
                # note_off channel=0 note=37 velocity=0 time=0
                # note_off channel=0 note=77 velocity=0 time=0.048076916666666664
                try:
                    self.my_strip.my_keys[a_msg.note-21].light_off(self.r, self.g, self.b)
                except IndexError:
                    print("Index out of range: {}".format(a_msg.note))
            else:
                print("Unexpected type: {}".format(a_msg.type))
            self.my_strip.strip.show()
            # print("{}: {}".format(self.my_track.name, self.my_tempo.get()))
            time_to_sleep = mido.tick2second(a_msg.time, self.my_ticks_per_beat, self.my_tempo.get())
            # print(time_to_sleep)
            time.sleep(time_to_sleep)

import mido
import time
from random import randrange
from globales import mColor

import observable

class Track():
    def __init__(self, a_strip, a_keys, a_track, ticks_per_beat, tempo, outport):
        self.my_strip = a_strip
        self.my_keys = a_keys
        self.my_track = a_track
        self.my_ticks_per_beat = ticks_per_beat
        self.my_tempo = tempo
        self.outport = outport

        if self.my_track.name == "Right":
            self.color_w = mColor(0, 255, 0)
            self.color_b = mColor(255, 0, 255)
        elif self.my_track.name == "Left":
            self.color_w = mColor(255, 0, 0)
            self.color_b = mColor(0, 255, 255)

        print("New track: {}".format(self.my_track.name))

    def play(self, t0):
        for a_msg in self.my_track:
            
            # Timing management
            t0 += mido.tick2second(a_msg.time, self.my_ticks_per_beat, self.my_tempo.get())
            
            to_sleep = t0 - time.time()
            if to_sleep > 0:
                time.sleep(to_sleep)
            if not a_msg.is_meta:
                self.outport.send(a_msg)
            if a_msg.is_meta:
                if a_msg.type == "set_tempo":
                    self.my_tempo.set(a_msg.tempo)
            elif a_msg.type == "control_change":
                # Can be used for the pedal!!!
                # Example
                # control_change channel=0 control=64 value=127 time=0.17164171666666664
                pass
            elif a_msg.type == "program_change":
                # Example
                # program_change channel=0 program=0 time=0
                pass
            elif a_msg.type == "note_on":
                # Example
                # note_on channel=0 note=37 velocity=33 time=0
                # note_on channel=0 note=44 velocity=26 time=0.07142853333333334
                try:
                    # Some midi files use a "note_on" with velocity at 0 to say "note_off"
                    if a_msg.velocity != 0:
                        # If velocity is not 0, it's note on
                        self.press_key(a_msg.note)
                    else:
                        # If velocity is 0, it's note off.
                        self.release_key(a_msg.note)
                except IndexError:
                    print("Index out of range: {}".format(a_msg.note))
            elif a_msg.type == "note_off":
                # Example
                # note_off channel=0 note=37 velocity=0 time=0
                # note_off channel=0 note=77 velocity=0 time=0.048076916666666664
                try:
                    self.release_key(a_msg.note)
                except IndexError:
                    print("Index out of range: {}".format(a_msg.note))
            else:
                print("Unexpected type: {}".format(a_msg.type))
            self.my_strip.strip.show()

    def press_key(self, idx):
        idx -= 21
        print("track: {}".format(type(self.color_w)))
        self.my_strip.my_keys[idx].light_on(self.color_w)

    def press_w_key(self):
        pass

    def press_b_key(self):
        pass

    def release_key(self, idx):
        idx -= 21
        self.my_strip.my_keys[idx].light_off(self.color_w)

    def release_w_key(self):
        pass

    def release_b_key(self):
        pass

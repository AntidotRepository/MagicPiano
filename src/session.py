from globales import mColor
import mido
import time
from message import Message
from strip import Strip


MIDI_INPUT = 'Alesis Recital:Alesis Recital MIDI 1 20:0'

class Session():
    def __init__(self, a_midi_file):
        self.midi_file = a_midi_file
        self.color_rw = mColor(0, 255, 0)
        self.color_rb = mColor(255, 0, 255)
        self.color_lw = mColor(255, 0, 0)
        self.color_lb = mColor(0, 255, 255)

        # Create the strip
        self.my_strip = Strip()

        # preprocessing
        self.msgs = list()
        id_track = 0
        time_track = 0
        for a_track in self.midi_file.tracks:
            print(a_track.name)
            for a_msg in a_track:
                time_track += a_msg.time
                self.msgs.append(Message(id_track, a_msg, time_track))
            id_track += 1
            time_track = 0  # Reset time for next rack

        self.msgs.sort(key=lambda x: x.time)

        print("{} messages to play!".format(len(self.msgs)))


    def press_key(self, msg):
        msg.msg.note -= 21
        a_key = self.my_strip.my_keys[msg.msg.note]
        if a_key.is_white:
            if msg.id_track == 0:
                a_key.light_on(self.color_rw)
            elif msg.id_track == 1:
                a_key.light_on(self.color_lw)
        else:
            if msg.id_track == 0:
                a_key.light_on(self.color_rb)
            elif msg.id_track == 1:
                a_key.light_on(self.color_lb)

    def release_key(self, msg):
        msg.msg.note -= 21
        a_key = self.my_strip.my_keys[msg.msg.note]
        if a_key.is_white:
            if msg.id_track == 0:
                a_key.light_off(self.color_rw)
            elif msg.id_track == 1:
                a_key.light_off(self.color_lw)
        else:
            if msg.id_track == 0:
                a_key.light_off(self.color_rb)
            elif msg.id_track == 1:
                a_key.light_off(self.color_lb)

    def play(self):
        # Midi output
        with mido.open_output(MIDI_INPUT) as outport:
            t0 = time.time()
            my_ticks_per_beat = self.midi_file.ticks_per_beat
            my_tempo = 833333 # default tempo value
            # for a_msg in msgs[2100:]:
            for i in range(0, len(self.msgs)):
                a_msg = self.msgs[i]
                if i == 0:
                    ticks = a_msg.time
                else:
                    ticks = a_msg.time - self.msgs[i-1].time
                t0 += mido.tick2second(ticks, my_ticks_per_beat, my_tempo)
                time_to_sleep = t0 - time.time()
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
                if not a_msg.msg.is_meta:
                    outport.send(a_msg.msg)
                if a_msg.msg.type == "set_tempo":
                    my_tempo = a_msg.msg.tempo
                elif a_msg.msg.type == "note_on":
                    if a_msg.msg.velocity != 0:
                        self.press_key(a_msg)
                    else:
                        self.release_key(a_msg)
                elif a_msg.msg.type == "note_off":
                    self.release_key(a_msg)
                self.my_strip.strip.show()
from argparse import ArgumentParser
import argparse
import mido
import threading
import time
from track import Track

from rpi_ws281x import *
from observable import Observable
from strip import Strip
from message import Message

MIDI_INPUT = 'Alesis Recital:Alesis Recital MIDI 1 20:0'


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

    my_keys = list()

    # Create the strip
    my_strip = Strip()

    # Contains our midi file
    midi_file = mido.MidiFile(args.file)

    tempo = Observable(0)

    tracks = list()

    # Preprocessing step
        # Go through the midi file and put in a list each message
        # Each message would have the "trackID" (quelle main), timestamp,
        # la note, relachée ou pressée...
    
    msgs = list()
    id_track = 0
    time_track = 0
    for a_track in midi_file.tracks:
        print(a_track.name)
        for a_msg in a_track:
            time_track += a_msg.time
            msgs.append(Message(id_track, a_msg, time_track))
        id_track += 1
        time_track = 0  # Reset time for next rack

    msgs.sort(key=lambda x: x.time)

    print("{} messages to play!".format(len(msgs)))

    # Midi output
    with mido.open_output(MIDI_INPUT) as outport:
        t0 = time.time()
        my_ticks_per_beat = midi_file.ticks_per_beat
        my_tempo = 833333 # default tempo value
        # for a_msg in msgs[2100:]:
        for i in range(0, len(msgs)):
            a_msg = msgs[i]
            if i == 0:
                ticks = a_msg.time
            else:
                ticks = a_msg.time - msgs[i-1].time
            t0 += mido.tick2second(ticks, my_ticks_per_beat, my_tempo)
            time_to_sleep = t0 - time.time()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            if not a_msg.msg.is_meta:
                outport.send(a_msg.msg)
            if a_msg.msg.type == "set_tempo":
                my_tempo = a_msg.msg.tempo


    # Midi output
    # with mido.open_output(MIDI_INPUT) as outport:
    #     # Load the midi tracks from the midi file
    #     for a_track in midi_file.tracks:
    #         a_track = Track(my_strip, my_keys, a_track, midi_file.ticks_per_beat, tempo, outport)
    #         tracks.append(a_track)
    #     # Despite what the doc seems to say, time is in sec!
    #     # print(mid)
    #     threads = list()
    #     t0 = time.time()
    #     for a_track in tracks:
    #         # Start a thread per track
    #         a_thread = threading.Thread(target=a_track.play, args=(t0,),daemon=True)
    #         a_thread.start()
    #         threads.append(a_thread)

    #     for a_thread in threads:
    #         a_thread.join()


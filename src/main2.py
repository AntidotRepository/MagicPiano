from argparse import ArgumentParser
import argparse
import mido
import threading
import time
from track import Track

from rpi_ws281x import *
from observable import Observable
from strip import Strip

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

    # Midi output
    with mido.open_output(MIDI_INPUT) as outport:
        # Load the midi tracks from the midi file
        for a_track in midi_file.tracks:
            a_track = Track(my_strip, my_keys, a_track, midi_file.ticks_per_beat, tempo, outport)
            tracks.append(a_track)
        # Despite what the doc seems to say, time is in sec!
        # print(mid)
        threads = list()
        for a_track in tracks:
            # Start a thread per track
            a_thread = threading.Thread(target=a_track.play, daemon=True)
            a_thread.start()
            threads.append(a_thread)

        for a_thread in threads:
            a_thread.join()


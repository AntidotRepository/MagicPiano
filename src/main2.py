from argparse import ArgumentParser
import argparse
import mido
from session import Session



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

    # Contains our midi file
    midi_file = mido.MidiFile(args.file)

    mySession = Session(midi_file)
    if args.mode == '0':
        mySession.play()
    elif args.mode == '1':
        mySession.train()

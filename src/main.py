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
    - 2: Piano only tells you when you're wrong and restart from the beginning (deathmode)\n\
    - 3: Free play mode")
    parser.add_argument("-f", "--file", dest="file", help="Midi file to play.")
    parser.add_argument("-s", "--speed", dest="speed", help="Speed of lecture",
                        default=1, type=float)
    parser.add_argument("-t", "--track", dest="track", help="Which hand to play.",
                        default='b')
    args = parser.parse_args()
    print(args.file)

    my_keys = list()

    # Contains our midi file
    midi_file = mido.MidiFile(args.file)

    mySession = Session(midi_file, args.track)
    if args.mode == '0':
        mySession.play()
    elif args.mode == '1':
        mySession.train()
    elif args.mode == '2':
        mySession.death_mode()
    elif args.mode == '3':
        mySession.free_play()
        
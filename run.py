from hashlib import new
from piano_type import PianoType
from midi_stream import open_midistream
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', required=True)
parser.add_argument("--debug", action='store_true')

parser_run = subparsers.add_parser('run')
parser_run.add_argument("--layout")

parser_layout = subparsers.add_parser('layout')
parser_layout.add_argument("--input")
parser_layout.add_argument("--output")

args = parser.parse_args()

if __name__ == "__main__":
  import asyncio

  loop = asyncio.new_event_loop()

  pianotype = PianoType(
    debug=args.debug,
  )
  midistream = loop.run_until_complete(open_midistream())

  if args.command == "run":
    pianotype.load_layout(args.layout)
    try:
      loop.run_until_complete(pianotype.run(midistream))
    except:
      midistream.close()
  elif args.command == "layout":
    if args.input:
      pianotype.load_layout(args.input)
    try:
      loop.run_until_complete(pianotype.mode_setting(midistream))
    except:
      ...
    path = None
    if args.output:
      path = args.output
    elif args.input and input("Do you want to overwrite and save?(y/n): ").lower() == "y":
      path = args.input
    else:
      while True:
        path = input("Save in: ")
        if input(f"Is it OK to save to {path}?(y/n): ").lower() == "y":
          break
    pianotype.save_layout(path)

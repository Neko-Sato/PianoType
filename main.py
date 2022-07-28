import argparse
import piano_type

version = "0.0.5"
print('\033[32m'+"PianoType "+version+" is running!"+'\033[0m')

parser = argparse.ArgumentParser()
parser.add_argument("--device", action='store_true')
parser.add_argument("--input", type=int)
parser.add_argument("--debug", action='store_true')

if __name__ == "__main__":
  args = parser.parse_args()
  if args.device:
    piano_type.get_input_midi_devices()
  else:
    pianotype = piano_type.PianoType(
      debug=args.debug,
    )
    pianotype.run(
      input=args.input,
    )
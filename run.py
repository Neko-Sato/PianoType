import argparse
import piano_type

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true')

if __name__ == "__main__":
  args = parser.parse_args()
  pianotype = piano_type.PianoType(
    debug=args.debug,
  )
  pianotype.run(
  )
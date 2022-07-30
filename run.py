from piano_type import PianoType
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true')

args = parser.parse_args()

if __name__ == "__main__":
  import asyncio
  
  pianotype = PianoType(
    debug=args.debug,
  )
  pianotype.load_layout()
  try:
    asyncio.run(pianotype.run())
  except KeyboardInterrupt:
    ...
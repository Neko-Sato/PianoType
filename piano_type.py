import asyncio
import json
import os.path

from midi_stream import MIDIStream

from sys import platform
if platform == "win32":
  from operation.windows import keyAction, mouseMove 
elif platform == 'darwin':
  from operation.darwin import keyAction, mouseMove 
else:
  print("not support.")
  exit()
del platform

from midi_to_ansi_note import midi_to_ansi_note

class PianoType:
  version = "0.0.5"
  default_layoutfile_path = os.path.join(os.path.dirname(__file__), "layout.json")
  def __init__(self, debug=False, layoutfile_path=default_layoutfile_path):
    self.__config_file = open(layoutfile_path, 'r')
    self.__config = json.load(self.__config_file)
    self.debug = debug
  async def converter(self, midi_stream):
    async for event in midi_stream:
      self.debug and print(event)
      status = int(event[0]/16)*16
      if status == 176:
        key = self.__config["modulation"].get(str(event[1]))
        if key is None:
          continue
        if key in ["mouse_x", "mouse_y"]:
          if event[2] < 127*1/3:
            rate = int(((3/127)*event[2]-1))
          elif 127*2/3 < event.data2:
            rate = int(((3/127)*event[2]-2))
          else:
            continue
          self.__control(key, rate)
        else:
          self.__switch(key, event[2] != 0)
      elif status in [144, 128]: 
        note = midi_to_ansi_note(event[1])
        key = self.__config["note"].get(note)
        if key is None:
          continue
        self.__switch(key, not(status == 128 or event[2] == 0))

  def __control(self, key, rate):
    if key == "mouse_x":
      mouseMove(xOffset=self.__config["speed"]*rate)
    elif key == "mouse_y":
      mouseMove(yOffset=self.__config["speed"]*-rate)

  def __switch(self, key, isOn):
    keyAction(key, isOn)
    # if key == "click_left":
    #   ...
    # elif key == "click_right":
    #   ...
    # else:
    #   keyAction(key, isOn)

  def run(self):
    print('\033[32m'+"PianoType "+self.version+" is running!"+'\033[0m')
    self.loop = asyncio.new_event_loop()
    midi_stream = MIDIStream(loop=self.loop)
    try:
      self.loop.run_until_complete(self.converter(midi_stream))
    except KeyboardInterrupt:
      ...
    print("Close...")
    midi_stream.close()
    self.loop.close()
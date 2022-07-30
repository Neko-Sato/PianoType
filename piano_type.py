import asyncio
import json
import os.path

from midi_stream import open_midistream

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
    self.load_layout(layoutfile_path)
    self.debug = debug
  def load_layout(self, layoutfile_path):
    self.__config_file = open(layoutfile_path, 'r')
    self.__config = json.load(self.__config_file)
  async def converter(self, event):
    status = int(event[0]/16)*16
    if status == 176:
      key = self.__config["modulation"].get(str(event[1]))
      if key is None:
        return
      if key in ["mouse_x", "mouse_y"]:
        if event[2] < 127*1/3:
          rate = (3/127)*event[2]-1
        elif 127*2/3 < event[2]:
          rate = (3/127)*event[2]-2
        else:
          return
        rate *= self.__config["speed"]
        self.debug and print(f"modulation : {event[1]} -> {key} :{rate}")
        self.__control(key, rate)
      else:
        isDown = event[2] != 0
        self.debug and print(f"modulation : {event[1]} -> {key} : {'Down' if isDown else 'Up'}")
        self.__switch(key, isDown)
    elif status in [144, 128]: 
      note = midi_to_ansi_note(event[1])
      key = self.__config["note"].get(note)
      if key is None:
        return
      isDown = not(status == 128 or event[2] == 0)
      self.debug and print(f"{note} : {'Down' if isDown else 'Up'} -> {key} : {'Down' if isDown else 'Up'}")
      self.__switch(key, isDown)

  def __control(self, key, rate):
    if key == "mouse_x":
      mouseMove(xOffset=int(rate))
    elif key == "mouse_y":
      mouseMove(yOffset=int(-rate))

  def __switch(self, key, isOn):
    keyAction(key, isOn)
    # if key == "click_left":
    #   ...
    # elif key == "click_right":
    #   ...
    # else:
    #   keyAction(key, isOn)

  async def __run(self):
    print('\033[32m'+"PianoType "+self.version+" is running!"+'\033[0m')
    midi_stream = await open_midistream()
    try:
      async for event in midi_stream:
        asyncio.ensure_future(self.converter(event))
    except KeyboardInterrupt:
      ...
    print("Close...")
    midi_stream.close()    

  def run(self):
    loop = asyncio.new_event_loop()
    try:
      loop.run_until_complete(self.__run())
    except KeyboardInterrupt:
      ...
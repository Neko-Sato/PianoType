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
  def __init__(self, debug=False):
    self.init_layout()
    self.debug = debug
  def init_layout(self):
    self.__config = {}
    self.__config.setdefault("speed", 10)
    self.__config.setdefault("modulation", {})
    self.__config.setdefault("note", {})
  def load_layout(self, layoutfile_path=default_layoutfile_path):
    with open(layoutfile_path, 'r') as file:
      self.__config = json.load(file)
  def save_layout(self, layoutfile_path):
    with open(layoutfile_path, 'w') as file:
      json.dump(self.__config, file, indent=2)
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

  # async def mode_setting(self, *args, **kwargs):
  #   midi_stream = await open_midistream(*args, **kwargs)
  #   while True:
  #     # await midi_stream.clear()
  #     event = await anext(midi_stream)
  #     status = int(event[0]/16)*16
  #     if status == 176:
  #       print(f"modulation : {event[1]} -> {self.__config['modulation'].get(str(event[1]), 'None')}")
  #       key = input(">>")
  #       if key != "":
  #         self.__config["modulation"][str(event[1])] = key
  #     elif not(status == 128 or event[2] == 0):
  #       note = midi_to_ansi_note(event[1])
  #       print(f"note : {note} -> {self.__config['note'].get(note, 'None')}")
  #       key = input(f">>")
  #       if key != "":
  #         self.__config["note"][note] = key
      
  async def run(self, *args, **kwargs):
    print('\033[32m'+"PianoType "+self.version+" is running!"+'\033[0m')
    midi_stream = await open_midistream(*args, **kwargs)
    try:
      async for event in midi_stream:
        asyncio.ensure_future(self.converter(event))
    except KeyboardInterrupt:
      ...
    print("Close...")
    midi_stream.close()
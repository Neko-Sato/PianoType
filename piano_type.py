import asyncio
import json
import pygame.midi as midi
from sys import platform

if platform == "win32":
  from operation.windows import keyAction, mouseMove 
elif platform == 'darwin':
  from operation.darwin import keyAction, mouseMove 
else:
  print("not support.")
  exit()

midi.init()

class MIDIStream:
  def __init__(self, input_id, num_events=10):
    assert midi.get_init()
    self.__input = midi.Input(input_id)
    self.num_events = num_events
  async def __aiter__(self):
    while True:
      try:
        if self.__input.poll():
          data = self.__input.read(self.num_events)
          for event in midi.midis2events(data, self.__input.device_id):
            yield event
        await asyncio.sleep(0.1)
      except midi.MidiException:
        print("MIDI device is closed.")
        break
  def close(self):
    self.__input.close()

def get_input_midi_devices():
  for i in range(midi.get_count()):
    _, name, input, _, _ = midi.get_device_info(i)
    if input == 1:
      print(f"[{i}] {name.decode()}")

class PianoType:
  def __init__(self, debug=False, layoutfile_path="layout.json"):
    self.__config_file = open(layoutfile_path, 'r')
    self.__config = json.load(self.__config_file)
    self.debug = debug
  async def converter(self, midi_stream):
    async for event in midi_stream:
      self.debug and print(event)
      status = int(event.status/16)*16
      if status == 176:
        key = self.__config["modulation"].get(str(event.data1))
        if key is None:
          continue
        if key in ["mouse_x", "mouse_y"]:
          if event.data2 < 127*1/3:
            rate = int(((3/127)*event.data2-1))
          elif 127*2/3 < event.data2:
            rate = int(((3/127)*event.data2-2))
          else:
            continue
          self.__control(key, rate)
        else:
          self.__switch(key, event.data2 != 0)
      elif status in [144, 128]: 
        note = midi.midi_to_ansi_note(event.data1)
        key = self.__config["note"].get(note)
        if key is None:
          continue
        self.__switch(key, not(status == 128 or event.data2 == 0))

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

  def run(self, input=None):
    _input = input if input is not None else midi.get_default_input_id()
    midi_stream = MIDIStream(_input)
    self.loop = asyncio.new_event_loop()
    try:
      self.loop.run_until_complete(self.converter(midi_stream))
    except KeyboardInterrupt:
      print("Close...")
      midi_stream.close()
    self.loop.close()
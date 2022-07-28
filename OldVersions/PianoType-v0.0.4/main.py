import asyncio
import platform
import pygame.midi as midi

pf = platform.system()

version = "0.0.4"

if pf == "Windows":
  from dict_constant_win import *
  import ctypes

  def mouseMove(xOffset=0, yOffset=0):
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, xOffset, yOffset, 0, 0)

  def keyDown(key):
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYDOWN, 0)
  
  def keyUp(key):
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)

elif pf == 'Darwin':
  from dict_constant_macos import *
  import Quartz
  import AppKit

  def mouseMove(xOffset=0, yOffset=0):
    loc = AppKit.NSEvent.mouseLocation()
    x, y = int(loc.x) + xOffset, int(Quartz.CGDisplayPixelsHigh(0) - loc.y) + yOffset
    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

  def keyDown(key):
    print(key)
    event = Quartz.CGEventCreateKeyboardEvent(None, key, True)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

  def keyUp(key):
    print(key)
    event = Quartz.CGEventCreateKeyboardEvent(None, key, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

else:
  exit()

print('\033[32m'+"PianoType "+version+" is running!"+'\033[0m')

##############################################################################

speed = 16

note2key = {
  #母音
  "C5": VirtualKeyCodes["A"],
  "D5": VirtualKeyCodes["I"],
  "E5": VirtualKeyCodes["U"],
  "F5": VirtualKeyCodes["E"],
  "G5": VirtualKeyCodes["O"],
  #外来子音
  "C#3": VirtualKeyCodes["V"],
  "D3": VirtualKeyCodes["F"],
  "D#3": VirtualKeyCodes["C"],
  "E3": VirtualKeyCodes["X"],
  "F#3": VirtualKeyCodes["Q"],
  "G3": VirtualKeyCodes["L"],
  "G#3": VirtualKeyCodes["J"],
  #半母音
  "A#3": VirtualKeyCodes["W"],
  "B3": VirtualKeyCodes["Y"],
  #子音
  "C4": VirtualKeyCodes["M"],
  "C#4": VirtualKeyCodes["B"],
  "D4": VirtualKeyCodes["H"],
  "D#4": VirtualKeyCodes["P"],
  "E4": VirtualKeyCodes["N"],
  "F4": VirtualKeyCodes["R"],
  "F#4": VirtualKeyCodes["D"],
  "G4": VirtualKeyCodes["T"],
  "G#4": VirtualKeyCodes["Z"],
  "A4": VirtualKeyCodes["S"],
  "A#4": VirtualKeyCodes["G"],
  "B4": VirtualKeyCodes["K"],
  #記号
  # "C#5": "!",
  "D#5": VirtualKeyCodes["/"],
  "G#5": VirtualKeyCodes[","],
  "A#5": VirtualKeyCodes["."],
  "F#5" : VirtualKeyCodes["-"],

  #数字
  "C2": VirtualKeyCodes["1"],
  "D2": VirtualKeyCodes["2"],
  "E2": VirtualKeyCodes["3"],
  "F2": VirtualKeyCodes["4"],
  "G2": VirtualKeyCodes["5"],
  "A2": VirtualKeyCodes["6"],
  "B2": VirtualKeyCodes["7"],
  "F#2": VirtualKeyCodes["8"],
  "G#2": VirtualKeyCodes["9"],
  "A#2": VirtualKeyCodes["0"],
  #機能キー
  "A5": VirtualKeyCodes["Space"],
  "B5": VirtualKeyCodes["Backspace"],
  "C6": VirtualKeyCodes["Enter"],
  "D6": VirtualKeyCodes["Shift"],
  "C#6": VirtualKeyCodes["eisu"],
  "D#6": VirtualKeyCodes["kana"],
}

async def midi_stream(input_midi, num_events=10):
  while True:
    try:
      if input_midi.poll():
        data = input_midi.read(num_events)
        for event in midi.midis2events(data, input_midi.device_id):
          yield event
      await asyncio.sleep(0.1)
    except midi.MidiException: 
      break

async def converter(midi_input):
  async for event in midi_stream(midi_input):
    print(event)
    number = int(event.status/16)*16
    if number == 176: 
      if event.data1 == 1: #x軸のマウス操作
        if event.data2 < 127*1/3:
          offset = int(speed*((3/127)*event.data2-1))
          mouseMove(xOffset=offset)
        elif 127*2/3 < event.data2:
          offset = int(speed*((3/127)*event.data2-2))
          mouseMove(xOffset=offset)
      elif event.data1 == 77: #y軸のマウス操作
        if 127-event.data2 < 127*1/3:
          offset = int(speed*((3/127)*(127-event.data2)-1))
          mouseMove(yOffset=offset)
        elif 127*2/3 < 127-event.data2:
          offset = int(speed*((3/127)*(127-event.data2)-2))
          mouseMove(yOffset=offset)

      elif event.data1 == 64: #Shiftキー
        if event.data2 != 0:
          keyDown(VirtualKeyCodes["Shift"])
        else:
          keyUp(VirtualKeyCodes["Shift"])

    elif number == 144: #キーボード押す
      key = note2key.get(midi.midi_to_ansi_note(event.data1))
      if key is not None:
        keyDown(key)
    elif number == 128: #キーボード離す
      key = note2key.get(midi.midi_to_ansi_note(event.data1))
      if key is not None:
        keyUp(key)

def main():
  midi.init()
  input_id = midi.get_default_input_id()
  midi_input = midi.Input(input_id)

  loop = asyncio.new_event_loop()
  try:
    loop.run_until_complete(converter(midi_input))
  except KeyboardInterrupt:
    midi_input.close()

if __name__ == "__main__":
  main()
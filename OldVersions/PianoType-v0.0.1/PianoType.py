import asyncio
import pyautogui as gui
import pygame.midi as midi

speed = 1

note2key = {
  #母音
  "C5": "u",
  "D5": "o",
  "E5": "a",
  "F5": "e",
  "G5": "i",
  #外来子音
  "C#3": "v",
  "D3": "f",
  "D#3": "c",
  "E3": "x",
  "F#3": "q",
  "G3": "l",
  #半母音
  "A#3": "w",
  "B3": "y",
  #子音
  "C4": "m",
  "C#4": "b",
  "D4": "h",
  "D#4": "p",
  "E4": "n",
  "F4": "r",
  "F#4": "d",
  "G4": "t",
  "G#4": "z",
  "A4": "s",
  "A#4": "g",
  "B4": "k",
  #記号
  "C#5": "!",
  "D#5": "?",
  "G#5": ",",
  "A#5": ".",
  #機能キー
  "A5": " ",
  "B5": "Backspace",
  "C6": "Enter",
  "C#6": "hanja",
  "D#6": "kana",
}

print('\033[32m'+"PianoType for Mac v0.0.1 is running!"+'\033[0m')

async def midi_stream(input_midi, num_events=10):
  while True:
    if input_midi.poll():
      for event in midi.midis2events(input_midi.read(num_events), input_midi.device_id):
        yield event
    await asyncio.sleep(0.001)

async def main():
  midi.init()
  input_id = midi.get_default_input_id()
  async for event in midi_stream(midi.Input(input_id)):
    #print(event)
    number = int(event.status/16)*16
    if number == 224: #x軸のマウス操作
      gui.move(speed*(event.data2-64), 0)
    elif number == 176: #y軸のマウス操作
      gui.move(0, speed*(event.data2-64))
    elif number == 144: #キーボード押す
      ansi_note  = midi.midi_to_ansi_note(event.data1)
      key = note2key.get(ansi_note)
      if key is not None:
        gui.keyDown(key)
    elif number == 128: #キーボード離す
      ansi_note  = midi.midi_to_ansi_note(event.data1)
      key = note2key.get(ansi_note)
      if key is not None:
        gui.keyUp(key)

asyncio.run(main())


'''
    if event.status == 227: #x軸のマウス操作
      gui.move(speed*(event.data2-64), 0)
    elif event.status == 179: #y軸のマウス操作
      gui.move(0, speed*(event.data2-32))
    elif event.status == 147: #キーボード操作
      ansi_note  = midi.midi_to_ansi_note(event.data1)
      key = note2key.get(ansi_note)
      if key is not None:
        if event.data2 == 0:
          gui.keyDown(key)
        else:
          gui.keyUp(key)
'''
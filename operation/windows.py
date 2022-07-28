import ctypes

MOUSEEVENTF_MOVE = 0x0001

def mouseMove(xOffset=0, yOffset=0):
  ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, xOffset, yOffset, 0, 0)

KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

VirtualKeyCodes = {
  "0" : 0x30,
  "1" : 0x31,
  "2" : 0x32,
  "3" : 0x33,
  "4" : 0x34,
  "5" : 0x35,
  "6" : 0x36,
  "7" : 0x37,
  "8" : 0x38,
  "9" : 0x39,

  "A" : 0x41,
  "B" : 0x42,
  "C" : 0x43,
  "D" : 0x44,
  "E" : 0x45,
  "F" : 0x46,
  "G" : 0x47,
  "H" : 0x48,
  "I" : 0x49,
  "J" : 0x4A,
  "K" : 0x4B,
  "L" : 0x4C,
  "M" : 0x4D,
  "N" : 0x4E,
  "O" : 0x4F,
  "P" : 0x50,
  "Q" : 0x51,
  "R" : 0x52,
  "S" : 0x53,
  "T" : 0x54,
  "U" : 0x55,
  "V" : 0x56,
  "W" : 0x57,
  "X" : 0x58,
  "Y" : 0x59,
  "Z" : 0x5A,

  "," : 0xBC,
  "." : 0xBE,

  "kana" : 0x19,

  "Shift" : 0xA0,
  "Ctrl" : 	0xA2,
  "Alt" : 0xA4,

  "Left" : 0x26,
  "Up" : 0x27,
  "Right" : 0x28,
  "Down" : 0x29,

  "Space" : 0x21,
  "Backspace" : 0x08,
  "Enter" : 0x0D,
}

def keyAction(key, isDown):
  print(key, isDown)
  vkc = VirtualKeyCodes.get(key)
  if vkc is None:
    return
  ctypes.windll.user32.keybd_event(vkc, 0, KEYEVENTF_KEYDOWN if isDown else KEYEVENTF_KEYUP, 0)
import Quartz
import AppKit


def mouseMove(xOffset=0, yOffset=0):
  loc = AppKit.NSEvent.mouseLocation()
  x, y = int(loc.x) + xOffset, int(Quartz.CGDisplayPixelsHigh(0) - loc.y) + yOffset
  mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
  Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

VirtualKeyCodes = {
  '0': 0x1d, # kVK_ANSI_0
  '1': 0x12, # kVK_ANSI_1
  '2': 0x13, # kVK_ANSI_2
  '3': 0x14, # kVK_ANSI_3
  '4': 0x15, # kVK_ANSI_4
  '6': 0x16, # kVK_ANSI_6
  '5': 0x17, # kVK_ANSI_5
  '9': 0x19, # kVK_ANSI_9
  '7': 0x1a, # kVK_ANSI_7
  '8': 0x1c, # kVK_ANSI_8

  'A': 0x00, # kVK_ANSI_A
  'B': 0x0b, # kVK_ANSI_B
  'C': 0x08, # kVK_ANSI_C
  'D': 0x02, # kVK_ANSI_D
  'E': 0x0e, # kVK_ANSI_E
  'F': 0x03, # kVK_ANSI_F
  'G': 0x05, # kVK_ANSI_G
  'H': 0x04, # kVK_ANSI_H
  'I': 0x22, # kVK_ANSI_I
  'J': 0x26, # kVK_ANSI_J
  'K': 0x28, # kVK_ANSI_K
  'L': 0x25, # kVK_ANSI_L
  'M': 0x2e, # kVK_ANSI_M
  'N': 0x2d, # kVK_ANSI_N
  'O': 0x1f, # kVK_ANSI_O
  'P': 0x23, # kVK_ANSI_P
  'Q': 0x0c, # kVK_ANSI_Q
  'R': 0x0f, # kVK_ANSI_R
  'S': 0x01, # kVK_ANSI_S
  'T': 0x11, # kVK_ANSI_T
  'U': 0x20, # kVK_ANSI_U
  'V': 0x09, # kVK_ANSI_V
  'W': 0x0d, # kVK_ANSI_W
  'X': 0x07, # kVK_ANSI_X
  'Y': 0x10, # kVK_ANSI_Y
  'Z': 0x06, # kVK_ANSI_Z
      
  ',': 0x2b, # kVK_ANSI_Comma
  '.': 0x2f, # kVK_ANSI_Period
  '-': 0x1b, # kVK_ANSI_Minus
  '/': 0x2c, # kVK_ANSI_Slash

  'eisu': 0x66, # kVK_JIS_Eisu
  'kana': 0x68, # kVK_JIS_Kana

  'Shift': 0x38, # kVK_Shift
#   'command': 0x37, # kVK_Command
#   'ctrl': 0x3b, # kVK_Control
  'Ctrl': 0x37, # kVK_Control
#   'option': 0x3a, # kVK_Option
  'Alt': 0x3a, # kVK_Option

  'Left': 0x7b, # kVK_LeftArrow
  'Up': 0x7e, # kVK_UpArrow
  'Right': 0x7c, # kVK_RightArrow
  'Down': 0x7d, # kVK_DownArrow

  'Space': 0x31,
  'Backspace': 0x33, # kVK_Delete, which is "Backspace" on OS X.
  'Enter': 0x24, # kVK_Return

#  'capslock': 0x39, # kVK_CapsLock  
#  'fn': 0x3f, # kVK_Function
}

def keyAction(key, isDown):
    event = Quartz.CGEventCreateKeyboardEvent(None, VirtualKeyCodes[key], isDown)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
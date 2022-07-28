import Quartz

def f():
  event_down = Quartz.CGEventCreateKeyboardEvent(None, 0, True)
  Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_down)
  
  event_up = Quartz.CGEventCreateKeyboardEvent(None, 0, False)
  Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_up)

f()
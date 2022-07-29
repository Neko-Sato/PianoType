import asyncio
import rtmidi
import rtmidi.midiutil

class MIDIStream:
  def __init__(
    self, 
    port=None, 
    api=rtmidi.API_UNSPECIFIED, 
    use_virtual=False,
    interactive=True,
    client_name=None,
    port_name=None,
    loop=None
  ):
    self.__midi, _ = rtmidi.midiutil.open_midiinput(
      port=port,
      api=api,
      use_virtual=use_virtual,
      interactive=interactive,
      client_name=client_name,
      port_name=port_name,
    )
    self.__loop = loop if loop else asyncio.get_running_loop()
    self.__queue = asyncio.Queue()
    self.__midi.set_callback(self.__callback)
  def __callback(self, msg, data):
    try:
      asyncio.run_coroutine_threadsafe(
        self.__queue.put(msg[0]), 
        self.__loop,
      )
    except RuntimeError:
      self.close()
  def __aiter__(self):
    return self
  async def __anext__(self):
    return await self.__queue.get()
  def close(self):
    self.__midi.cancel_callback()
    self.__midi.close_port()
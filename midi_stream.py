import asyncio
import rtmidi
import rtmidi.midiutil

async def open_midistream(
  port=None, 
  api=rtmidi.API_UNSPECIFIED, 
  use_virtual=False,
  interactive=True,
  client_name=None,
  port_name=None,
):
  return MIDIStream(
    port=port,
    api=api,
    use_virtual=use_virtual,
    interactive=interactive,
    client_name=client_name,
    port_name=port_name,
    loop=asyncio.get_running_loop(),
  )


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
    self.__isClosed = False
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
    if self.__isClosed:
      raise StopAsyncIteration
    result = await self.__queue.get()
    self.__queue.task_done()
    return result
  def close(self):
    self.__isClosed = True
    self.__midi.cancel_callback()
    self.__midi.close_port()
  
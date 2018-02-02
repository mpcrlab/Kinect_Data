import pyaudio
import numpy as np
import wave

p = pyaudio.PyAudio()
wf = wave.open("alert.wav", 'rb')
volume = 1

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    data = np.fromstring(data, dtype='>f4').astype(np.float32)
    print(data)
    data = data * volume
    data = data.astype(np.uint8)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), 
                channels=wf.getnchannels(), rate=wf.getframerate(), 
                output=True, stream_callback=callback)
stream.stop_stream()
  
def start_tone():
  global stream
  wf.setpos(0)
  stream.start_stream()
  
def stop_tone():
  global stream
  stream.stop_stream()

def exit():
  global stream, p
  stream.close()
  p.terminate()

def set_volume(v):
  global volume
  volume = v
import sounddevice as sd
import numpy as np
import wave

wf = wave.open("alert.wav", 'rb')
nframes, sr = wf.getnframes(), wf.getframerate()
wf = wf.readframes(wf.getnframes())
wfnp = np.fromstring(wf, dtype='i2')
wfnp = np.reshape(wfnp, (nframes, 2))[:,1]
volume = 0.1


sd.stop()

  
def start_tone():
  sd.play((volume * wfnp).astype(np.int16), sr)
  
def stop_tone():
  sd.stop()

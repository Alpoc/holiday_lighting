

import time
import numpy as np
import pyaudio

MIC_RATE = 48000

def start_stream():
    p = pyaudio.PyAudio()
    frames_per_buffer = int(MIC_RATE / 50)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)
    overflows = 0
    prev_ovf_time = time.time()
    print('starting')
    while True:
#        try:
         y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
         y = y.astype(np.float32)
         stream.read(stream.get_read_available(), exception_on_overflow=False)
         if any(y != 0):
            print("true")
#         print(y)
         #callback(y)
#        except IOError:
#            overflows += 1
#            if time.time() > prev_ovf_time + 1:
#                prev_ovf_time = time.time()
#                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    p.terminate()


start_stream()
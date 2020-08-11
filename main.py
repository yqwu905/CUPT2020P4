import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import threading
import time

ay = np.array([0])
data = 0

def draw():
    time.sleep(0.5)
    global ay, data
    RATE = 48000
    plt.ion()
    while(True):
        y = ay
        x = np.linspace(1, y.__len__(), y.__len__()) / RATE
        plt.clf()
        plt.plot(x, y)
        plt.pause(0.1)      
        plt.ioff()


def rec():
    global ax, ay, data
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "cache.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    frames = []
    plt.ion()
    drawTh = threading.Thread(target=draw)
    drawTh.start()
    while (True):
        rawData = stream.read(CHUNK, exception_on_overflow = False)
        #frames.append(rawData)
        data = np.frombuffer(rawData, dtype=np.short)
        ay = np.concatenate((ay, data))
        if ay.__len__() > 1000000:
            ay = np.array([0])
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
if __name__ == '__main__':
    rec()
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import threading

ax = [0]
ay = [0]

def draw():
    global ax, ay
    plt.ion()
    while(True):
        x = ax
        y = ay
        if x.__len__() == y.__len__():
            plt.clf()
            plt.plot(x, y)
            plt.pause(0.1)      
            plt.ioff()


def rec():
    global ax, ay
    CHUNK = 2048
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
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
        data = np.frombuffer(data, dtype=np.short)
        ay = np.concatenate((ay, data))
        ax = np.concatenate((ax, np.linspace(0,CHUNK,CHUNK) / RATE + ax[-1]))   
    
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
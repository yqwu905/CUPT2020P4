import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import threading

x = [0]
y = [0]

def draw():
    global x, y
    plt.ion()
    while(True):
        plt.clf()
        plt.plot(x,y)
        plt.pause(0.1)      
        plt.ioff()


def rec():
    global x, y
    CHUNK = 512
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
    ax = np.array([0])
    ay = np.array([0])
    frames = []
    plt.ion()
    f = 0
    drawTh = threading.Thread(target=draw)
    drawTh.start()
    while (True):
        f += 1
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
        data = np.frombuffer(data, dtype=np.short)
        ay = np.concatenate((ay, data))
        ax = np.concatenate((ax, np.linspace(0,CHUNK,CHUNK) / RATE + ax[-1]))   
        if f % 100 == 0:
            x = ax
            y = ay
        #print(ax.__len__())
    
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
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import warnings

ay = np.array([0])
data = 0

def draw():
    time.sleep(0.5)
    global ay, data
    RATE = 48000
    CHUNK = 16384
    THRESHOLD = 100
    plt.ion()
    while(True):
        d = data
        y = ay
        if d.__len__() == CHUNK:
            print('Show')
            plt.clf()
            plt.xlabel('Frequency/Hz')
            plt.ylabel('Amplitude/mV')
            freqs = np.fft.fftfreq(d.size, 1/RATE)
            fftD = np.fft.fft(d)
            pows = np.abs(fftD)
            pows = pows[freqs > 3000]
            freqs = freqs[freqs > 3000]
            plt.plot(freqs, pows)
            maxFreq = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
            for i in range(freqs.__len__()):
                delta = []
                if pows[i] > maxFreq[-1][1]:
                    for j in maxFreq:
                        delta.append(abs(freqs[i] - j[0]))
                    if min(delta) < THRESHOLD:
                        if pows[i] > maxFreq[delta.index(min(delta))][1]:
                            maxFreq[delta.index(min(delta))] = (freqs[i], pows[i])
                    else:
                        maxFreq[-1] = (freqs[i], pows[i])
                        maxFreq.sort(reverse = True, key = lambda x:x[1])
            for i in maxFreq:
                print(i)
                plt.annotate('(%.1f)'%(i[0]), i)
            '''
            x = np.linspace(1, y.__len__(), y.__len__()) / RATE
            plt.subplot(1,2,2)
            plt.plot(x, y)
            '''
            plt.pause(0.1)
            plt.ioff()
            


def rec():
    global ax, ay, data
    CHUNK = 16384
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
    warnings.filterwarnings("ignore")
    rec()
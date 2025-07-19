from pydub import AudioSegment
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

MIN_AMP_FOR_BUZZ = -21
MAX_FREQ_FOR_BUZZ = 462.5

def get_freq_and_amplitude(segment: AudioSegment):
    # Get raw audio data as array
    samples = np.array(segment.get_array_of_samples())
    
    # If stereo, average the channels
    if segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)
    
    # Get amplitude in dBFS
    amplitude_dbfs = segment.dBFS
    
    # Compute FFT
    N = len(samples)
    T = 1.0 / segment.frame_rate
    yf = fft(samples)
    xf = fftfreq(N, T)[:N//2]

    # Magnitude spectrum
    magnitude = np.abs(yf[:N//2])
    
    # Get dominant frequency
    dominant_idx = np.argmax(magnitude)
    dominant_freq = xf[dominant_idx]

    return dominant_freq, amplitude_dbfs

def is_buzz(freq, amp):
    return freq <= MAX_FREQ_FOR_BUZZ and amp >= MIN_AMP_FOR_BUZZ

def get_buzzes(audio, sleep=False):
    buzzes = []
    buzz_start = None
    buzzing = False
    frames_with_buzz = 0
    for i in range(0, len(audio), 100):
        segment = audio[max(0, i-100):i+1]

        freq, amp = get_freq_and_amplitude(segment)
        # print(f"Time: {i/1000:.2f}s | Freq: {freq:.2f} Hz | Amplitude: {amp:.2f} dBFS")
        
        if is_buzz(freq, amp):
            frames_with_buzz += 1
            if not buzzing and frames_with_buzz >= 3:
                buzzing = True
                buzz_start = (i-300)/1000
                # print("bzzzz.")
        else:
            frames_with_buzz = 0
            if buzzing:
                buzz_end = i/1000
                duration = buzz_end - buzz_start
                buzzes.append({
                    "start": round(buzz_start, 2),
                    "duration": round(duration, 2)
                })
                buzzing = False

        if sleep:
            time.sleep(0.1)

    if buzzing:
        buzz_end = 30.0
        duration = buzz_end - buzz_start
        buzzes.append({
            "start": round(buzz_start, 2),
            "duration": round(duration, 2)
        })

    return buzzes

def main():
    AUDIO: AudioSegment = AudioSegment.from_wav("uvb76.wav")

    start = time.perf_counter()
    print(len(get_buzzes(AUDIO)))
    end = time.perf_counter()
    print("Duration:", end - start)

    x = np.array([i//10 for i in range((len(AUDIO)//100) + 1)])
    y = np.array([get_freq_and_amplitude(AUDIO[max(0, i-100):i+1])[0] for i in range(0, len(AUDIO), 100)])
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Hz")
    plt.title("Average Frequency over Time")
    plt.show()

if __name__ == '__main__':
    main()
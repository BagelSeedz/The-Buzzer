from pydub import AudioSegment
import time
import matplotlib.pyplot as plt
import numpy as np

MIN_FOR_BUZZ = -20

audio: AudioSegment = AudioSegment.from_wav("USB_TEST.wav")

def main():
    buzzes = 0
    frames_with_no_buzz = 0
    buzzed = False
    for i in range(0, len(audio), 100):
        segment = audio[i]

        if segment.dBFS >= MIN_FOR_BUZZ:
            frames_with_no_buzz = 0

            if not buzzed:
                print("bzzzz.")
                buzzed = True
                buzzes += 1
        elif frames_with_no_buzz < 10:
            frames_with_no_buzz += 1
        else:
            buzzed = False

        time.sleep(0.1)

    print(buzzes)

    x = np.array(range(len(audio)))
    y = np.array([seg.dBFS for seg in audio])
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Hz")
    plt.show()

main()
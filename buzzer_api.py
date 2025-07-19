from flask_restful import Resource
from wav_extract import get_buzzes
from pydub import AudioSegment
import json

BUZZER = AudioSegment.from_wav("uvb76.wav")

class Buzzer(Resource):
    def get(self):
        buzzer: AudioSegment = AudioSegment.from_wav("uvb76_0.wav")
        if len(buzzer) != 30000:
            buzzer = AudioSegment.from_wav("uvb76_1.wav")
        buzzes = get_buzzes(buzzer)
        output = dict()
        for i in range(len(buzzes)):
            output[i] = buzzes[i]
        return output
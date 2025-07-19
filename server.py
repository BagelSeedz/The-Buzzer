from flask import Flask
from flask_restful import Api
from buzzer_api import Buzzer
import subprocess
import threading

# === Config ===
KIWIRECORDER_PATH = "kiwirecorder.py"  # path to your recorder script
SERVER = "kiwi-vih.aprs.fi"
PORT = "8073"
FREQ = "4625"
MODE = "usb"
CHUNK_DURATION = 30  # seconds
ROTATION_COUNT = 2   # Number of chunks before overwriting

# === Api ===
app = Flask(__name__)
api = Api(app)
api.add_resource(Buzzer, '/')


def record_chunk(index):
    filename = f"uvb76_{index}"
    print(f"[+] Recording to {filename}")
    
    subprocess.run([
        "python", KIWIRECORDER_PATH,
        "-s", SERVER,
        "-p", PORT,
        "-f", FREQ,
        "-m", MODE,
        "--filename", filename,
        "--tlimit", str(CHUNK_DURATION)
    ])

def loop_record():
    index = 0
    while True:
        record_chunk(index)
        index = (index + 1) % ROTATION_COUNT
        # await asyncio.sleep(1)


if __name__ == '__main__':
    thread = threading.Thread(target=loop_record, daemon=False)
    thread.start()
    app.run(debug=False)
    
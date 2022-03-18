import base64
import json
from pprint import pprint
import pyaudio
import wave
import requests

#Create audio recording stream
audio = pyaudio.PyAudio()
audio_stream = audio.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024)

#Gets audio input
try:
    frames = []
    while True:
        data = audio_stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()

# Write recording to file
sound_file = wave.open("test.wav","wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(16000)
sound_file.writeframes(b''.join(frames))
sound_file.close()

# Open file as binary
with open("test.wav", 'rb') as f:
    audio_encoded = base64.b64encode(f.read())  # read file into RAM and encode it

audio_data = audio_encoded.decode('ascii')

json_audio_data = {
    "data": audio_data,
    "config": {
        "audio_format": "wav",
        "property": "english_16k_common"
    }
}

json_auth_string = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": "tohks2001",
                    "password": "Letmeinpls1234",
                    "domain": {
                        "name": "iamgreybunny"
                    }
                }
            }
        },
        "scope": {
            "project": {
                "name": "ap-southeast-3"
            }
        }
    }
}

response = requests.post("https://iam.ap-southeast-3.myhuaweicloud.com/v3/auth/tokens", json=json_auth_string)
token = response.headers['X-Subject-Token']

header = {"Content-Type": "application/json", "X-Auth-Token": token}
response = requests.post(
    "https://sis-ext.ap-southeast-3.myhuaweicloud.com/v1/046066f16b584b488233cd3732d15da6/asr/short-audio",
    headers=header, json=json_audio_data)
pprint(response.text)

import pyaudio
import wave
import os
import random
CHUNK = 2048
resource_path = os.path.join(os.path.dirname(__file__), 'resource')


def play_audio(wave_input_path):
    p = pyaudio.PyAudio()
    wf = wave.open(wave_input_path, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()


def play_wakeup():
    wav_path = os.path.join(resource_path, 'wav/wakeup_audio')
    wakeup_audio_list = os.listdir(wav_path)
    select_idx = random.randint(0, len(wakeup_audio_list)-1)
    wakeup_audio = wakeup_audio_list[select_idx]
    wakeup_audio_path = os.path.join(wav_path, wakeup_audio)
    play_audio(wakeup_audio_path)


def play_waiting():
    wav_path = os.path.join(resource_path, 'wav/wait')
    wakeup_audio_list = os.listdir(wav_path)
    select_idx = random.randint(0, len(wakeup_audio_list)-1)
    wakeup_audio = wakeup_audio_list[select_idx]
    wakeup_audio_path = os.path.join(wav_path, wakeup_audio)
    play_audio(wakeup_audio_path)

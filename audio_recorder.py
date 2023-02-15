import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 2048


def record_audio(wave_out_path, record_second):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

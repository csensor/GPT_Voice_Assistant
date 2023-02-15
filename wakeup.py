import os
import struct
import pyaudio
import pvporcupine


class WakeupHandler():
    def __init__(self, settings):
        resource_path = os.path.join(os.path.dirname(__file__), 'resource')
        access_key = settings['access_key']
        self.pa = pyaudio.PyAudio()
        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=settings['keywords'] if settings['keywords'] else False,
            keyword_paths=[os.path.join(resource_path, model_name)
                           for model_name in settings['keyword_paths']] if settings['keyword_paths'] else False,
            sensitivities=settings['sensitivities'] if settings['sensitivities'] else [
                0.5]
        )
        self.keywords = settings['keywords'] if settings['keywords'] else [
            name.split('_')[0] for name in settings['keyword_paths']]
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def run_detect_wakeup_word(self):
        pcm = self.audio_stream.read(self.porcupine.frame_length)
        pcm = struct.unpack_from('h' * self.porcupine.frame_length, pcm)
        keyword_index = self.porcupine.process(pcm)
        if keyword_index >= 0:
            return self.keywords[keyword_index]
        else:
            return False

    def release(self):
        self.porcupine.delete()

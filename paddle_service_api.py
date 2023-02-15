import base64
import json
import requests
import soundfile
import io
import traceback


class NLPService():
    def __init__(self, settings):
        self.settings = settings['paddlepaddle']

    def get_asr_result(self, wav_file):
        with open(wav_file, 'rb') as f:
            try:
                base64_bytes = base64.b64encode(f.read())
                base64_string = base64_bytes.decode('utf-8')

                data = {
                    "audio": base64_string,
                    "audio_format": "wav",
                    "sample_rate": 16000,
                    "lang": "zh_cn",
                    "punc": 0
                }

                url = self.settings['asr_url']

                payload = json.dumps(data)
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request(
                    "POST", url, headers=headers, data=payload).json()
                return response['result']['transcription']
            except Exception as e:
                traceback.print_exc()
                return False

    def get_tts_result(self, text, output_path):
        try:
            url = self.settings['tts_url']
            payload = json.dumps({
                "text": text,
                "spk_id": 0,
                "speed": 1,
                "volume": 1,
                "sample_rate": 0
            })
            headers = {
                'Content-Type': 'application/json'
            }

            res = requests.request(
                "POST", url, headers=headers, data=payload).json()
            if not res['success']:
                return False
            wav_base64 = res['result']['audio']
            audio_data_byte = base64.b64decode(wav_base64)
            samples, sample_rate = soundfile.read(
                io.BytesIO(audio_data_byte), dtype='float32')
            soundfile.write(output_path, samples, sample_rate)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

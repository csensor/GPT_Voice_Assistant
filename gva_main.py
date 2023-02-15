import os
from wakeup import WakeupHandler
from audio_player import play_audio, play_wakeup, play_waiting
from audio_recorder import record_audio
from paddle_service_api import NLPService
from gpt_service_api import GPTBot
from utils import get_json
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Pipeline():
    def __init__(self, settings):
        self.wakeup_handler = WakeupHandler(settings['porcupine'])
        self.nlp_service = NLPService(settings['nlp_service'])
        self.gpt_bot = GPTBot(settings['openai'])

    def run(self):
        logger.info('running...')
        while True:
            keyword = self.wakeup_handler.run_detect_wakeup_word()
            if not keyword:
                continue
            # 1. Wait for the wake word
            logger.info('wakeup & listening...')
            play_wakeup()

            # 2. Record your voice
            temp_audio_path = 'temp.wav'
            record_audio(temp_audio_path, 5)

            # 3. Call Automatic Speech Recognition api
            query_text = self.nlp_service.get_asr_result(temp_audio_path)
            if not query_text:
                logger.info("play not get result")
            logger.info('query text: {}'.format(query_text))

            # 4. Wait for GPT reply
            play_waiting()
            response_text = self.gpt_bot.feed_prompt(query_text)
            logger.info('GPT response: {}'.format(response_text))
            temp_response_audio_path = 'temp_res.wav'
            logger.info('gen speech...')

            # 5. Call Text to speech api
            self.nlp_service.get_tts_result(
                response_text, temp_response_audio_path)
            logger.info('play response...')

            # 6. Play the speech
            play_audio(temp_response_audio_path)
            logger.info('listening...')

            # 7. Clean up temporary files
            os.remove(temp_audio_path)
            os.remove(temp_response_audio_path)


if __name__ == '__main__':
    settings_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'resource/settings.json')
    settings = get_json(settings_file)
    pipeline = Pipeline(settings)
    pipeline.run()

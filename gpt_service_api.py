import openai


class GPTBot():
    def __init__(self, settings):
        self.settings = settings
        openai.api_key = settings['api_key']

    def feed_prompt(self, text):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text.strip()
        if '？' in message:
            message = message.split('？')[-1]
        return message

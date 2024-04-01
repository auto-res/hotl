import openai

class ChatGPT:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'model' not in kwargs:
            self.kwargs['model'] = 'gpt-3.5-turbo'
        self.client = openai.OpenAI()

    def __call__(self, messages):
        response = self.client.chat.completions.create(
            messages=messages,
            **self.kwargs)
        return response.choices[0].message.content
from openai import OpenAI
from env import settings

GPT_CONFIG = settings.GPT_CONFIG


class GPT():
    def __init__(self) -> None:
        self.client = OpenAI(api_key=GPT_CONFIG['api_key'])

    def gpt_query_1(self, content, item):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": item}
            ]
        )
        return completion.choices[0].message.content

    def gpt_query_7(self, content7, content8, item7, item8):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": content7},
                {"role": "user", "content": item7}
            ]
        )
        if (completion.choices[0].message.content == "No data"):
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": content8},
                    {"role": "user", "content": item8}
                ]
            )
        return completion.choices[0].message.content

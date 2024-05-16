from openai import OpenAI
from env2 import settings
import json

GPT_CONFIG = settings.GPT_CONFIG


class GPT():
    def __init__(self) -> None:
        self.client = OpenAI(api_key=GPT_CONFIG['api_key'])

    # contents는 프롬프트 list, items는 아이템 list이다.
    # items[i][0]에 내용이 담겨있다.
    def gpt_query(self, contents, items):
        answer_array = []
        for i in range(7):
            print(i)
            # item 8만 토큰이 초과되는데, item 8이 6번째로 들어온다.
            # 둘로 나눠서 No data 가 출력되면 한 번 더 물어본다.
            if (i == 6 and items[i][1] > 12500):
                print('토큰 초과')
                checkpoint = items[i][1] // 2
                if (checkpoint > 13000):
                    print('토큰이 많아도 너무 많음.')
                    answer_array.append('No Data')
                else:
                    midpoint = len(items[i][0]) // 2
                    print(midpoint)
                    front_item = items[i][0][:midpoint]
                    back_item = items[i][0][midpoint:]
                    completion = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": contents[i]},
                            {"role": "user", "content": back_item}
                        ]
                    )
                    print(completion.choices[0].message)
                    if ("No Data" in completion.choices[0].message.content):
                        print("No Data")
                        completion = self.client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": contents[i]},
                                {"role": "user", "content": front_item}
                            ]
                        )
                        answer_array.append(
                            completion.choices[0].message.content)
                    else:
                        answer_array.append(
                            completion.choices[0].message.content)
            else:
                completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": contents[i]},
                        {"role": "user", "content": items[i][0]}
                    ]
                )
                print(completion.choices[0].message)
                answer_array.append(completion.choices[0].message.content)
        return answer_array

    def just_query(self, prompt, content):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
        )
        return completion.choices[0].message.content

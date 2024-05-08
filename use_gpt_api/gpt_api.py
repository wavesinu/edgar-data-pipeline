from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

# gpt_api를 통한 답변 생성
def gpt(corporate_10K_data, prompt_list):
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    prompt = prompt_list[0]
    data = corporate_10K_data

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Answer the questions from {prompt} based on the information from {data}"}

        ]
    )
    return completion.choices[0].message.content
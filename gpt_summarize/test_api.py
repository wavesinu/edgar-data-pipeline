import os
from openai import OpenAI
from sec_api import ExtractorApi
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
extractorApi = ExtractorApi(os.getenv("SEC_API_KEY"))

filing_url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"

section_text = extractorApi.get_section(filing_url, section="1A", return_type="text")

# prompt = f"Summarize the following text in 15 sentencens:\n{section_text}"
# response = OpenAI.Completion.create(engine="text-davinci-003", prompt=prompt)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are an assistant who analyzes the qualitative elements of the content of the annual US report (10K) and suggests investment directions.",
        },
        {
            "role": "user",
            "content": "Summarize the following text in 10 sentences. and translate it to korean.",
        },
        {
            "role": "assistant",
            "content": section_text,
        },
    ],
)

print(completion.choices[0].message.content)

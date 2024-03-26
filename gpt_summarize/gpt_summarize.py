import openai
from sec_api import ExtractorApi


openai.api_key = "API_KEY"
extractorApi = ExtractorApi("API_KEY")

filing_url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"

section_text = extractorApi.get_section(filing_url, item="1A", type="text")

propmt = f"Summarize the following text in 15 sentencens:\n{section_text}"

response = openai.Completion.create(engine="text-davinci-003", propmt=propmt)

print(response["choices"][0]["text"])

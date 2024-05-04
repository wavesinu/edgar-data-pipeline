from gpt_api import gpt
from dotenv import load_dotenv
from load_json_data import load_json
from load_10K_data import load_10K
import os

# 환경변수 로드
load_dotenv()

# 회사명 및 프롬프트 load
prompt_data = load_json("prompt")
corporation_name_data = load_json("corporation")

# 채팅형 프로그램 반복
while True:
    prompt_company = input("애플(APPL), 마이크로소프트(MSFT), 아마존(AMZN) 중 검색할 회사를 입력하세요. 종료를 원하면 '종료'를 입력하십시오: ")
    if prompt_company.strip() == "종료":
        print("프로그램을 종료합니다.")
        break    
    elif prompt_company.strip() in corporation_name_data['company_AAPL']:
        corporate_10K_data = load_10K("apple")
        result = gpt(corporate_10K_data['item_1A'], prompt_data['prompt'])
        print(result)
    elif prompt_company.strip() in corporation_name_data['company_MSFT']:
        corporate_10K_data = load_10K("microsoft")
        result = gpt(corporate_10K_data['item_1A'], prompt_data['prompt'])
        print(result)
    elif prompt_company.strip() in corporation_name_data['company_AMZN']:
        corporate_10K_data = load_10K("amazon")
        result = gpt(corporate_10K_data['item_1A'], prompt_data['prompt'])
        print(result)
    else:
        print("잘못 입력하셨습니다. 다시 입력하세요.")


import json

# json 파일 open 및 load
def load_json(file_name):
    if file_name == "corporation":
        file_path = "C:\\Users\\kdwon\\OneDrive\\바탕 화면\\캡스톤 설계\\edgar-data-pipeline\\use_gpt_api\\company_list.json"
    elif file_name == "prompt":
        file_path = "C:\\Users\\kdwon\\OneDrive\\바탕 화면\\캡스톤 설계\\edgar-data-pipeline\\use_gpt_api\\prompt_list.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
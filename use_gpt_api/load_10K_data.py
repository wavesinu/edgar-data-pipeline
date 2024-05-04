import json

# 파일 경로 
appl_data_path = "C:\\Users\\김대원\\캡스톤 설계\\edgar-data-pipeline\\datasets\\EXTRACTED_FILINGS\\320193_10K_2022_0000320193-22-000108.json"
msft_data_path = "C:\\Users\\김대원\\캡스톤 설계\\edgar-data-pipeline\\datasets\\EXTRACTED_FILINGS\\789019_10K_2022_0001564590-22-026876.json"
amzn_data_path = "C:\\Users\\김대원\\캡스톤 설계\\edgar-data-pipeline\\datasets\\EXTRACTED_FILINGS\\1018724_10K_2022_0001018724-23-000004.json"


# 기업의 10K 데이터 load
def load_10K(corporation):
    if corporation == "apple":
        path = appl_data_path
    elif corporation == "microsoft":
        path = msft_data_path
    elif corporation == "amazon":
        path = amzn_data_path
    else:
        return None

    if path:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return None
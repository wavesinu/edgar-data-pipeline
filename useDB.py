import json
import psycopg2
import os

print("run python3................")

# Connect EDGAR TABLE
conn = psycopg2.connect(host='127.0.0.1', dbname='postgres',user='postgres',password='wkdudwjs0811',port=5432)
cursor=conn.cursor()

# Droping EDGAR table if already exists.
cursor.execute("DROP TABLE IF EXISTS EDGAR")
# Creating table as per requirement
cursor.execute("CREATE TABLE EDGAR (CIK TEXT, COMPANY TEXT, FILING_DATE TEXT, ITEM_1 TEXT, ITEM_3 TEXT, ITEM_7A TEXT)")
print("Table connected successfully...............")

# JSON file's path list
data_path = r'C:\\Users\\김대원\\Desktop\\캡스톤 설계\\edgar_crawler_daewon\\datasets\\EXTRACTED_FILINGS'

# 모든 JSON 파일의 경로가 저장될 리스트
json_data_list = []

# 지정된 디렉토리에서 모든 JSON 파일을 순회
for filename in os.listdir(data_path):
    # 파일 확장자가 .json인 경우에만 처리
    if filename.endswith('.json'):
        # JSON 파일의 경로를 json_data_list에 삽입
        json_data_list.append(os.path.join(data_path, filename))
        
for lst in json_data_list:
    with open(lst, 'r') as file:
        data = json.load(file)
    cursor.execute(
    "INSERT INTO EDGAR (CIK, COMPANY, FILING_DATE, ITEM_1, ITEM_3, ITEM_7A) VALUES (%s, %s, %s, %s, %s, %s)",
    (data['cik'], data['company'], data['filing_date'], data['item_1'], data['item_3'], data['item_7A'])
)

#Open JSON file

# SAVE
conn.commit()

# CLOSE
cursor.close()
conn.close()

print("end python....................")

from stopwords_delete import stopwords_d
import json
import os
from connect_postgresql import *
from connect_gpt import *

# gpt 인스턴스 생성
gpt = GPT()

# db 인스턴스 생성
database = Databases()

first_query = """
CREATE TABLE IF NOT EXISTS table1 (
    company_cik INT NOT NULL,
    year INT NOT NULL,
    name varchar(30),
    item_1 TEXT,
    item_2 TEXT,
    item_3 TEXT,
    item_5 TEXT,
    item_7 TEXT,
    item_7a TEXT,
    item_8 TEXT
)
"""

database.insertDB(first_query)


# extract 폴더 불러와 안에 있는 파일 모두 읽기
dir_path = 'edgar-crawler-main/datasets/EXTRACTED_FILINGS'
file_list = os.listdir(dir_path)

# gpt 프롬프트 json 불러오기
with open('gpt_prompt.json', "r") as file:
    prompt_json = json.load(file)

# 프롬프트 리스트로 만들기
prompt_list = [prompt_json['item_1']['system'],
               prompt_json['item_2']['system'],
               prompt_json['item_3']['system'],
               prompt_json['item_5']['system'],
               prompt_json['item_7']['system'],
               prompt_json['item_7A']['system'],
               prompt_json['item_8']['system']]

# 데이터 추출


def extract_data():
    for file in file_list:
        if (file == ".DS_Store"):
            print(file)
        else:
            index = file.rfind('_')
            index2 = file.rfind('/')

            year = int(file[index-4:index])
            cik = int(file[index2+1:index-9])

            query = f"select * from table1 where company_cik={cik} and year = {year}"
            check = database.readDB(query)
            if (len(check) > 0):
                print(f'{cik},{year}: 이미 존재하는 데이터\n')
            else:
                path = 'edgar-crawler-main/datasets/EXTRACTED_FILINGS/' + file

                with open(path, "r", encoding='utf-8') as f:
                    data = json.load(f)

                name = data['company'].replace("'", "''")

                item1 = stopwords_d(data["item_1"])
                item2 = stopwords_d(data['item_2'])
                item3 = stopwords_d(data['item_3'])
                item5 = stopwords_d(data['item_5'])
                item7A = stopwords_d(data['item_7A'])
                item7 = stopwords_d(data["item_7"])
                item8 = stopwords_d(data["item_8"])
                items = [item1, item2, item3, item5, item7, item7A, item8]
                print(
                    f'{cik}, {year}, 토큰 개수: 1: {item1[1]}, 2: {item2[1]}, 3: {item3[1]}, 5: {item5[1]}, 7: {item7[1]}, 7A: {item7A[1]}, 8: {item8[1]}')
                answer = gpt.gpt_query(prompt_list, items)
                result = []
                for item in answer:
                    # json으로 변환할 수 있는 문자열 형태로 만든다.
                    if (item != 'No Data'):
                        first_processed = item.replace("json", "")
                        second_processed = first_processed.translate(
                            {ord(letter): None for letter in '\n`'})
                        final_processed = second_processed.replace("'", "''")
                        result.append(final_processed)
                    else:
                        result.append(item)

                query = f"insert into table1 (company_cik, year, name, item_1, item_2, item_3, item_5, item_7, item_7a, item_8) values({cik}, {year}, '{name}', '{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}','{result[6]}')"
                database.insertDB(query)


extract_data()

# item 중 1A, 8이 토큰 초과하는 경우가 많다. 때문에 1A와 8은 반으로 나눠서 진행해야 한다.

from stopwords_delete import stopwords_d
import json
import os
from connect_postgresql import *
from connect_gpt import *

# db 인스턴스 생성
database = Databases()

# gpt 인스턴스 생성
gpt = GPT()

# extract 폴더 불러와 안에 있는 파일 모두 읽기
dir_path = 'edgar-crawler-main/datasets/EXTRACTED_FILINGS'
file_list = os.listdir(dir_path)

# gpt 프롬프트 json 불러오기
with open('gpt_prompt.json', "r") as file:
    prompt_json = json.load(file)


# 데이터 추출


def extract_data():
    for file in file_list:
        if file == ".DS_Store":
            print(file)
        else:
            index = file.rfind('_')
            index2 = file.rfind('/')

            year = int(file[index - 4:index])
            cik = int(file[index2 + 1:index - 9])

            query = f"select year from table1 where company_cik={cik}"
            check = database.readDB(query)
            if (len(check) > 0):
                print(f'{cik},{year}: 이미 존재하는 데이터\n')
            else:
                path = 'edgar-crawler-main/datasets/EXTRACTED_FILINGS/' + file

                with open(path, "r", encoding='utf-8') as f:
                    data = json.load(f)

                item1 = stopwords_d(data["item_1"])
                item7 = stopwords_d(data["item_7"])
                item8 = stopwords_d(data["item_8"])
                print(
                    f'{cik}, {year}, item1의 토큰 개수: {item1[1]}, item7의 토큰 개수: {item7[1]}, item8의 토큰 개수: {item8[1]}')

                if item1[1] > 13000:
                    if item7[1] > 13000:
                        if item8[1] > 13000:
                            print("토큰 초과: 1, 7, 8\n")
                        else:
                            print("토큰 초과: 1, 7\n")
                    else:
                        if item8[1] > 13000:
                            print("토큰 초과: 1, 8\n")
                        else:
                            print("토큰 초과: 1\n")
                else:
                    if item7[1] > 13000:
                        if item8[1] > 13000:
                            print("토큰 초과: 7, 8\n")
                        else:
                            print("토큰 초과: 7\n")
                    else:
                        if item8[1] > 13000:
                            print("토큰 초과: 8\n")
                        else:
                            get_re(cik, year, item1, item7, item8)


def get_re(cik, year, item1, item7, item8):
    product_service_new = gpt.gpt_query_1(
        content=prompt_json['product_service_new']['system'], item=item1[0])
    revenue_productNregion = gpt.gpt_query_7(
        content7=prompt_json["revenue_productNregion_7"]["system"],
        content8=prompt_json["revenue_productNregion_8"]["system"], item7=item7[0], item8=item8[0])
    netsales_productNregion = gpt.gpt_query_7(
        content7=prompt_json["netsales_productNregion_7"]["system"],
        content8=prompt_json["netsales_productNregion_8"]["system"], item7=item7[0], item8=item8[0])
    p1 = product_service_new.replace("'", "''")
    p2 = revenue_productNregion.replace("'", "''")
    p3 = netsales_productNregion.replace("'", "''")

    query = f"INSERT INTO table1 (company_cik, year, product_service_new, revenue_productNregion, netsales_productNregion) VALUES({cik}, {year}, '{p1}', '{p2}', '{p3}')"
    database.insertDB(query)


extract_data()

del database

# 작은 질문 단위로 나눠서 질문하는 것이 정확도가 더 높음.(revenue라면 지역별, 제품별을 나눠서 질문하는 것이 정확도가 높음.)

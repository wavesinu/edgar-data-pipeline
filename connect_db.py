from openai import OpenAI
from stopwords_delete import stopwords_d
import json
import os
import pymysql
from env import settings

DATABASE_CONFIG = settings.DATABASE_CONFIG
GPT_CONFIG = settings.GPT_CONFIG

connection = pymysql.connect(
    host=DATABASE_CONFIG['host'], user=DATABASE_CONFIG['user'], password=DATABASE_CONFIG['password'], db=DATABASE_CONFIG['db'])

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS capstone1")
cursor.execute("""CREATE TABLE IF NOT EXISTS table1(
        company_cik INT NOT NULL,
        year INT NOT NULL,
        product_service_new TEXT,
        revenue_productNregion TEXT,
        netsales_productNregion TEXT,
        PRIMARY KEY(company_cik, year)
    )"""
               )


def insert_data(cik, year, p1, p2, p3):
    cursor.execute(
        f"INSERT INTO table1 (company_cik, year, product_service_new, revenue_productNregion, netsales_productNregion) VALUES({cik}, {year}, '{p1}', '{p2}', '{p3}')")


# extract 폴더 불러와 안에 있는 파일 모두 읽기
dir_path = 'edgar-crawler-main/datasets/EXTRACTED_FILINGS'
file_list = os.listdir(dir_path)

# gpt 프롬프트 json 불러오기
with open('gpt_prompt.json', "r") as file:
    prompt_json = json.load(file)

# gpt api 설정
API_KEY = GPT_CONFIG['api_key']
client = OpenAI(api_key=API_KEY)

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

            path = 'edgar-crawler-main/datasets/EXTRACTED_FILINGS/' + file

            with open(path, "r", encoding='utf-8') as f:
                data = json.load(f)

            item1 = stopwords_d(data["item_1"])
            item7 = stopwords_d(data["item_7"])
            item8 = stopwords_d(data["item_8"])
            print(
                f'\n{cik}, {year}, item1의 토큰 개수: {item1[1]}, item7의 토큰 개수: {item7[1]}, item8의 토큰 개수: {item8[1]}')

            if (item1[1] > 13000):
                if (item7[1] > 13000):
                    if (item8[1] > 13000):
                        print("토큰 초과: 1, 7, 8")
                    else:
                        print("토큰 초과: 1, 7")
                else:
                    if (item8[1] > 13000):
                        print("토큰 초과: 1, 8")
                    else:
                        print("토큰 초과: 1")
            else:
                if (item7[1] > 13000):
                    if (item8[1] > 13000):
                        print("토큰 초과: 7, 8")
                    else:
                        print("토큰 초과: 7")
                else:
                    if (item8[1] > 13000):
                        print("토큰 초과: 8")
                    else:
                        get_re(cik, year, item1, item7, item8)


def gpt_query_1(data, item):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": data},
            {"role": "user", "content": item}
        ]
    )
    return completion.choices[0].message.content


def gpt_query_7(data, data8, item7, item8):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": data},
            {"role": "user", "content": item7}
        ]
    )
    if (completion.choices[0].message.content == "No data"):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": data8},
                {"role": "user", "content": item8}
            ]
        )
    return completion.choices[0].message.content


def get_re(cik, year, item1, item7, item8):
    product_service_new = gpt_query_1(
        prompt_json['product_service_new']['system'], item1[0])
    revenue_productNregion = gpt_query_7(
        data=prompt_json["revenue_productNregion_7"]["system"], data8=prompt_json["revenue_productNregion_8"]["system"], item7=item7[0], item8=item8[0])
    netsales_productNregion = gpt_query_7(
        data=prompt_json["netsales_productNregion_7"]["system"], data8=prompt_json["netsales_productNregion_8"]["system"], item7=item7[0], item8=item8[0])
    p1 = product_service_new.replace("'", "''")
    p2 = revenue_productNregion.replace("'", "''")
    p3 = netsales_productNregion.replace("'", "''")
    insert_data(cik, year, p1, p2, p3)


extract_data()

connection.commit()
connection.close()


# 작은 질문 단위로 나눠서 질문하는 것이 정확도가 더 높음.(revenue라면 지역별, 제품별을 나눠서 질문하는 것이 정확도가 높음.)

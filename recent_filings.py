# 새로운 공시의 공시 종류, 주요 내용 요약
# 오늘 또는 어제 올라온 공시

import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse


CIK = '320193'

# 회사 이름 가져오기


def get_company_name():
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    headers = {'User-Agent': 'Mozilla'}
    res = requests.get(url, headers=headers).json()
    cik_df = pd.DataFrame(res['data'], columns=res['fields'])
    return cik_df

# 데이터 가져오기


def getData(cik):
    cik_df = get_company_name()

    headers = {
        "User-Agent": "Mozilla"
    }

    company_name = cik_df.loc[cik_df['cik'] == int(cik), 'name'].values[0]

    url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"

    res = requests.get(url, headers=headers).json()

    company_filings = res['filings']['recent']

    df = pd.DataFrame(company_filings)

    return df, company_name

# 데이터 변환


def recent_filings(cik):
    array = getData(cik=cik)
    df = array[0]
    company_name = array[1]

    # filingDate를 datetime으로 변환
    df['reportDate'] = pd.to_datetime(df['reportDate'])

    yesterday = datetime.today() - timedelta(days=90)

    # 어제나 오늘 파일로 필터링
    filtered_df = df[df['reportDate'] >= yesterday]

    # 혹시 파일이 많이 올라왔을 경우
    value_counts = filtered_df['form'].value_counts()
    print(f'{company_name} 의 최근(3달) 추가된 공시는 총 {len(filtered_df)}건입니다.')

    for value, count in value_counts.items():
        print(f"문서종류 : {value}: {count}건")


recent_filings(cik=CIK)

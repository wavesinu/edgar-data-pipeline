import json
import pandas as pd
import requests
import sys

headers = {
    "User-Agent": "Mozilla/5.0"
}

# matching ticker
def cik_matching_ticker(ticker, headers=headers):
    ticker = ticker.upper().replace(".", "-")
    ticker_json = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()

    for company in ticker_json.values():
        if company["ticker"] == ticker:
            cik = str(company["cik_str"]).zfill(10)
            return cik
    raise ValueError(f"Ticker {ticker} not found in SEC database")

def get_submission_data_for_ticker(ticker, headers=headers, only_filings_df=False):
    cik = cik_matching_ticker(ticker, headers = headers)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    company_json = requests.get(url, headers=headers).json()
    if only_filings_df:
        return pd.DataFrame(company_json['filings']['recent'])
    return company_json

# get accession number 
def get_filtered_filings(ticker, ten_k=True, just_accession_numbers=False, index=1, headers=headers):
    company_filings_df = get_submission_data_for_ticker(ticker, only_filings_df=True, headers=headers)
    if ten_k:
        df = company_filings_df[company_filings_df['form'] == '10-K']
    else:
        df = company_filings_df[company_filings_df['form'] == '10-Q']
    # if just_accession_numbers:
    #     # df = df.set_index('reportDate')
    #     accession_df = df['accessionNumber']
    #     return accession_df[2]
    # else:
    #     return df
        # 데이터프레임을 'reportDate' 기준으로 정렬합니다.
    # df = df.sort_values('reportDate', ascending=False)
    
    # 필요한 경우 accessionNumber만 반환합니다.
    if just_accession_numbers:
        accession_numbers = df['accessionNumber']
        # 요청된 인덱스에 해당하는 accessionNumber가 있는지 확인합니다.
        if len(accession_numbers) >= index:
            return accession_numbers.iloc[index-1]  # index에 해당하는 accessionNumber 반환
        else:
            # 요청된 인덱스에 데이터가 충분하지 않은 경우 예외 메시지 반환
            return f"Not enough filings to provide the {index}th accession number"
    else:
        # just_accession_numbers가 False인 경우, 필터링된 DataFrame 반환
        return df

# def getFilePath(ticker):
#     cik = cik_matching_ticker(ticker, headers = headers)
#     cleaned_cik = cik.lstrip('0')
#     ac_2021 = get_filtered_filings(ticker, ten_k=True, just_accession_numbers=True, headers=headers, 1)
#     ac_2022 = get_filtered_filings(ticker, ten_k=True, just_accession_numbers=True, headers=headers, 2)
#     ac_2023 = get_filtered_filings(ticker, ten_k=True, just_accession_numbers=True, headers=headers, 3)
#     path_2021 = f"{cleaned_cik}_10k_2021_{ac_2021}"
#     path_2022 = f"{cleaned_cik}_10k_2022_{ac_2022}"
#     path_2023 = f"{cleaned_cik}_10k_2023_{ac_2023}"

def getFilePath(ticker, startYear, endYear):
    cik = cik_matching_ticker(ticker, headers=headers)
    cleaned_cik = cik.lstrip('0')
    
    # 연도별로 필요한 정보를 저장할 딕셔너리 생성
    paths = {}
    basePath = "datasets/EXTRACTED_FILINGS"
    
    index = endYear - startYear + 1

    # startYear에서 endYear로 순방향으로 루프 실행
    for year in range(startYear, endYear + 1):
        ac = get_filtered_filings(ticker, ten_k=True, just_accession_numbers=True, headers=headers, index=index)
        paths[year] = f"{basePath}/{cleaned_cik}_10k_{year}_{ac}.json"
        # print(year, ":", paths[year])
        
        # 다음 연도를 위해 index 감소
        index -= 1

    return paths

#Function to load JSON content and return as a dictionary
def load_json_content(file_path):
    try:
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "The file was not found."
    except json.JSONDecodeError:
        return "Error decoding the JSON file."
    except Exception as e:
        return str(e)

# ticker = "aapl"
# filePaths = getFilePath(ticker, 2021, 2023)
# print(filePaths)

if __name__ == "__main__":

    ticker = input("Enter ticker (e.g., AAPL): ")
    key = input("Enter item to extract (e.g., item_1): ")
    startYear = 2021
    endYear = 2023

    file_paths = getFilePath(ticker, startYear, endYear)
    result = {}
    for year in range(startYear, endYear + 1):
        data = load_json_content(file_paths[year])
        item_content = data.get(key, "Item not found in the JSON file.")

        result[f"{year}_10k_report"] = item_content

    print(result)


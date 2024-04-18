import pandas as pd
import requests
import edgarFunctions as edgar
from bs4 import BeautifulSoup
# from headers import headers
import collections
collections.Callable = collections.abc.Callable
from html_table_parser import parser_functions as parser

headers = {
    "User-Agent": "Mozilla"
}

# cik 가져오기 (애플의 경우 예시)
ticker = "aapl"
cik = edgar.cik_matching_ticker(ticker)
print("cik = ",edgar.cik_matching_ticker(ticker))

# submit list (no use)
# data = edgar.get_submission_data_for_ticker(ticker, only_filings_df=False)
# print(data.keys())

# 사업보고서 가져오기 / 10-k | 10-q
filings = edgar.get_filtered_filings(ticker, ten_k=True, just_accession_numbers=True, headers=headers)
print(filings)


# 가장 최신 사업보고서 번호 가져오기
latest_accession_number = filings.sort_index(ascending=False).iloc[0]
accession_number = latest_accession_number
print("latest_accession_number = ", accession_number)

# url_txt
# accession_number_formatted = accession_number.replace('-', '')
# base_url = "https://www.sec.gov/Archives/edgar/data"
# url = f"{base_url}/{cik}/{accession_number_formatted}/{accession_number}.txt"
# print(url)

# url_htm
accession_number_formatted = accession_number.replace('-', '')
base_url = "https://www.sec.gov/Archives/edgar/data"
url_htm = f"{base_url}/{cik}/{accession_number_formatted}/R10.htm"
print(url_htm)

# get filing summary - filename/longname/shortname 추출
# filing_summary = edgar.get_filing_summary(cik, accession_number, headers)
# print(filing_summary)

# # # get content.txt 보고서 전체 내용 추출 
# txt_content = edgar.get_filing_content(cik, accession_number, headers)
# print(txt_content)

# # # get content.htm 보고서 섹션 추출 e.g. R10.htm
htm_content = edgar.get_filing_content_htm(cik, accession_number, headers)
print(htm_content)


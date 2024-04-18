import urllib
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
#사업보고서 개요
# url = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240312000736"
#사업보고서 세부
url = "https://dart.fss.or.kr/report/viewer.do?rcpNo=20240312000736&dcmNo=9702846&eleId=11&offset=150482&length=5624&dtd=dart4.xsd"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

body_content = soup.find('body')
# tables = soup.find('body').find_all('table')

# 모든 테이블을 데이터프레임으로 변환
# dataframes = []
# for table in tables:
#     # HTML 테이블을 pandas 데이터프레임으로 변환
#     df = pd.read_html(str(table))[0]
#     dataframes.append(df)
# data = soup.find("table")
# print(body_content.prettify())
print(body_content)
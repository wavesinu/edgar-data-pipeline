import pandas
import pandas as pd
import requests
from bs4 import BeautifulSoup
# from headers import headers  # change to your own headers file or add variable in code
import re
import time

# only use get_filing_content_htm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from html_table_parser import parser_functions as parser

# only use get_filing_summary
import xml.etree.ElementTree as ET

headers = {
    "User-Agent": "Mozilla"
}


# matching ticker =========================================================
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


# =========================================================
def get_submission_data_for_ticker(ticker, headers=headers, only_filings_df=False):
    cik = cik_matching_ticker(ticker, headers=headers)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    company_json = requests.get(url, headers=headers).json()
    if only_filings_df:
        return pd.DataFrame(company_json['filings']['recent'])
    return company_json


# get accession number 10years =========================================================
def get_filtered_filings(ticker, ten_k=True, just_accession_numbers=False, headers=headers):
    company_filings_df = get_submission_data_for_ticker(ticker, only_filings_df=True, headers=headers)
    if ten_k:
        df = company_filings_df[company_filings_df['form'] == '10-K']
    else:
        df = company_filings_df[company_filings_df['form'] == '10-Q']
    if just_accession_numbers:
        df = df.set_index('reportDate')
        accession_df = df['accessionNumber']
        return accession_df
    else:
        return df


# get latest accession number =========================================================
def get_latest_accession_number(ticker, ten_k=True, headers=headers):
    # only_filings_df=True로 설정하여 DataFrame으로만 제출 데이터를 가져옵니다.
    filings_df = get_filtered_filings(ticker, ten_k=ten_k, just_accession_numbers=True, headers=headers)

    # 가장 최신 날짜의 제출물을 가져오기 위해 인덱스(날짜)를 기준으로 내림차순 정렬 후 첫 번째 항목을 선택합니다.
    latest_accession_number = filings_df.sort_index(ascending=False).iloc[0]

    return latest_accession_number


# # get filing summary =========================================================
def get_filing_summary(cik, accession_number, headers):
    # Accession number에서 하이픈('-') 제거
    accession_number_formatted = accession_number.replace('-', '')

    # SEC EDGAR에서 문서 URL 생성
    base_url = "https://www.sec.gov/Archives/edgar/data"
    url = f"{base_url}/{cik}/{accession_number_formatted}/FilingSummary.xml"

    response = requests.get(url, headers=headers)

    # 성공적으로 데이터를 가져왔는지 확인
    if response.status_code == 200:
        # 응답에서 XML 데이터를 가져옴
        xml_data = response.content

        # ElementTree를 사용하여 XML 데이터 파싱
        tree = ET.ElementTree(ET.fromstring(xml_data))

        # # 루트 요소에 접근
        # root = tree.getroot()

        segment_count = tree.find('.//SegmentCount').text
        print(f"Segment Count: {segment_count}\n")
        # 'Reports' 섹션 내의 'Report' 태그들을 순회
        for report in tree.findall('.//Report'):
            html_file_name = report.find('HtmlFileName').text if report.find('HtmlFileName') is not None else 'N/A'
            long_name = report.find('LongName').text if report.find('LongName') is not None else 'N/A'
            short_name = report.find('ShortName').text if report.find('ShortName') is not None else 'N/A'

            # 결과 출력
            print(f"HTML File Name: {html_file_name}\nLong Name: {long_name}\nShort Name: {short_name}\n")
    else:
        print(f"Error fetching XML: Status code {response.status_code}")


# get report content,txt =========================================================
def get_filing_content(cik, accession_number, headers):
    # Accession number에서 하이픈('-') 제거
    accession_number_formatted = accession_number.replace('-', '')

    # SEC EDGAR에서 문서 URL 생성
    base_url = "https://www.sec.gov/Archives/edgar/data"
    url = f"{base_url}/{cik}/{accession_number_formatted}/{accession_number}.txt"

    # 요청 및 응답 받기
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # BeautifulSoup를 사용하여 HTML 내용 파싱 (예시로 HTML 내용을 그대로 반환)
        soup = BeautifulSoup(response.text, 'html.parser').div
        # html -> txt
        # text_content = soup.get_text(separator='\n', strip=True)
        return soup.prettify()
    else:
        return "Error fetching document."


# def get_filing_content_htm(cik, accession_number, headers):
#     # Initialize Chrome driver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#     # Remove hyphens from the accession number for URL
#     accession_number_formatted = accession_number.replace('-', '')

#     # Create the main document URL (.htm format)
#     base_url = "https://www.sec.gov/Archives/edgar/data"
#     url = f"{base_url}/{cik}/{accession_number_formatted}/R25.htm"

#     # Open the web page using Selenium
#     driver.get(url)

#     # Optional: wait for the page to load completely
#     # time.sleep(5)

#     # Get the source code of the page
#     html_source = driver.page_source
#     driver.quit()  # Always close the driver

#     # Create a BeautifulSoup object
#     soup = BeautifulSoup(html_source, "html.parser")

#     # Locate the table
#     data = soup.find("table")
#     if not data:
#         return pd.DataFrame()  # Return an empty DataFrame if no table is found

#     # Process each row in the table
#     table_rows = []
#     for tr in data.find_all('tr'):
#         row = []
#         cells = tr.find_all('td')
#         for cell in cells:
#             cell_text = ' '.join(cell.stripped_strings)  # Join all text items stripping extra whitespace
#             cell_text = re.sub(r'\s+', ' ', cell_text).replace('$', '')  # Remove $ and reduce multiple spaces
#             if cell_text:  # Add non-empty text to the row
#                 row.append(cell_text)
#         if row:
#             table_rows.append(row)

#     # Normalize row lengths by filling shorter rows with None
#     if table_rows:
#         max_length = max(len(row) for row in table_rows)
#         for row in table_rows:
#             while len(row) < max_length:
#                 row.append(None)

#     # Convert the list of rows into a DataFrame
#     df = pd.DataFrame(table_rows)
#     print(df)
#     return df

# def make2d(table_soup):
#     """ Convert an HTML table (parsed by BeautifulSoup) to a 2D list. """
#     return [[cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
#             for row in table_soup.find_all('tr')]

def revise_table(html_source):
    soup = BeautifulSoup(html_source, "html.parser")

    data = soup.find("table")

    tr_tags = data.find('tr')

    tr_list = []

    for tr_tag in tr_tags:
        t_list = []
        td_tags = tr_tag.find('td')
        for td_tag in td_tags:
            if td_tag.text.strip() == "":
                td_tag.decompose()
            else:
                p_tags = td_tag.find("p")
                if p_tags:
                    text = ''
                    for p_tag in p_tags:
                        text += p_tag.get_text(separator=' ', strip=True)
                        if "$" in text:
                            text = text.replace("$", "")
                        t_list.append(re.sub(r'\s+', ' ', text))

                else:
                    text = ''
                    one_p_tag = td_tag.find("p")
                    if one_p_tag:
                        print('p 태그 하나')
                    else:
                        text += td_tag.get_text(separator=' ', strip=True)
                        if "$" in text:
                            text = text.replace("$", "")
                        t_list.append(re.sub(r'\s+', ' ', text))

        tr_list.append(t_list)

    tr_list = [item for item in tr_list if item != []]

    for i in range(len(tr_list)):
        tr_list[i] = [ele for ele in tr_list[i] if ele != '']

    max_length = max(len(arr) for arr in tr_list)

    for arr in tr_list:
        if len(arr) != 1:
            while len(arr) < max_length:
                arr.insert(0, None)

    df = pandas.DataFrame(tr_list)
    print(df)


# get report content_other type =========================================================
def get_filing_content_htm(cik, accession_number, headers):
    # Chrome 드라이버 초기화
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Accession number에서 하이픈('-') 제거
    accession_number_formatted = accession_number.replace('-', '')

    # SEC EDGAR에서 메인 문서 URL 생성 (.htm 형식)
    base_url = "https://www.sec.gov/Archives/edgar/data"
    url = f"{base_url}/{cik}/{accession_number_formatted}/R25.htm"
    # url = f"{base_url}/{cik}/{accession_number_formatted}/{accession_number}-index-headers.html"

    # Selenium을 사용하여 웹 페이지 열기
    driver.get(url)

    # 페이지 로드를 기다리기 위해 필요하다면 time.sleep()을 사용할 수 있습니다.
    # 예: import time; time.sleep(5)

    # 페이지의 소스 코드 가져오기
    html_source = driver.page_source

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_source, 'html.parser')

    data = soup.find("table", {"class": "report"})

    table = parser.make2d(data)

    # df = pd.DataFrame(table)

    print(table)

    # t_data = []

    # for table in data:
    #     f_data = table.find("table")
    #     revise_table(f_data)

    # revise_table(html_source)

    # df=pd.DataFrame(table[1:], columns=table[0])

    # 데이터를 pandas DataFrame으로 변환

    # DataFrame 출력

    # table = make2d(data)
    # print("table: ", table)

    # df = pd.DataFrame(rows=rows, columns=columns)
    # print(df)

    # df = pd.DataFrame(data=table[1:], columns=table[0])
    # print(df)

    # if data:
    #     # Use the 'make2d' function from the parser module, which should be defined elsewhere
    #     # Ensure you have correctly imported this function or have defined it appropriately
    #     # Example: from your_parser_module import make2d
    #     try:
    #         table = make2d(data)  # Assuming make2d is a function that converts HTML table to a 2D list
    #         if table and len(table) > 1:
    #             df = pd.DataFrame(data=table[1:], columns=table[0])
    #             print(df)
    #             return df
    #         else:
    #             print("Table data is not sufficient to form a DataFrame.")
    #             return pd.DataFrame()
    #     except Exception as e:
    #         print(f"Failed to parse the table: {e}")
    #         return pd.DataFrame()
    # else:
    #     print("No table found with the specified class.")
    #     return pd.DataFrame()

    # table = parser.make2d(data)
    # df = pd.DataFrame(data= table[1:], columns= table[0])
    # print(df)

    # # html -> txt
    # # soup = soup.get_text(separator='\n', strip=True)

    # # 가져온 데이터 출력 (또는 처리)
    # # print(soup.prettify())
    # return table

    # 드라이버 종료
    driver.quit()

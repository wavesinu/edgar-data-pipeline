import os

from sec_api import QueryApi
from dotenv import load_dotenv

load_dotenv()
queryApi = QueryApi(api_key=os.getenv("SEC_API_KEY"))

nasdaq_tickers = [
    "AAPL",
    "MSFT"
]

base_query = {
    "query": {
        "query_string": {
            "query": "PLACEHOLDER",
            "time_zone": "America/New_York",
        }
    },
    "from": "0",
    "size": "200",
    # sort returned filings by the filedAt key/value
    "sort": [{"filedAt": {"order": "desc"}}],
}

log_file = open("filing_urls.txt", "a")

for ticker in nasdaq_tickers:
    print("Starting download for ticker {ticker}".format(ticker=ticker))

    # 2020년부터 2023년까지의 10-K 보고서 다운로드
    for year in range(2023, 2022, -1):
        for month in range(1, 13, 1):
            universe_query = (
                    'formType:("10-K") AND '
                    + "filedAt:[{year}-{month:02d}-01 TO {year}-{month:02d}-31]".format(year=year, month=month)
            )

            # 쿼리에 티커 추가
            universe_query += ' AND ticker:"{ticker}"'.format(ticker=ticker)

            base_query["query"]["query_string"]["query"] = universe_query

            for from_batch in range(0, 400, 200):
                base_query["from"] = from_batch

                response = queryApi.get_filings(base_query)

                if len(response["filings"]) == 0:
                    break

                urls_list = list(
                    map(lambda x: x["linkToFilingDetails"], response["filings"])
                )

                urls_string = "\n".join(urls_list) + "\n"

                log_file.write(urls_string)

            print(
                "Filing URLs downloaded for {year}-{month:02d}".format(
                    year=year, month=month
                )
            )

log_file.close()

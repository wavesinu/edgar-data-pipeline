from sec_api import QueryApi

queryApi = QueryApi(api_key="15bb43f74ff79a99c92827072077c98639fec14ae379af7cb5b8ba2c5a50e9f6")

"""
On each search request, the PLACEHOLDER in the base_query is replaced 
with our form type filter and with a date range filter.
"""
base_query = {
    "query": {
        "query_string": {
            "query": "PLACEHOLDER",  # this will be set during runtime
            "time_zone": "America/New_York"
        }
    },
    "from": "0",
    "size": "200",  # don't change this
    # sort returned filings by the filedAt key/value
    "sort": [{"filedAt": {"order": "desc"}}]
}

# open the file we use to store the filing URLs
log_file = open("filing_urls.txt", "a")

# start with filings filed in 2022, then 2020, 2019, ... up to 2010
# uncomment next line to fetch all filings filed from 2022-2010
# for year in range(2022, 2009, -1):
for year in range(2024, 2020, -1):
    print("Starting download for year {year}".format(year=year))

    # a single search universe is represented as a month of the given year
    for month in range(1, 13, 1):
        # get 10-Q and 10-Q/A filings filed in year and month
        # resulting query example: "formType:\"10-Q\" AND filedAt:[2021-01-01 TO 2021-01-31]"
        universe_query = \
            "formType:(\"10-K\") AND " + \
            "filedAt:[{year}-{month:02d}-01 TO {year}-{month:02d}-31]" \
                .format(year=year, month=month)

        # set new query universe for year-month combination
        base_query["query"]["query_string"]["query"] = universe_query;

        # paginate through results by increasing "from" parameter
        # until we don't find any matches anymore
        # uncomment next line to fetch all 10,000 filings
        # for from_batch in range(0, 9800, 200):
        for from_batch in range(0, 400, 200):
            # set new "from" starting position of search
            base_query["from"] = from_batch;

            response = queryApi.get_filings(base_query)

            # no more filings in search universe
            if len(response["filings"]) == 0:
                break;

            # for each filing, only save the URL pointing to the filing itself
            # and ignore all other data.
            # the URL is set in the dict key "linkToFilingDetails"
            urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))

            # transform list of URLs into one string by joining all list elements
            # and add a new-line character between each element.
            urls_string = "\n".join(urls_list) + "\n"

            log_file.write(urls_string)

        print("Filing URLs downloaded for {year}-{month:02d}".format(year=year, month=month))

log_file.close()

print("All URLs downloaded")

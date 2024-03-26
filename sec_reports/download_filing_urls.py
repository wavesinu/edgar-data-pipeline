import os
import multiprocessing
from sec_api import RenderApi

renderApi = RenderApi(
    api_key="d1cceb7c0f4c36080e90bca6c0970aac477952759486bc5f8988c8353d8db872"
)


# download filing and save to "filings" folder
def download_filing(url):
    try:
        filing = renderApi.get_filing(url)
        # file_name example: 000156459019027952-msft-10k_20190630.htm
        file_name = url.split("/")[-2] + "-" + url.split("/")[-1]
        download_to = "./filings/" + file_name
        with open(download_to, "w") as f:
            f.write(filing)
    except Exception as e:
        print("Problem with {url}".format(url=url))
        print(e)


# load URLs from log file
def load_urls():
    log_file = open("filing_urls.txt", "r")
    urls = log_file.read().split("\n")  # convert long string of URLs into a list
    log_file.close()
    return urls


def download_all_filings():
    print("Start downloading all filings")

    download_folder = "./filings"
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)

    # uncomment next line to process all URLs
    # urls = load_urls()
    urls = load_urls()[1:40]
    print("{length} filing URLs loaded".format(length=len(urls)))

    number_of_processes = 20

    with multiprocessing.Pool(number_of_processes) as pool:
        pool.map(download_filing, urls)

    print("All filings downloaded")

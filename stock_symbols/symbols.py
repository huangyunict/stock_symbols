import pprint
import sys

from bs4 import BeautifulSoup

from stock_symbols.symbol_helper import *


#   pass in working path to avoid potential permission error
def get_sp500_symbols(work_path=""):
    if not work_path:
        work_path = _get_default_work_path()
    page_html = wiki_html('List_of_S%26P_500_companies', os.path.join(work_path, 'SP500.html'))
    wiki_soup = BeautifulSoup(page_html, "html.parser")
    symbol_table = wiki_soup.find(attrs={'class': 'wikitable sortable'})

    symbol_data_list = list()

    for symbol in symbol_table.find_all("tr"):
        symbol_data_content = dict()
        symbol_raw_data = symbol.find_all("td")
        td_count = 0
        for symbol_data in symbol_raw_data:
            if(td_count == 0):
                symbol_data_content['symbol'] = symbol_data.text.encode('utf-8')
            elif(td_count == 1):
                symbol_data_content['company'] = symbol_data.text.encode('utf-8')
            elif(td_count == 3):
                symbol_data_content['sector'] = symbol_data.text.encode('utf-8')
            elif(td_count == 4):
                symbol_data_content['industry'] = symbol_data.text.encode('utf-8')
            elif(td_count == 5):
                symbol_data_content['headquaters'] = symbol_data.text.encode('utf-8')

            td_count += 1

        symbol_data_list.append(symbol_data_content)

    return symbol_data_list[1::]


def get_nyse_symbols(work_path=""):
    if not work_path:
        work_path = _get_default_work_path()
    return _get_exchange_data("NYSE", work_path)


def get_amex_symbols(work_path=""):
    if not work_path:
        work_path = _get_default_work_path()
    return _get_exchange_data("AMEX", work_path)


def get_nasdaq_symbols(work_path=""):
    if not work_path:
        work_path = _get_default_work_path()
    return _get_exchange_data("NASDAQ", work_path)


def _get_exchange_data(exchange, work_path):
    url = get_exchange_url(exchange)
    file_path = os.path.join(work_path, exchange)
    if is_cached(file_path):
        with open(file_path, "r") as cached_file:
            symbol_data = cached_file.read()
    else:
      symbol_data = fetch_file(url)
      save_file(file_path, symbol_data)
    
    return get_symbol_list(symbol_data, exchange)


def _get_default_work_path():
    return os.path.dirname(stock_symbols.__file__)


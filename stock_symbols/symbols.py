# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from stock_symbols.symbol_helper import *


__work_dir = None


def set_work_dir(work_dir=""):
    """Set working directory, used in following functions.
    :param work_dir: working directory. If passed in None or empty, using default working directory.
    """
    global __work_dir
    if not work_dir:
        __work_dir = _get_default_work_dir()


def get_work_dir():
    """Get working directory.
    :return: working directory.
    """
    global __work_dir
    if not __work_dir:
        __work_dir = _get_default_work_dir()
    return __work_dir


#   pass in working path to avoid potential permission error
def get_sp500_symbols():
    page_html = wiki_html("List_of_S%26P_500_companies", os.path.join(get_work_dir(), "SP500.html"))
    wiki_soup = BeautifulSoup(page_html, "html.parser")
    symbol_table = wiki_soup.find(attrs={"class": "wikitable sortable"})

    symbol_data_list = list()

    for symbol in symbol_table.find_all("tr"):
        symbol_data_content = dict()
        symbol_raw_data = symbol.find_all("td")
        td_count = 0
        for symbol_data in symbol_raw_data:
            if td_count == 0:
                symbol_data_content["symbol"] = symbol_data.text.encode("utf-8")
            elif td_count == 1:
                symbol_data_content["company"] = symbol_data.text.encode("utf-8")
            elif td_count == 3:
                symbol_data_content["sector"] = symbol_data.text.encode("utf-8")
            elif td_count == 4:
                symbol_data_content["industry"] = symbol_data.text.encode("utf-8")
            elif td_count == 5:
                symbol_data_content["headquaters"] = symbol_data.text.encode("utf-8")

            td_count += 1

        symbol_data_list.append(symbol_data_content)

    return symbol_data_list[1::]


def get_nyse_symbols():
    """Get symbols from New York Stock Exchange market.
    :return: Symbol list from NYSE market.
    """
    return _get_exchange_data("NYSE")


def get_amex_symbols():
    """Get symbols from American Stock Exchange market.
    :return: Symbol list from AMEX market.
    """
    return _get_exchange_data("AMEX")


def get_nasdaq_symbols():
    """Get symbols from NASDAQ market.
    :return: Symbol list from NASDAQ market.
    """
    return _get_exchange_data("NASDAQ")


def _get_exchange_data(market):
    """Get market symbols from NASDAQ website,
    :param market: exchange market, possible values are: "AMEX", "NASDAQ", "NYSE".
    :return: symbol list.
    """
    url = get_exchange_url(market)
    file_path = os.path.join(get_work_dir(), market)
    if is_cached(file_path):
        with open(file_path, "r") as cached_file:
            symbol_data = cached_file.read()
    else:
        symbol_data = fetch_file(url)
        save_file(file_path, symbol_data)
    return get_symbol_list(symbol_data, market)


def _get_default_work_dir():
    """Get default work directory, default to the package install path
    :return: default work directory.
    """
    return os.path.dirname(stock_symbols.__file__)

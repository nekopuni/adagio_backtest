from collections import namedtuple
from datetime import datetime
from enum import Enum, unique

import adagio
import quandl
from adagio import keys
from adagio.utils.logging import get_logger
from adagio.utils.mongo import get_library
from pandas_datareader.data import DataReader

from adagio_backtest.config import *

logger = get_logger(name=__name__)
START_DATE = datetime(1970, 1, 1)
adagio.AdagioConfig.quandl_token = QUANDL_TOKEN

fx_rates_info = namedtuple('fx_rates_info',
                           ['data_name', 'data_source', 'fx_rates_name'])


@unique
class FxRatesInfo(Enum):
    EUR = fx_rates_info('DEXUSEU', 'fred', 'EUR/USD')
    JPY = fx_rates_info('DEXJPUS', 'fred', 'USD/JPY')
    CNH = fx_rates_info('DEXCHUS', 'fred', 'USD/CNH')
    CNY = fx_rates_info('DEXCHUS', 'fred', 'USD/CNY')
    CAD = fx_rates_info('DEXCAUS', 'fred', 'USD/CAD')
    GBP = fx_rates_info('DEXUSUK', 'fred', 'GBP/USD')
    MXN = fx_rates_info('DEXMXUS', 'fred', 'USD/MXN')
    AUD = fx_rates_info('DEXUSAL', 'fred', 'AUD/USD')
    BRL = fx_rates_info('DEXBZUS', 'fred', 'USD/BRL')
    KRW = fx_rates_info('DEXKOUS', 'fred', 'USD/KRW')
    CHF = fx_rates_info('DEXSZUS', 'fred', 'USD/CHF')
    INR = fx_rates_info('DEXINUS', 'fred', 'USD/INR')
    ZAR = fx_rates_info('DEXSFUS', 'fred', 'USD/ZAR')
    TRY = fx_rates_info('CURRFX/USDTRY', 'quandl', 'USD/TRY')


def get_fx_rates(currency):
    """ Return historical fx rates for a given currency name """
    fx_rates_info = FxRatesInfo[currency].value

    if fx_rates_info.data_source == 'quandl':
        fx_rates = quandl.get(fx_rates_info.data_name,
                              api_key=adagio.AdagioConfig.quandl_token)
        fx_rates = fx_rates['Rate']
    else:
        fx_rates = DataReader(fx_rates_info.data_name,
                              fx_rates_info.data_source, START_DATE)
        fx_rates = fx_rates.squeeze()

    fx_rates = (fx_rates
                .fillna(method='pad')
                .rename(fx_rates_info.fx_rates_name))
    return fx_rates


if __name__ == '__main__':
    library = get_library(keys.fx_rates)

    for item in FxRatesInfo:
        logger.info('Saving fx rates for {}'.format(item.name))
        fx_rates = get_fx_rates(item.name)
        symbol = fx_rates.name
        library.write(symbol, fx_rates)

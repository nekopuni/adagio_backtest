import adagio
from adagio import keys
from adagio.data.cash import get_cash_rate, to_cash_returns
from adagio.utils.logging import get_logger
from adagio.utils.mongo import get_library

from config import QUANDL_TOKEN

logger = get_logger(name=__name__)
adagio.AdagioConfig.quandl_token = QUANDL_TOKEN


if __name__ == '__main__':
    library = get_library(keys.cash_returns)

    currencies = ['USD', 'EUR', 'JPY', 'GBP']

    for ccy in currencies:
        logger.info('Saving cash returns for {}'.format(ccy))

        # get cash rates
        cash_rate = get_cash_rate(ccy)
        symbol = cash_rate.name
        library.write(symbol, cash_rate)

        # get cash returns
        cash_return = to_cash_returns(cash_rate, ccy)
        symbol = cash_return.name
        library.write(symbol, cash_return)

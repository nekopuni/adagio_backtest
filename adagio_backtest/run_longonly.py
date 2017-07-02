import adagio
from adagio import keys
from adagio.utils.const import FuturesInfo
from adagio.utils.logging import get_logger
from adagio.utils.mongo import get_library

from adagio_backtest.config import *

logger = get_logger(name=__name__)
adagio.AdagioConfig.quandl_token = QUANDL_TOKEN


if __name__ == '__main__':

    library = get_library(keys.backtest)

    for futures in FuturesInfo:
        logger.info('Running backtest for {}'.format(futures.name))
        futures_info = futures.value

        longonly_params = {
            keys.lo_ticker: futures.name,
            keys.backtest_ccy: futures_info.contract_ccy,
        }

        engine = adagio.Engine()
        engine.add(adagio.LongOnly(**longonly_params))
        engine.backtest()
        library.write(engine.symbol, engine, metadata=engine.all_params)

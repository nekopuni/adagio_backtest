import adagio
from adagio import keys
from adagio.utils.const import FuturesInfo
from adagio.utils.logging import get_logger
from adagio.utils.mongo import get_library

from config import QUANDL_TOKEN

logger = get_logger(name=__name__)
adagio.AdagioConfig.quandl_token = QUANDL_TOKEN

if __name__ == '__main__':

    library = get_library(keys.backtest)

    for futures in FuturesInfo:
        logger.info('Saving futures contracts for {}'.format(futures.name))
        engine = adagio.Engine()
        engine.add(adagio.LongOnly(lo_ticker=futures.name))
        engine.update_database()

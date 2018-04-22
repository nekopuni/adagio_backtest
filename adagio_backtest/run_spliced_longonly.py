import adagio
from adagio import keys
from adagio.utils.logging import get_logger
from adagio.utils.mongo import get_library

from config import QUANDL_TOKEN

logger = get_logger(name=__name__)
adagio.AdagioConfig.quandl_token = QUANDL_TOKEN


if __name__ == '__main__':

    library = get_library(keys.backtest)

    splice_params = [
        ['CME_ES', keys.splice_es_and_sp],
        ['CME_NQ', keys.splice_nq_and_nd],
        ['CME_YM', keys.splice_ym_and_dj],
    ]

    for ticker, splice_func in splice_params:
        engine = adagio.Engine()
        engine.add(adagio.LongOnly(lo_ticker=ticker, splice_func=splice_func))
        engine.backtest()
        library.write(engine.symbol, engine, metadata=engine.all_params)

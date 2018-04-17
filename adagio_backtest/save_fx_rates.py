import adagio
from adagio import keys
from adagio.data.fx import FxRatesInfo, get_fx_rates
from adagio.utils.logging import get_logger
from adagio.utils.mongo import get_library

from config import QUANDL_TOKEN

logger = get_logger(name=__name__)
adagio.AdagioConfig.quandl_token = QUANDL_TOKEN


if __name__ == '__main__':
    library = get_library(keys.fx_rates)

    for item in FxRatesInfo:
        logger.info('Saving fx rates for {}'.format(item.name))
        fx_rates = get_fx_rates(item.name)
        symbol = fx_rates.name
        library.write(symbol, fx_rates)

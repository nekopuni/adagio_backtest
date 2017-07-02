import adagio
from adagio import keys

from adagio_backtest.config import *

adagio.AdagioConfig.quandl_token = QUANDL_TOKEN

if __name__ == '__main__':

    # common parameters
    lo_vol_scale_params = {
        keys.vs_window: 63,
        keys.vs_chg_rule: '+Wed-1bd+1bd',
        keys.vs_target_vol: 0.1,
    }
    momentum_params = {
        keys.signal_type: keys.momentum,
        keys.signal_windows: [[8, 24], [16, 48], [32, 96]],
        keys.signal_chg_rule: '+Wed-1bd+1bd',
        keys.signal_to_position: keys.linear,
        keys.position_cap: 1.0,
        keys.position_floor: -1.0
    }

    # parameters by asset-class
    equity_lo_params = {
        keys.lo_ticker: ['CME_SP', 'CME_ND', 'CME_DJ', 'CME_MD'],
        keys.slippage: 2.0,
    }

    # Nested Engine example
    engine_equity = adagio.Engine(name='equity_momentum')
    engine_equity.add(adagio.LongOnly(**equity_lo_params))
    engine_equity.add(adagio.VolatilityScaling(**lo_vol_scale_params))
    engine_equity.add(adagio.Signal(**momentum_params))
    engine_equity.backtest()

    # engine2 = adagio.Engine(name='engine2')
    # engine2.add(adagio.LongOnly(**longonly_params))
    # engine2.add(adagio.VolatilityScaling(**lo_vol_scale_params))
    # engine2.add(adagio.Signal(**signal_params))
    #
    # engine3 = adagio.Engine(name='engine3')
    # engine3.add([engine1, engine2])
    # engine3.add(adagio.Portfolio(**portfolio_params))
    # engine3.add(adagio.PortVolatilityScaling(**portfolio_vol_scale_params))
    # engine3.backtest()

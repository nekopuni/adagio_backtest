import adagio
from adagio import keys

from config import *

adagio.AdagioConfig.quandl_token = QUANDL_TOKEN

if __name__ == '__main__':
    longonly_params = {
        keys.lo_ticker: ['SGX_NK', 'LIFFE_FTI'],
        keys.slippage: 1.0,
    }
    lo_vol_scale_params = {
        keys.vs_window: 63,
        keys.vs_chg_rule: '+Wed-1bd+1bd',
        keys.vs_target_vol: 0.1,
    }
    signal_params = {
        keys.signal_type: keys.momentum,
        keys.signal_windows: [[8, 24], [16, 48], [32, 96]],
        keys.signal_chg_rule: '+Wed-1bd+1bd',
        keys.signal_to_position: keys.linear,
        keys.position_cap: 1.0,
        keys.position_floor: -1.0
    }
    portfolio_params = {
        keys.weighting: keys.equal_weight
    }
    portfolio_vol_scale_params = {
        keys.vs_window: 63,
        keys.vs_chg_rule: '+Wed-1bd+1bd',
        keys.vs_target_vol: 0.1,
    }
    engine_params = {
        keys.name: 'engine',
        keys.backtest_ccy: 'USD'
    }

    # Simple Engine example
    engine = adagio.Engine(**engine_params)
    engine.add(adagio.LongOnly(**longonly_params))
    engine.add(adagio.VolatilityScaling(**lo_vol_scale_params))
    engine.add(adagio.Signal(**signal_params))
    engine.add(adagio.Portfolio(**portfolio_params))
    engine.add(adagio.PortVolatilityScaling(**portfolio_vol_scale_params))
    engine.backtest()

    # Nested Engine example
    engine1 = adagio.Engine(name='engine1')
    engine1.add(adagio.LongOnly(**longonly_params))
    engine1.add(adagio.VolatilityScaling(**lo_vol_scale_params))
    engine1.add(adagio.Signal(**signal_params))

    engine2 = adagio.Engine(name='engine2')
    engine2.add(adagio.LongOnly(**longonly_params))
    engine2.add(adagio.VolatilityScaling(**lo_vol_scale_params))
    engine2.add(adagio.Signal(**signal_params))

    engine3 = adagio.Engine(name='engine3')
    engine3.add([engine1, engine2])
    engine3.add(adagio.Portfolio(**portfolio_params))
    engine3.add(adagio.PortVolatilityScaling(**portfolio_vol_scale_params))
    engine3.backtest()

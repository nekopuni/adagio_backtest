import adagio
from adagio import keys

from adagio_backtest.config import *
from adagio.utils.mongo import get_library

adagio.AdagioConfig.quandl_token = QUANDL_TOKEN

if __name__ == '__main__':
    library = get_library(keys.backtest)

    # common parameters
    lo_vol_scale_params = {
        keys.vs_chg_rule: '+Wed-1bd+1bd',
        keys.vs_target_vol: 0.1,
        keys.vs_method_params: {
            keys.vs_method: keys.vs_ewm,
            keys.vs_ewm_halflife: 21,
        }
    }
    momentum_params = {
        keys.signal_method_params: {
            keys.signal_method: keys.signal_trend_ma_xover,
            keys.signal_windows: [[8, 24], [16, 48], [32, 96]],
        },
        keys.signal_chg_rule: '+Wed-1bd+1bd',
        keys.signal_to_position: keys.linear,
        keys.position_cap: 1.0,
        keys.position_floor: -1.0
    }
    portfolio_params = {
        keys.weighting: keys.equal_weight,
        keys.port_weight_chg_rule: '+Wed-1bd+1bd',
    }
    port_vol_scale_params = {
        keys.vs_chg_rule: '+Wed-1bd+1bd',
        keys.vs_target_vol: 0.1,
        keys.vs_method_params: {
            keys.vs_method: keys.vs_ewm,
            keys.vs_ewm_halflife: 63,
        }
    }

    # parameters by asset-class
    equity_dm_lo_params = {
        keys.lo_ticker: ['CME_ES', 'CME_NQ', 'CME_YM', 'CME_MD', 'ICE_RF',
                         'CME_NK', 'EUREX_FESX', 'EUREX_FDAX',
                         'EUREX_FSMI', 'LIFFE_FCE', 'LIFFE_Z', 'LIFFE_FTI',
                         'CFFEX_IF', 'MX_SXF'],
        keys.slippage: 2.0,
    }
    equity_em_lo_params = {
        keys.lo_ticker: ['SGX_IN', 'LIFFE_PSI', 'SGX_ID', 'SGX_SG', 'SGX_TW'],
        keys.slippage: 2.0,
    }
    rates_lo_params = {
        keys.lo_ticker: ['CME_TU', 'CME_FV', 'CME_TY', 'CME_US', 'CME_UL',
                         'EUREX_FGBS', 'EUREX_FGBM', 'EUREX_FGBL', 'EUREX_FGBX',
                         'EUREX_FBTS', 'EUREX_FBTP', 'EUREX_FOAT', 'MX_CGB',
                         'LIFFE_R', 'SGX_JB'],
        keys.slippage: 2.0,
    }
    fx_dm_lo_params = {
        keys.lo_ticker: ['CME_EC', 'CME_JY', 'CME_BP', 'CME_SF', 'CME_CD',
                         'CME_AD', 'CME_NE'],
        keys.slippage: 2.0,
    }
    fx_em_lo_params = {
        keys.lo_ticker: ['CME_MP', 'CME_RU', 'CME_BR', 'CME_RA'],
        keys.slippage: 2.0,
    }
    comdty_energy_lo_params = {
        keys.lo_ticker: ['CME_CL', 'CME_HO', 'CME_RB', 'CME_NG', 'ICE_B',
                         'ICE_G', 'ICE_M'],
        keys.slippage: 2.0,
    }
    comdty_grains_lo_params = {
        keys.lo_ticker: ['CME_C', 'CME_W', 'CME_S', 'CME_KW', 'ICE_RS',
                         'LIFFE_EBM', 'LIFFE_ECO', 'MGEX_MW'],
        keys.slippage: 2.0,
    }
    comdty_softs_lo_params = {
        keys.lo_ticker: ['ICE_SB', 'ICE_KC', 'ICE_CT', 'ICE_CC', 'ICE_OJ',
                         'LIFFE_W'],
        keys.slippage: 2.0,
    }
    comdty_agri_lo_params = {
        keys.lo_ticker: ['CME_LC', 'CME_FC', 'CME_LN', 'CME_DA', 'CME_BO',
                         'CME_SM'],
        keys.slippage: 2.0,
    }
    comdty_metal_lo_params = {
        keys.lo_ticker: ['CME_GC', 'CME_SI', 'CME_PL', 'CME_PA', 'CME_HG'],
        keys.slippage: 2.0,
    }

    # Equity Developed markets
    engine_equity_dm = adagio.Engine(name='Equity DM Trend-following')
    engine_equity_dm.add(adagio.LongOnly(**equity_dm_lo_params))
    engine_equity_dm.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                                  **lo_vol_scale_params))
    engine_equity_dm.add(adagio.Signal(**momentum_params))
    engine_equity_dm.add(adagio.Portfolio(name='equity_port',
                                          **portfolio_params))
    engine_equity_dm.add(adagio.PortVolatilityScaling(name='equity_port_vs',
                                                      **port_vol_scale_params))

    # Equity Emerging markets
    engine_equity_em = adagio.Engine(name='Equity EM Trend-following')
    engine_equity_em.add(adagio.LongOnly(**equity_em_lo_params))
    engine_equity_em.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                                  **lo_vol_scale_params))
    engine_equity_em.add(adagio.Signal(**momentum_params))
    engine_equity_em.add(adagio.Portfolio(name='equity_port',
                                          **portfolio_params))
    engine_equity_em.add(adagio.PortVolatilityScaling(name='equity_port_vs',
                                                      **port_vol_scale_params))

    # Rates
    engine_rates = adagio.Engine(name='Rates Trend-following')
    engine_rates.add(adagio.LongOnly(**rates_lo_params))
    engine_rates.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                              **lo_vol_scale_params))
    engine_rates.add(adagio.Signal(**momentum_params))
    engine_rates.add(adagio.Portfolio(name='rates_port', **portfolio_params))
    engine_rates.add(adagio.PortVolatilityScaling(name='rates_port_vs',
                                                  **port_vol_scale_params))

    # FX Developed markets
    engine_fx_dm = adagio.Engine(name='FX DM Trend-following')
    engine_fx_dm.add(adagio.LongOnly(**fx_dm_lo_params))
    engine_fx_dm.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                              **lo_vol_scale_params))
    engine_fx_dm.add(adagio.Signal(**momentum_params))
    engine_fx_dm.add(adagio.Portfolio(name='fx_dm_port', **portfolio_params))
    engine_fx_dm.add(adagio.PortVolatilityScaling(name='fx_dm_port_vs',
                                                  **port_vol_scale_params))

    # FX Emerging markets
    engine_fx_em = adagio.Engine(name='FX EM Trend-following')
    engine_fx_em.add(adagio.LongOnly(**fx_em_lo_params))
    engine_fx_em.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                              **lo_vol_scale_params))
    engine_fx_em.add(adagio.Signal(**momentum_params))
    engine_fx_em.add(adagio.Portfolio(name='fx_em_port', **portfolio_params))
    engine_fx_em.add(adagio.PortVolatilityScaling(name='fx_em_port_vs',
                                                  **port_vol_scale_params))

    # Commodity energy futures
    engine_energy = adagio.Engine(name='Energy Trend-following')
    engine_energy.add(adagio.LongOnly(**comdty_energy_lo_params))
    engine_energy.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                               **lo_vol_scale_params))
    engine_energy.add(adagio.Signal(**momentum_params))
    engine_energy.add(adagio.Portfolio(name='energy_port', **portfolio_params))
    engine_energy.add(adagio.PortVolatilityScaling(name='energy_port_vs',
                                                   **port_vol_scale_params))

    # Commodity grain futures
    engine_grains = adagio.Engine(name='Grain Trend-following')
    engine_grains.add(adagio.LongOnly(**comdty_grains_lo_params))
    engine_grains.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                               **lo_vol_scale_params))
    engine_grains.add(adagio.Signal(**momentum_params))
    engine_grains.add(adagio.Portfolio(name='grain_port', **portfolio_params))
    engine_grains.add(adagio.PortVolatilityScaling(name='grain_port_vs',
                                                   **port_vol_scale_params))

    # Commodity soft futures
    engine_soft = adagio.Engine(name='Soft Trend-following')
    engine_soft.add(adagio.LongOnly(**comdty_softs_lo_params))
    engine_soft.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                             **lo_vol_scale_params))
    engine_soft.add(adagio.Signal(**momentum_params))
    engine_soft.add(adagio.Portfolio(name='soft_port', **portfolio_params))
    engine_soft.add(adagio.PortVolatilityScaling(name='soft_port_vs',
                                                 **port_vol_scale_params))

    # Commodity agriculture futures
    engine_agri = adagio.Engine(name='Agri Trend-following')
    engine_agri.add(adagio.LongOnly(**comdty_agri_lo_params))
    engine_agri.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                             **lo_vol_scale_params))
    engine_agri.add(adagio.Signal(**momentum_params))
    engine_agri.add(adagio.Portfolio(name='agri_port', **portfolio_params))
    engine_agri.add(adagio.PortVolatilityScaling(name='agri_port_vs',
                                                 **port_vol_scale_params))

    # Commodity metal futures
    engine_metal = adagio.Engine(name='Metal Trend-following')
    engine_metal.add(adagio.LongOnly(**comdty_metal_lo_params))
    engine_metal.add(adagio.VolatilityScaling(name='vs_pre_signal',
                                              **lo_vol_scale_params))
    engine_metal.add(adagio.Signal(**momentum_params))
    engine_metal.add(adagio.Portfolio(name='metal_port', **portfolio_params))
    engine_metal.add(adagio.PortVolatilityScaling(name='metal_port_vs',
                                                  **port_vol_scale_params))

    # Momentum strategy basket
    engine_momentum = adagio.Engine(name='Trend-following benchmark')
    engine_momentum.add([engine_equity_dm, engine_equity_em,
                         engine_rates, engine_fx_dm, engine_fx_em,
                         engine_energy, engine_grains,
                         engine_soft, engine_agri, engine_metal])
    engine_momentum.add(
        adagio.Portfolio(weighting=[1 / 4 * 0.9,  # equity dm
                                    1 / 4 * 0.1,  # equity em
                                    1 / 4,  # rates
                                    1 / 4 * 2 / 3,  # fx dm
                                    1 / 4 * 1 / 3,  # fx em
                                    1 / 4 * 0.2,  # energy
                                    1 / 4 * 0.2,  # grains
                                    1 / 4 * 0.2,  # soft
                                    1 / 4 * 0.2,  # agri
                                    1 / 4 * 0.2  # metal
                                    ])
    )
    engine_momentum.add(adagio.PortVolatilityScaling(**port_vol_scale_params))
    engine_momentum.backtest()
    library.write(engine_momentum.symbol, engine_momentum,
                  metadata=engine_momentum.all_params)

from cadCAD_tools import easy_run
import pandas as pd
from .parts.uniswap_model import *

PSUBs = [
    {
        'policies': {
            'user_action': p_actionDecoder
        },
        'variables': {
            'RAI_balance': s_mechanismHub_RAI,
            'ETH_balance': s_mechanismHub_ETH,
            'UNI_supply': s_mechanismHub_UNI,
            'price_ratio': s_price_ratio
        }
    }

]

genesis_states = {
    'RAI_balance': None,
    'ETH_balance': None,
    'UNI_supply': None,
    'price_ratio': None
}

sys_params = {
    'fee_numerator': [997, 997, 997, 997,
                        995, 995, 995, 995],
    'fee_denominator': [1000],
    'uniswap_events': [pd.read_csv('../data/clean_graph_data.csv')],
    'fix_cost': [-1], # -1 to deactivate
    'retail_precision': [3,3,15,15,
                3,3,15,15],
    'retail_tolerance': [0.0005, 0.025, 0.0005, 0.025,
                        0.0005, 0.025, 0.0005, 0.025]
}
def run_model() -> pd.DataFrame:
    events = sys_params['uniswap_events'][0]
    first_row = events.iloc[0]
    
    genesis_states.update(RAI_balance=first_row.token_balance,
                          ETH_balance=first_row.eth_balance,
                          UNI_supply=first_row.UNI_supply)
    
    N_t = len(events) - 2
    #N_t = 100
    
    
    df = easy_run(genesis_states,
                  sys_params,
                  PSUBs,
                  N_t,
                  1.0,
                  assign_params=False)
    
    return df


run_model()
import pandas as pd

sys_params = {
    'fee_numerator': [997, 997, 997, 997,
                        995, 995, 995, 995],
    'fee_denominator': [1000],
    'uniswap_events': [pd.read_csv('./data/clean_graph_data.csv')],
    'fix_cost': [-1], # -1 to deactivate
    'retail_precision': [3,3,15,15,
                3,3,15,15],
    'retail_tolerance': [0.0005, 0.025, 0.0005, 0.025,
                        0.0005, 0.025, 0.0005, 0.025]
}

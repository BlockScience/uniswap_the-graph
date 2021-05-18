import pandas as pd

SIMULATION_TIME_STEPS = len(pd.read_csv('./data/clean_graph_data.csv'))-2
MONTE_CARLO_RUNS = 1

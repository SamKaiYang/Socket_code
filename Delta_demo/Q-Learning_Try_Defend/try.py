import pandas as pd
import numpy as np

player1_q_table = pd.read_csv("~/PycharmProjects/Q-learning_Try/player1_q_table.csv", index_col="Unnamed: 0")
player1_q_table = pd.DataFrame(player1_q_table)

player1_q_table.columns = player1_q_table.columns.astype(np.int64)

print(player1_q_table.columns)

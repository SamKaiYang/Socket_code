import checkerboard as cb
import numpy as np
import pandas as pd

height = cb.Initial().height
width = cb.Initial().width
player1 = cb.Initial().players[0]
player2 = cb.Initial().players[1]


class QLearningTable(object):

    def __init__(self, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = list(range(height * width))
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        # self.player1_q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        # self.player2_q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        player1_q_table = pd.read_csv("~/Desktop/Q-Learning_Try_Defend/player1_q_table_15000.csv", index_col="Unnamed: 0")
        self.player1_q_table = pd.DataFrame(player1_q_table, dtype=np.float64)
        player1_q_table.columns = player1_q_table.columns.astype(np.int64)
        player2_q_table = pd.read_csv("~/Desktop/Q-Learning_Try_Defend/player2_q_table_15000.csv", index_col="Unnamed: 0")
        self.player2_q_table = pd.DataFrame(player2_q_table, dtype=np.float64)
        player2_q_table.columns = player2_q_table.columns.astype(np.int64)

    def choose_action(self, player, observation, int_observation):
        action = -1

        self.check_state_exist(player, observation)

        if player == player1:
            self.q_table = self.player1_q_table

        elif player == player2:
            self.q_table = self.player2_q_table

        # action selection

        unempty = 1

        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]

            while unempty:
                # choose best action
                unempty = 0
                # some actions may have the same value, randomly choose on in these actions
                action = np.random.choice(state_action[state_action == np.max(state_action)].index)

                if int_observation[int(action)] != 0:
                    unempty = 1
                    state_action[int(action)] = -1000000

        else:

            while unempty:
                # choose random action
                unempty = 0
                action = np.random.choice(self.actions)

                if int_observation[int(action)] != 0:
                    unempty = 1

        return action

    def learn(self, player, s, a, r, s_, endgame):
        self.check_state_exist(player, s_)

        if player == player1:
            self.q_table = self.player1_q_table

        elif player == player2:
            self.q_table = self.player2_q_table

        q_predict = self.q_table.loc[s, a]
        if endgame != 1:
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

        if player == player1:
            self.player1_q_table = self.q_table

        elif player == player2:
            self.player2_q_table = self.q_table

    def check_state_exist(self, player, state):

        if player == player1:
            self.q_table = self.player1_q_table

        elif player == player2:
            self.q_table = self.player2_q_table

        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*(len(self.q_table.columns)),
                    index=self.q_table.columns,
                    name=state,
                )
            )

        if player == player1:
            self.player1_q_table = self.q_table

        elif player == player2:
            self.player2_q_table = self.q_table

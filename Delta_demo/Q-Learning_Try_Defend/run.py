from Q_Learning_brain import QLearningTable
import checkerboard as cb
import time
from socket import *

host = "127.0.1.1"  # one computer -> terminal -> hostname -i
# host = "192.168.43.135" # two computer -> terminal -> hosname -I
port = 8080
ADDR = (host, port)
BUFSIZ = 1024

tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.bind(ADDR)
# set the max number of tcp connection
tcpSocket.listen(5)
print('waiting for connection...')
clientSocket, clientAddr = tcpSocket.accept()
print('conneted form: %s', str(clientAddr))

height = cb.Initial().height
width = cb.Initial().width
player1 = cb.Initial().players[0]
player2 = cb.Initial().players[1]
player = cb.Initial().StartPlayer
column = cb.Initial().column
win_line = cb.Initial().win_line
piece = cb.Board().reset()
sleep = 1
step = 0
draw_cnt = 0
win1_cnt = 0
win2_cnt = 0

QL = QLearningTable()

print("\n\n\n\n\n\n\n\n\n\n\n\nStart Game\n")

time.sleep(sleep)

for i_episode in range(5000):

    observation = cb.Board().reset()
    step = 0
    # player = player1

    # print("empty with 0")
    # print("Player 1 :", "{0:8}".format(player1), "with -1")
    # print("Player 2 :", "{0:8}".format(player2), "with  1")
    #
    # cb.Board().boardstate(observation)
    # print("\n")

    while True:

        # print("Turn to " + player)

        if player != "Human":

            one_order_observation = observation.flatten('C')

            list_one_order_observation = one_order_observation.tolist()

            action = QL.choose_action(player, str(list_one_order_observation), one_order_observation)

            observation_, action = cb.Action().get_action(player, observation, action, QL)

            data = str(action)

            step += 1

            if player == player1:
                clientSocket.send(data.encode('utf-8'))
                returnData = clientSocket.recv(BUFSIZ)
                if not returnData:
                    print("No returnData!")
                    break
                print("\nStep: %d" % step)
                print('Successful! receive acton is: %s' % returnData.decode('utf-8'))

                time.sleep(2)

            endgame = cb.Board().check_computer_boardstate_endgame(player, observation_)

            # if endgame != 1 and step == win_line:
            #
            #     reward = 0
            #
            #     endgame = 1
            #
            # else:

            reward = cb.Board().check_computer_boardstate_reward(player, observation_, action)

            one_order_observation_ = observation_.flatten('C')

            list_one_order_observation_ = one_order_observation_.tolist()

            QL.learn(player, str(list_one_order_observation), action, reward, str(list_one_order_observation_), endgame)

            # cb.Board().boardstate(observation_)
            #
            # y = action // width
            # x = action - y * width
            #
            # print("\n\n" + player + "'s move: ", end='')
            # print(str(y) + "," + str(column[x]))

        else:
            observation_ = cb.Action().get_action(player, observation, None, QL)

            endgame = cb.Board().check_human_boardstate(observation_)

            # cb.Board().boardstate(observation_)
            #
            # print("\n")

        if endgame == 1 or step == height * width:
            # calculate running

            print('\n' * 50)

            cb.Board().boardstate(observation_)

            print("\n\n")

            print(i_episode)

            end = str("11111111111111111111111111111111111111111111111111111111111111111111111111111111")

            clientSocket.send(end.encode('utf-8'))
            returnEnd = clientSocket.recv(BUFSIZ)
            if not returnEnd:
                print("No returnEnd!")
            else:
                print("receive endgame\n")

            QL.player1_q_table.to_csv("~/Desktop/Q-Learning_Try_Defend/player1_q_table_test.csv")
            QL.player2_q_table.to_csv("~/Desktop/Q-Learning_Try_Defend/player2_q_table_test.csv")

            if endgame != 1:
                draw_cnt += 1
                # print("\n\n\n draw!!")

            else:
                if player == player1:
                    win1_cnt += 1

                elif player == player2:
                    win2_cnt += 1

                # print("\n\n\n" + player + " win!!")

            # print('\n' * 50)
            # print(QL.player1_q_table.columns[0])
            # print('\n' * 50)
            # print(" draw " + str(draw_cnt) + " times")
            # print(player1 + " win " + str(win1_cnt) + " times")
            # print(player2 + " win " + str(win2_cnt) + " times")
            # print("\n\n\n\n\n\n\n\n\n\n")
            # print("Game End\n\n")

            if player == player1:
                win1_cnt += 1
            elif player == player2:
                win2_cnt += 1

            break

        observation = observation_

        if player == player1:
            player = player2
        elif player == player2:
            player = player1

clientSocket.close()
tcpSocket.close()

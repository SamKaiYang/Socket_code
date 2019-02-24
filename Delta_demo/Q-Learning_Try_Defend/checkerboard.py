import numpy as np


class Initial(object):

    def __init__(self):
        self.height = 4
        self.width = 4
        self.win_line = 3
        self.players = ["Computer1", "Computer2"]
        self.StartPlayer = self.players[0]
        self.column = [i for i in 'abcdefghijklmnopqrstuvwxyz']


class Board(object):

    def __init__(self):
        self.size = list(range(Initial().height * Initial().width))
        self.reward = [[0, 10, 40, 80, 200, 480, 1000, 1200, 1800, 3000, 10000],
                       [0, 15, 50, 100, 230, 600, 1200, 1800, 2100, 5000, 100000]]

    def reset(self):
        piece = np.zeros((Initial().height, Initial().width), dtype=np.int32)
        return piece

    def boardstate(self, piece):
        for x in range(Initial().height - 1, -1, -1):
            print("\n\n")
            print("{0:4}".format(x), end='')
            print("{0:4}".format(piece[x][0]), end='')
            for y in range(1, Initial().width, 1):
                print("{0:8}".format(piece[x][y]), end='')
        print("\n\n{0:7}".format(" "), end='')
        for z in range(0, Initial().width):
            print("{0:8}".format(Initial().column[z]), end='')

    def check_human_boardstate(self, piece):
        playerstate = 1
        endgame = 0

        for y in range(Initial().height - 1, -1, -1):
            for x in range(0, Initial().width - 4, 1):
                linepoint = 0
                for i in range(5):
                    if piece[y][x+i] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * 5:
                            endgame = 1
                            return endgame

        for x in range(Initial().width):
            for y in range(Initial().height - 1, 3, -1):
                linepoint = 0
                for i in range(5):
                    if piece[y-i][x] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * 5:
                            endgame = 1
                            return endgame

        for y in range(Initial().height - 1, 3, -1):
            for x in range(0, Initial().width - 4, 1):
                linepoint = 0
                for i in range(5):
                    if piece[y-i][x+i] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * 5:
                            endgame = 1
                            return endgame

        for y in range(Initial().height - 1, 3, -1):
            for x in range(Initial().width - 1, 3, -1):
                linepoint = 0
                for i in range(5):
                    if piece[y-i][x-i] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * 5:
                            endgame = 1
                            return endgame

        return endgame

    def check_computer_boardstate_endgame(self, player, piece):
        endgame = 0
        playerstate = 0

        if player == Initial().players[0]:
            playerstate = -1

        elif player == Initial().players[1]:
            playerstate = 1

        for y in range(Initial().height - 1, -1, -1):
            for x in range(0, Initial().width - (Initial().win_line - 1), 1):
                linepoint = 0
                for i in range(Initial().win_line):
                    if piece[y][x+i] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * Initial().win_line:
                            endgame = 1
                            return endgame

        for x in range(Initial().width):
            for y in range(Initial().height - 1, Initial().win_line - 2, -1):
                linepoint = 0
                for i in range(Initial().win_line):
                    if piece[y-i][x] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * Initial().win_line:
                            endgame = 1
                            return endgame

        for y in range(Initial().height - 1, Initial().win_line - 2, -1):
            for x in range(0, Initial().width - (Initial().win_line - 1), 1):
                linepoint = 0
                for i in range(Initial().win_line):
                    if piece[y-i][x+i] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * Initial().win_line:
                            endgame = 1
                            return endgame

        for y in range(Initial().height - 1, Initial().win_line - 2, -1):
            for x in range(Initial().width - 1, Initial().win_line - 2, -1):
                linepoint = 0
                for i in range(Initial().win_line):
                    if piece[y-i][x-i] == playerstate:
                        linepoint += playerstate
                        if linepoint == playerstate * Initial().win_line:
                            endgame = 1
                            return endgame

        return endgame

    def check_computer_boardstate_reward(self, player, piece, action):
        y = action // Initial().width
        x = action - y * Initial().width

        playerstate = -2

        if player == Initial().players[0]:
            playerstate = -1

        elif player == Initial().players[1]:
            playerstate = 1

        a = int(self.LeftRight(piece, y, x, playerstate, player)) + int(self.BottomTop(piece, y, x, playerstate, player)) \
            + int(self.LeftBottom(piece, y, x, playerstate, player)) + int(self.LeftTop(piece, y, x, playerstate, player))
        b = int(self.LeftRight(piece, y, x, -playerstate, player)) + int(self.BottomTop(piece, y, x, -playerstate, player)) \
            + int(self.LeftBottom(piece, y, x, -playerstate, player)) + int(self.LeftTop(piece, y, x, -playerstate, player))
        reward = a - b

        return reward

    def LeftRight(self, piece, y, x, playerstate, player):

        maxreward = 0

        for j in range(0, Initial().win_line, 1):
            death = 0
            live = 0
            count = 1

            for i in range(1, Initial().win_line - j, 1):
                if x - i < 0 or piece[y][x - i] == -playerstate:
                    death += 1
                    break

                elif piece[y][x - i] == 0:
                    live += 1

                elif piece[y][x - i] == playerstate:
                    count += 1

            if j != 0:
                for i in range(1, j + 1, 1):
                    if x + i >= Initial().width or piece[y][x + i] == -playerstate:
                        death += 1
                        break

                    elif piece[y][x + i] == 0:
                        live += 1

                    elif piece[y][x + i] == playerstate:
                        count += 1

            reward = self.model(count, live, death, playerstate, player)

            if reward > maxreward:
                maxreward = reward

        return maxreward

    def BottomTop(self, piece, y, x, playerstate, player):

        maxreward = 0

        for j in range(0, Initial().win_line, 1):
            death = 0
            live = 0
            count = 1

            for i in range(1, Initial().win_line - j, 1):
                if y - i < 0 or piece[y - i][x] == -playerstate:
                    death += 1
                    break

                elif piece[y - i][x] == 0:
                    live += 1

                elif piece[y - i][x] == playerstate:
                    count += 1

            if j != 0:
                for i in range(1, j + 1, 1):
                    if y + i >= Initial().height or piece[y + i][x] == -playerstate:
                        death += 1
                        break

                    elif piece[y + i][x] == 0:
                        live += 1

                    elif piece[y + i][x] == playerstate:
                        count += 1

            reward = self.model(count, live, death, playerstate, player)

            if reward > maxreward:
                maxreward = reward

        return maxreward

    def LeftBottom(self, piece, y, x, playerstate, player):

        maxreward = 0

        for j in range(0, Initial().win_line, 1):
            death = 0
            live = 0
            count = 1

            for i in range(1, Initial().win_line - j, 1):
                if y + i >= Initial().height or x - i < 0 or piece[y + i][x - i] == -playerstate:
                    death += 1
                    break

                elif piece[y + i][x - i] == 0:
                    live += 1

                elif piece[y + i][x - i] == playerstate:
                    count += 1

            if j != 0:
                for i in range(1, j + 1, 1):
                    if y - i < 0 or x + i >= Initial().width or piece[y - i][x + i] == -playerstate:
                        death += 1
                        break

                    elif piece[y - i][x + i] == 0:
                        live += 1

                    elif piece[y - i][x + i] == playerstate:
                        count += 1

            reward = self.model(count, live, death, playerstate, player)

            if reward > maxreward:
                maxreward = reward

        return maxreward

    def LeftTop(self, piece, y, x, playerstate, player):

        maxreward = 0

        for j in range(0, Initial().win_line, 1):
            death = 0
            live = 0
            count = 1

            for i in range(1, Initial().win_line - j, 1):
                if y - i < 0 or x - i < 0 or piece[y - i][x - i] == -playerstate:
                    death += 1
                    break

                elif piece[y - i][x - i] == 0:
                    live += 1

                elif piece[y - i][x - i] == playerstate:
                    count += 1

            if j != 0:
                for i in range(1, j + 1, 1):
                    if y + i >= Initial().height or x + i >= Initial().width or piece[y + i][x + i] == -playerstate:
                        death += 1
                        break

                    elif piece[y + i][x + i] == 0:
                        live += 1

                    elif piece[y + i][x + i] == playerstate:
                        count += 1

            reward = self.model(count, live, death, playerstate, player)

            if reward > maxreward:
                maxreward = reward

        return maxreward

    def model(self, count, live, death, playerstate, player):
        reward = 0

        if player == Initial().players[0]:
            if playerstate == -1:
                reward = self.reward[0]

            elif playerstate == 1:
                reward = self.reward[1]

        elif player == Initial().players[1]:
            if playerstate == -1:
                reward = self.reward[1]

            elif playerstate == 1:
                reward = self.reward[0]

        if count == 1:
            if death == 1:
                return reward[1]  # sleep one

            elif death == 0:
                return reward[2]  # alive one

        elif count == 2:
            if death == 1:
                return reward[3]  # sleep two

            elif death == 0 and live >= 1:
                return reward[4]  # (big) jump alive two

        elif count == 3:
            if death == 1:
                return reward[5]  # sleep three

            elif death == 0 and live == 1:
                return reward[6]  # jump alive three

            elif death == 0:
                return reward[7]  # alive three

        elif count == 4:
            if death == 1:
                return reward[8]  # resist four

            elif death == 0:
                return reward[9]  # alive four

        elif count == 5:
            return reward[10]  # get five

        return reward[0]


class Action(object):

    def get_action(self, player, piece, action, QL):
        error = 0
        notempty = 0
        piece_ = piece

        try:
            location = []
            if player != "Human":
                # print(player + "'s move: ", end='')
                y = action // Initial().width
                x = action - y * Initial().width

                # print(str(y) + "," + str(Initial().column[x]))

                for i in range(Initial().height):
                    error = 1
                    if y == i:
                        error = 0
                        break

                if error == 0:
                    for i in range(Initial().width):
                        error = 1
                        if x == i:
                            error = 0
                            break

                location.append(str(y))
                location.append(str(x))

            elif player == "Human":
                location = input(player + "'s move: ")
                x = -1

                if isinstance(location, str):  # for python3
                    location = [n for n in location.split(",")]

                    for i in range(Initial().height):
                        error = 1
                        if location[0] == str(i):
                            error = 0
                            break

                    if error == 0:
                        for i in range(Initial().width):
                            error = 1
                            x += 1
                            if location[1] == Initial().column[i]:
                                location[1] = x
                                error = 0
                                break

            # if error == 1:
                # Board().boardstate(piece)
                # print("\n\nNot correct type")

            if len(location) != 2 and error == 0:
                # Board().boardstate(piece)
                # print("\n\nlength error!!")
                error = 1

            y = int(location[0])
            x = int(location[1])
            w = Initial().width
            move = y * w + x

            if move in Board().size:
                if piece[y][x] != 0 and error == 0:
                    # Board().boardstate(piece)
                    # print("\n\nThe location is not empty!!")
                    notempty = 1

                elif error == 0:
                    piece_ = self.location_to_move(player, location, piece)

            else:
                error = 1

        except Exception as e:
            if error == 0:
                # print("\n\nException!!")
                error = 1

        if error == 1:
            # print("invalid move")
            # print("Turn to " + player)
            piece_ = self.get_action(player, piece, action, QL)

        if notempty == 1:
            one_order_piece = piece.flatten('C')

            list_one_order_piece = one_order_piece.tolist()

            action = QL.choose_action(player, str(list_one_order_piece), one_order_piece)

            piece_, action = self.get_action(player, piece, action, QL)

        return piece_, action

    def location_to_move(self, player, location, piece):
        y = int(location[0])
        x = int(location[1])

        if player == Initial().players[0]:
            piece[y][x] = -1
        elif player == Initial().players[1]:
            piece[y][x] = 1

        return piece


class CheckProbability(object):

    def checkempty(self, probability, piece):
        cnt = 0
        number = 0
        for i in range(Initial().height * Initial().width):
            if piece[0][i] != 0:
                number += probability[0][i]
                probability[0][i] = 0
                cnt += 1

        if cnt != 0:
            for i in range(Initial().height * Initial().width):
                if probability[0][i] != 0:
                    probability[0][i] += (number / (Initial().height * Initial().width - cnt))

        return probability

if __name__ == "__main__":
    pass

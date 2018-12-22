"""
This class defines a game and state of connect four
States are given by 2-element tuples containing the game board and the player who's turn it is
    Game boards are given by 2D numpy arrays of integers, 0 for no player, 1 for active player, 2 for opposing player
    1 corresponds to the agent (active) player
    2 corresponds to the opposing player
"""
import numpy as np

class ConnectFourGame:
    # Board size is a two-element tuple (height, width)
    def __init__(self, board_size = (6, 7), first_to_move = 1, match_length=4):
        self.board_size = board_size
        self.num_rows = board_size[0]
        self.num_cols = board_size[1]
        self.first_to_move = first_to_move
        self.match_length = match_length

    def start_state(self):
        return (np.zeros(self.board_size, dtype=int), self.first_to_move)

    def actions(self, state):
        actions = []
        for i in range(self.num_cols):
            if state[0][0,i] == 0:
                actions.append(i)
        return actions

    # Assume the move is legal  
    def successor(self, state, action):
        new_board = state[0].copy()
        for i in range(self.num_rows - 1, -1, -1):
            if new_board[i, action] == 0:
                new_board[i, action] = state[1]
                break

        return (new_board, 3 - state[1])

    # Returns a two-element tuple with the game end state and winner
    # (False, 0) for an in-progress gmae
    # (True, 1) or (True, 2) for a game that has been won by either player
    def is_end(self, state):
        board = state[0]

        for i in range(self.num_rows):
            row = board[i,:]
            for j in range(self.num_cols - self.match_length + 1):
                if len(np.unique(np.array(row[j:j+self.match_length]))) == 1:
                    if row[j] != 0:
                        return (True, row[j])

        for i in range(self.num_cols):
            col = board[:,i]
            for j in range(self.num_rows - self.match_length + 1):
                if len(np.unique(np.array(col[j:j+self.match_length]))) == 1:
                    if col[j] != 0:
                        return (True, col[j])

        for row in range(self.num_rows - self.match_length + 1):
            for col in range(self.num_cols):
                first = board[row][col]
                if first == 0:
                    continue

                if col + self.match_length <= self.num_cols:
                    matched = True
                    for i in range(1, self.match_length):
                        if board[row + i][col + i] != first:
                            matched = False
                            break
                    if matched:
                        return (True, first)

                if col - self.match_length + 1 >= 0:
                    matched = True
                    for i in range(1, self.match_length):
                        if board[row + i][col - i] != first:
                            matched = False
                            break
                    if matched:
                        return (True, first)

        if len(self.actions(state)) == 0:
            return (True, 0)

        return (False, 0)

    def print_state(self, state):
        self.print_board(state[0])
        print(str(state[1]) + " to move")

    def print_board(self, board):
        print ("-" * (self.num_cols * 5 + 1))
        for row in range(self.num_rows):
            line = "| "
            for col in range(self.num_cols):
                if board[row][col] == 0:
                    c = " "
                elif board[row][col] == 1:
                    c = "$"
                else:
                    c = "*"
                line += c * 2 + " | "
            print(line)
            print(line)
            print ("-" * (self.num_cols * 5 + 1))

    def player(self, state):
        return state[1]
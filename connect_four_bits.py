"""
This class defines a game and state of connect four
States are given by 3-element tuples containing the game board and the player who's turn it is
    Game boards are given by two 2D numpy arrays of booleans, the first representing the first player's pieces, the second representing the second player's pieces
    1 corresponds to the agent (active) player
    2 corresponds to the opposing player
"""
import numpy as np

class ConnectFourGameBits:
    # Board size is a two-element tuple (height, width)
    def __init__(self, board_size = (6, 7), first_to_move = 1, match_length=4):
        self.board_size = board_size
        self.num_rows = board_size[0]
        self.num_cols = board_size[1]
        self.first_to_move = first_to_move
        self.match_length = match_length
        self.generate_victory_masks()

    def generate_victory_masks(self):
        num_masks = 0
        num_masks += self.num_rows * (self.num_cols - self.match_length + 1)
        num_masks += self.num_cols * (self.num_rows - self.match_length + 1)
        num_masks += (self.num_cols - self.match_length + 1) * (self.num_rows - self.match_length + 1) * 2
        self.masks = np.zeros((num_masks, self.num_rows, self.num_cols), dtype=bool)

        index = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols - self.match_length + 1):
                for i in range(self.match_length):
                    self.masks[index][row][col + i] = True
                index += 1

        for col in range(self.num_cols):
            for row in range(self.num_rows - self.match_length + 1):
                for i in range(self.match_length):
                    self.masks[index][row + i][col] = True
                index += 1

        for row in range(self.num_rows - self.match_length + 1):
            for col in range(self.num_cols - self.match_length + 1):
                for i in range(self.match_length):
                    self.masks[index][row + i][col + i] = True
                index += 1

        for row in range(self.num_rows - self.match_length + 1):
            for col in range(self.match_length - 1, self.num_cols):
                for i in range(self.match_length):
                    self.masks[index][row + i][col - i] = True
                index += 1

        assert index == num_masks

    def start_state(self):
        return (np.zeros(self.board_size, dtype=bool), np.zeros(self.board_size, dtype=bool), self.first_to_move)

    def actions(self, state):
        return list(np.where(np.logical_not(np.logical_or(state[0][0], state[1][0])))[0])

    def successor(self, state, action):
        new_state = (state[0].copy(), state[1].copy(), 3 - state[2])

        combined = np.logical_or(state[0][:,action], state[1][:,action])
        row = self.num_rows - 1 - len(np.where(combined)[0])
        new_state[state[2] - 1][row, action] = True
        return new_state

    # Returns a two-element tuple with the game end state and winner
    # (False, 0) for an in-progress gmae
    # (True, 1) or (True, 2) for a game that has been won by either player
    # (True, 0) for a game that ended in a tie
    def is_end(self, state):
        # the only winner could be the last player
        board = state[2 - state[2]]
        if sum(np.all(np.logical_or(np.logical_not(self.masks), board), axis=(1,2))) > 0:
            return (True, 3 - state[2])

        if np.all(np.logical_or(state[0], state[1])):
            return (True, 0)

        return (False, 0)

    def print_state(self, state):
        self.print_board(state[0], state[1])
        print(str(state[2]) + " to move")

    def print_board(self, p1_board, p2_board):
        print ("-" * (self.num_cols * 5 + 1))
        for row in range(self.num_rows):
            line = "| "
            for col in range(self.num_cols):
                if p1_board[row][col]:
                    c = "$"
                elif p2_board[row][col]:
                    c = "*"
                else:
                    c = " "
                line += c * 2 + " | "
            print(line)
            print(line)
            print ("-" * (self.num_cols * 5 + 1))

    def player(self, state):
        return state[1]
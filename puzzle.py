import random

class Puzzle:
    def __init__(self):
        self.board = list(range(1, 16)) + [0]
        self.moves = 0

    def scramble(self):
        random.shuffle(self.board)
        self.moves = 0

    def move(self, index):
        empty = self.board.index(0)
        row1, col1 = divmod(index, 4)
        row2, col2 = divmod(empty, 4)

        if abs(row1 - row2) + abs(col1 - col2) == 1:
            self.board[empty], self.board[index] = self.board[index], self.board[empty]
            self.moves += 1

    def is_solved(self):
        return self.board == list(range(1, 16)) + [0]

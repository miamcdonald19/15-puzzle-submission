import random


class Puzzle:
    """
    Sliding puzzle logic for either a 3x3 or 4x4 board.

    Attributes:
        size (int): Board dimension (3 or 4).
        allow_diagonal (bool): If True, diagonal moves into the blank are allowed.
        board (list[int]): Flat list representing the board. 0 is the blank.
        moves (int): Number of successful moves made by the player.
    """

    def __init__(self, size=4, allow_diagonal=False):
        if size not in (3, 4):
            raise ValueError("size must be 3 or 4")

        self.size = size
        self.allow_diagonal = allow_diagonal
        self.moves = 0
        self.board = self._solved_board()

    def _solved_board(self):
        """Return the solved board for the current size."""
        return list(range(1, self.size * self.size)) + [0]

    def reset(self):
        """Reset the board to the solved state and clear the move counter."""
        self.board = self._solved_board()
        self.moves = 0

    def is_solved(self):
        """Return True if the board is in solved order."""
        return self.board == self._solved_board()

    def _neighbors(self, index):
        """
        Return a list of indices that are adjacent to the given index.
        Includes diagonal neighbors when diagonal mode is enabled.
        """
        row, col = divmod(index, self.size)
        neighbors = []

        # Orthogonal directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Optional diagonal directions
        if self.allow_diagonal:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                neighbors.append(nr * self.size + nc)

        return neighbors

    def valid_move_indices(self):
        """Return all tile indices that can currently move into the blank."""
        empty_index = self.board.index(0)
        return self._neighbors(empty_index)

    def move(self, index):
        """
        Move the tile at index into the blank if the move is legal.

        Returns:
            bool: True if the move happened, False otherwise.
        """
        if not (0 <= index < len(self.board)):
            return False

        empty_index = self.board.index(0)

        if index in self._neighbors(empty_index):
            self.board[empty_index], self.board[index] = (
                self.board[index],
                self.board[empty_index],
            )
            self.moves += 1
            return True

        return False

    def inversion_count(self, board=None):
        """
        Return the inversion count of the board, ignoring the blank (0).
        This is mainly useful for standard non-diagonal solvability checks.
        """
        if board is None:
            board = self.board

        nums = [x for x in board if x != 0]
        inversions = 0

        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    inversions += 1

        return inversions

    def is_solvable(self, board=None):
        """
        Check solvability under STANDARD sliding-puzzle rules
        (orthogonal moves only).

        For diagonal mode, this method is not the right mathematical test,
        but our scramble is still guaranteed solvable because it is generated
        from valid moves starting from the solved board.
        """
        if board is None:
            board = self.board

        if self.allow_diagonal:
            # In diagonal mode, we guarantee solvability by construction
            # via scramble(), which starts solved and performs valid moves.
            return True

        inversions = self.inversion_count(board)

        if self.size % 2 == 1:
            # Odd grid (3x3): solvable if inversions are even
            return inversions % 2 == 0

        # Even grid (4x4): use blank row from bottom
        blank_index = board.index(0)
        blank_row_from_top = blank_index // self.size
        blank_row_from_bottom = self.size - blank_row_from_top

        if blank_row_from_bottom % 2 == 0:
            return inversions % 2 == 1
        return inversions % 2 == 0

    def scramble(self, steps=None):
        """
        Scramble the puzzle by making random valid moves from the solved board.
        This guarantees the result is reachable (therefore solvable).

        Args:
            steps (int | None): Number of random legal moves to apply.
                                If None, a default based on board size is used.
        """
        self.reset()

        if steps is None:
            steps = self.size * self.size * 30

        previous_empty = None

        for _ in range(steps):
            empty_index = self.board.index(0)
            choices = self._neighbors(empty_index)

            # Avoid immediately undoing the last move when possible
            if previous_empty in choices and len(choices) > 1:
                choices.remove(previous_empty)

            chosen = random.choice(choices)

            # Swap chosen tile with blank directly (do not count scramble moves)
            self.board[empty_index], self.board[chosen] = (
                self.board[chosen],
                self.board[empty_index],
            )
            previous_empty = empty_index

        # Very rare, but if it accidentally returns to solved, scramble again
        if self.is_solved():
            return self.scramble(steps=steps)

        self.moves = 0
from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with the number of objects in each row.
    """

    def __init__(self, board):
        """Initialize the Game of Nim with the given board."""
        self.board = board
        moves = [(x, y) for x in range(len(board)) for y in range(1, board[x] + 1)]
        self.initial = GameState(
            board=board, moves=moves, utility=0, to_move="MAX"
        )

    def actions(self, state):
        """Return the list of legal moves for the current state."""
        if state is None:  # Handle the case where no state is passed
            state = self.initial  # Use the initial state if not provided

        # Ensure 'state' has a 'moves' attribute
        if hasattr(state, "moves") and state.moves:
            return state.moves
        else:
            # Generate legal moves based on the current board
            moves = [
                (x, y)
                for x in range(len(self.board))
                for y in range(1, self.board[x] + 1)
            ]
            return moves

    def result(self, state, move):
        """Return the new state reached from the given state and the given move."""
        if move not in state.moves:
            return state

        row = move[0]
        n = move[1]
        board = state.board.copy()
        board[row] -= n

        moves = [
            (x, y) for x in range(len(board)) for y in range(1, board[x] + 1)
        ]

        next_player = "MIN" if state.to_move == "MAX" else "MAX"
        return GameState(
            to_move=next_player,
            utility=self.utility(state, state.to_move),
            board=board,
            moves=moves,
        )

    def utility(self, state, player):
        """Return +1 if MAX wins, -1 if MIN wins."""
        if self.terminal_test(state):
            return 1 if state.to_move == "MIN" else -1
        return 0  # Game continues

    def terminal_test(self, state):
        """Return True if the given state represents the end of the game."""
        return all(i == 0 for i in state.board)

    def display(self, state):
        """Display the Game of Nim board."""
        print("board:", state.board)
        print("Current Turn:", state.to_move)


if __name__ == "__main__":
    # Create an instance of the Game of Nim with a predefined board
    nim = GameOfNim(board=[11, 9, 7, 5, 3, 1])  # Custom board

    # Display the initial board
    print("Initial board:", nim.initial.board)

    # Play the game using alpha-beta pruning for the computer and query-based input for the player
    utility = nim.play_game(alpha_beta_player, query_player)

    # Determine and display the winner
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")


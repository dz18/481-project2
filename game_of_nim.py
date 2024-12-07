
from games import *

class GameOfNim(Game):

    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board):
        """ Init. Game of Nim Elements """
        self.board = board
        moves = [(x, y) for x in range(len(board))
                for y in range(1, board[x] + 1)]
        self.initial = GameState(board=board, moves=moves, utility=0, to_move="MAX")
    
    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves
    
    def result(self, state, move):
        """ Returns the new state reached from the given state and the given move """
        if move not in state.moves:
            return state
        
        row = move[0]
        n = move[1]
        board = state.board.copy()
        board[row] -= n

        moves = [(x, y) for x in range(len(board))
                for y in range(1, board[x] + 1)]

        next_player = ('MIN' if state.to_move == 'MAX' else 'MAX')
        return GameState(
            to_move=next_player,
            utility=self.utility(state, state.to_move),
            board=board, 
            moves=moves
        )
    
    def utility(self, state, player):
        """ Return +1 if Max wins, -1 if Min wins"""

        if self.terminal_test(state):
            if state.to_move == 'MAX':
                return 1
            else:  
                return -1
            # return 1 if state.to_move == "MAX"  else -1
            
        return 0 # Game Continues
    
    def terminal_test(self, state):
        """ Returns true if given state represents end of a game """
        result = True
        for i in state.board:
            if i != 0:
                result = False
        
        return result
    

    def display(self, state):
        """ Display Game of Nim Board """
        board = state.board
        next = state.to_move
        print("board: ", board)
        print("Current Turn: ", next)


if __name__ == "__main__":

    nim = GameOfNim(board=[11,9,7,5,3,1]) # Creating the game instance

    # nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    # print(nim.initial.board) # must be [0, 5, 3, 1]
    # print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2,1), (2, 2), (2, 3), (3, 1)]

    #print(nim.result(nim.initial, (1,3) ).board)
    print("board: ", nim.initial.board)
    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first
    if (utility < 0):
        print("MIN won the game")
    else:
        print("MAX won the game")

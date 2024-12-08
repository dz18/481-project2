from games import *
import tkinter as tk
from tkinter import messagebox

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

class NimGUI:
    def __init__(self):
        self.state = None
        self.game = None

        # Tkinter Setup
        self.root = tk.Tk()
        self.root.title("Game of Nim")

        # Frames
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack(pady=20)

        self.board_frame = tk.Frame(self.root)
        self.controls_frame = tk.Frame(self.root)

        # Setup Elements
        self.piles_label = tk.Label(self.setup_frame, text="Number of Piles:", font=("Arial", 12))
        self.piles_label.grid(row=0, column=0, padx=5)

        self.piles_entry = tk.Entry(self.setup_frame, width=5)
        self.piles_entry.grid(row=0, column=1, padx=5)

        self.stones_label = tk.Label(self.setup_frame, text="Stones in Each Pile (comma-separated):", font=("Arial", 12))
        self.stones_label.grid(row=1, column=0, columnspan=2, padx=5)

        self.stones_entry = tk.Entry(self.setup_frame, width=30)
        self.stones_entry.grid(row=1, column=2, padx=5)

        self.start_button = tk.Button(self.setup_frame, text="Start Game", command=self.initialize_game)
        self.start_button.grid(row=2, column=1, pady=10)

    def initialize_game(self):
        """Set up the game with the custom board configuration."""
        try:
            # Get the number of piles and stones from the user
            piles = int(self.piles_entry.get())
            stones = list(map(int, self.stones_entry.get().split(',')))

            if len(stones) != piles:
                raise ValueError("Number of stones does not match the number of piles")

            # Initialize the game
            self.game = GameOfNim(stones)
            self.state = self.game.initial

            self.setup_frame.pack_forget()
            self.board_frame.pack(pady=20)
            self.controls_frame.pack(pady=10)

            self.create_game_elements()
            self.update_board()
            self.ai_move()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def create_game_elements(self):
        """Create elements for the game interface."""
        self.status_label = tk.Label(self.root, text="Your Turn", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.pile_label = tk.Label(self.controls_frame, text="Pile:", font=("Arial", 12))
        self.pile_label.grid(row=0, column=0, padx=5)

        self.pile_entry = tk.Entry(self.controls_frame, width=5)
        self.pile_entry.grid(row=0, column=1, padx=5)

        self.stones_label = tk.Label(self.controls_frame, text="Stones:", font=("Arial", 12))
        self.stones_label.grid(row=0, column=2, padx=5)

        self.stones_entry = tk.Entry(self.controls_frame, width=5)
        self.stones_entry.grid(row=0, column=3, padx=5)

        self.move_button = tk.Button(self.controls_frame, text="Make Move", command=self.player_move)
        self.move_button.grid(row=0, column=4, padx=10)

    def update_board(self, move=None):
        """Refresh the display of the game board."""
        for widget in self.board_frame.winfo_children():
            widget.destroy()  # Clear the board display

        for i, pile in enumerate(self.state.board):
            pile_label = tk.Label(self.board_frame, text=f"Pile {i+1}: {'O ' * pile}", font=("Arial", 12))
            pile_label.pack()

        if move:
            pile, stone = move 
            move_label = tk.Label(
                self.board_frame,
                text=f"{'AI' if self.state.to_move == 'MIN' else 'Player'} removed {stone} stone(s) from Pile {pile + 1}.",
                font=("Arial", 12),
                fg="blue",
            )
            move_label.pack()

    def player_move(self):
        """Handle the player's move."""
        try:
            pile = int(self.pile_entry.get()) - 1
            stones = int(self.stones_entry.get())
            if pile < 0 or pile >= len(self.state.board) or stones <= 0 or stones > self.state.board[pile]:
                raise ValueError("Invalid move")

            move = (pile, stones)
            if move not in self.game.actions(self.state):
                raise ValueError("Illegal move")

            self.state = self.game.result(self.state, move)
            self.update_board()
            self.check_game_end()

            # Check if game is over
            if not self.game.terminal_test(self.state):
                self.ai_move()

        except ValueError as e:
            messagebox.showerror("Invalid Move", str(e))

    def ai_move(self):
        """Handle the AI's move."""
        self.root.update_idletasks()

        move = alpha_beta_player(self.game, self.state)
        self.state = self.game.result(self.state, move)

        self.update_board(move)
        self.check_game_end()

    def check_game_end(self):
        """Check if the game has ended and display the winner."""
        if self.game.terminal_test(self.state):
            winner = "AI" if self.state.to_move == "MAX" else "You"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.root.quit()

        else:
            current_turn = "MAX" if self.state.to_move == "MAX" else "MIN"
            self.status_label.config(text=f"Your Turn")

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()

if __name__ == "__main__":
    gui = NimGUI()
    gui.run()

# if __name__ == "__main__":
#     # Create an instance of the Game of Nim with a predefined board
#     nim = GameOfNim(board=[7, 5, 3, 1])  # Custom board

#     # Display the initial board
#     print("Initial board:", nim.initial.board)

#     # Play the game using alpha-beta pruning for the computer and query-based input for the player
#     utility = nim.play_game(alpha_beta_player, query_player)

#     # Determine and display the winner
#     if utility < 0:
#         print("MIN won the game")
#     else:
#         print("MAX won the game")
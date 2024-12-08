import tkinter as tk
from game_of_nim import GameOfNim  # Import the fixed GameOfNim class

# Initialize the main application
root = tk.Tk()
root.title("Game of Nim")
root.geometry("400x400")

# Initialize the game with a starting board
game = GameOfNim([3, 4, 5])  # Example: 3 piles with 3, 4, and 5 stones

# Create a frame to display the game board
board_frame = tk.Frame(root)
board_frame.pack(pady=10)

def update_board():
    """
    Refresh the display of the game board.
    """
    for widget in board_frame.winfo_children():
        widget.destroy()  # Clear previous display
    for i, pile in enumerate(game.board):
        label = tk.Label(
            board_frame,
            text=f"Pile {i+1}: {'O ' * pile}",
            font=("Arial", 12)
        )
        label.pack()

# Create input fields for player's move
pile_entry = tk.Entry(root, width=5)
pile_entry.pack(pady=5)
pile_entry.insert(0, "Pile")

stones_entry = tk.Entry(root, width=5)
stones_entry.pack(pady=5)
stones_entry.insert(0, "Stones")

# Create a label to display the current status
status_label = tk.Label(root, text="Player's Turn", font=("Arial", 12))
status_label.pack(pady=10)

def make_move():
    """
    Handle the player's move and update the board.
    """
    try:
        pile = int(pile_entry.get()) - 1  # Convert to 0-based index
        stones = int(stones_entry.get())

        # Check if the move is valid
        if 0 <= pile < len(game.board) and 1 <= stones <= game.board[pile]:
            game.board[pile] -= stones  # Update the board
            update_board()

            # Check if the player has won
            if sum(game.board) == 0:
                status_label.config(text="You win!")
                return

            # AI's turn: Choose the first valid move
            ai_move = game.actions(None)[0]
            game.board[ai_move[0]] -= ai_move[1]
            update_board()

            # Check if the AI has won
            if sum(game.board) == 0:
                status_label.config(text="AI wins!")
            else:
                status_label.config(text="Player's Turn")
        else:
            status_label.config(text="Invalid move!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

# Button for submitting moves
move_button = tk.Button(root, text="Make Move", command=make_move)
move_button.pack(pady=10)

# Display the initial game board
update_board()

# Run the GUI application
root.mainloop()

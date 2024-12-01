import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class TicTacToeWithNumbersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe with Numbers")
        self.root.geometry("600x600")  # Resize the window

        # Initialize the 3x3 grid with random numbers between 1 and 20
        self.board = [[random.randint(1, 20) for _ in range(3)] for _ in range(3)]
        self.occupied = [['' for _ in range(3)] for _ in range(3)]  # Track which player occupies each block
        self.current_player = 'X'
        self.winner = None
        self.score = {'X': 0, 'O': 0}
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Buttons for the grid

        # Create the 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                btn = tk.Button(self.root, text=" ", font=("Arial", 40), width=5, height=2,
                                command=lambda r=row, c=col: self.guess_number(r, c))
                btn.grid(row=row, column=col, padx=10, pady=10)  # Add padding between buttons
                self.buttons[row][col] = btn

        # Label to show the current player
        self.player_label = tk.Label(self.root, text=f"Player {self.current_player}'s turn", font=("Arial", 20))
        self.player_label.grid(row=3, column=0, columnspan=3)

    def check_winner(self):
        # Check for a winner (3 in a row, column, or diagonal)
        for row in range(3):
            if self.occupied[row][0] == self.occupied[row][1] == self.occupied[row][2] and self.occupied[row][0] != '':
                return self.occupied[row][0]
        for col in range(3):
            if self.occupied[0][col] == self.occupied[1][col] == self.occupied[2][col] and self.occupied[0][col] != '':
                return self.occupied[0][col]
        if self.occupied[0][0] == self.occupied[1][1] == self.occupied[2][2] and self.occupied[0][0] != '':
            return self.occupied[0][0]
        if self.occupied[0][2] == self.occupied[1][1] == self.occupied[2][0] and self.occupied[0][2] != '':
            return self.occupied[0][2]
        return None

    def guess_number(self, row, col):
        # If the block is already occupied, do nothing
        if self.occupied[row][col]:
            messagebox.showwarning("Occupied", "This block is already occupied!")
            return
        
        # Open an input dialog for the player to guess the number
        guess = simpledialog.askinteger("Guess", f"Player {self.current_player}, guess the number for block ({row}, {col}) (1-20)", minvalue=1, maxvalue=20)

        if guess is None:  # If the player cancels the input
            return

        if guess == self.board[row][col]:
            # Correct guess, occupy the block
            self.occupied[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state="disabled")
            self.score[self.current_player] += 1
            self.player_label.config(text=f"Correct! {self.current_player} occupies block ({row}, {col})")

            # Check for winner
            winner = self.check_winner()
            if winner:
                self.winner = winner
                self.end_game()
                return

            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.player_label.config(text=f"Player {self.current_player}'s turn")
        else:
            # Incorrect guess, switch player
            self.player_label.config(text=f"Wrong guess! Now it's {self.current_player}'s turn.")
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.player_label.config(text=f"Player {self.current_player}'s turn")

    def end_game(self):
        # Show the winner and final score
        messagebox.showinfo("Game Over", f"Player {self.winner} wins!\n\nFinal Score:\nX: {self.score['X']} blocks\nO: {self.score['O']} blocks")
        self.root.quit()  # Exit the game

# Create the main window
root = tk.Tk()
game = TicTacToeWithNumbersGUI(root)
root.mainloop()

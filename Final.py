import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
import os
from heroes_data import heroes

class MBLLXOXO:
    def __init__(self, root):
        self.root = root
        self.root.title("MBLLXOXO")
        self.root.geometry("1000x750") 
        self.current_player = 'X'
        self.time_left = 15  
        image_path = "Map.jpg" 
        image = Image.open(image_path)
        image = image.resize((1200, 900))
        self.bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # self.hero_images = {}
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)
        self.initialize_game()
    
    def initialize_game(self):
        self.selected_heroes = random.sample(list(heroes.items()), 9)
        self.board = [self.selected_heroes[i:i+3] for i in range(0, 9, 3)]
        self.occupied = [['' for _ in range(3)] for _ in range(3)] 
        self.winner = None
        self.score = {'X': 0, 'O': 0}
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  
        self.frames = [[None for _ in range(3)] for _ in range(3)]   
        self.images = [[None for _ in range(3)] for _ in range(3)] 
        for row in range(3):
            for col in range(3):
                canvas = tk.Canvas(self.root, width=150, height=150,highlightthickness=0)
                canvas.grid(row=row, column=col, padx=10, pady=10)
                
                hero_id, hero_data = self.board[row][col]
                hero_role = random.choice(hero_data.get("role")) 
                hero_skin = hero_data.get("skin")
                hero_skill = hero_data.get("skill")
                btn_text = f"Role: {hero_role}\nSkin: {hero_skin}\nSkill: {hero_skill}"
                
                btn = tk.Button(canvas, text=btn_text, font=("Arial", 9), width=145, height=145, command=lambda r=row, c=col: self.guess_hero_name(r, c),bg="#cfd8e6")
                btn.place(relx=0.5, rely=0.5, anchor="center")   
                self.buttons[row][col] = btn
                self.frames[row][col] = canvas
            
        self.player_canvas = tk.Canvas(self.root, width=250, height=40, bg="#6d8c97", bd=0, highlightthickness=3, highlightbackground="#121a24")
        self.player_canvas.grid(row=3, column=0, columnspan=3, pady=10)
        self.player_x_circle = self.player_canvas.create_oval(5, 5, 38, 38, fill="#2567ab")  
        self.timer_text = self.player_canvas.create_text(125, 20, text=f"Time left: {self.time_left}s", font=("Arial", 15))
        self.player_o_circle = self.player_canvas.create_oval(215, 5, 248, 38, fill="gray") 
        self.countdown()
            
        def reset_game():
            self.current_player = 'X' 
            self.time_left = 15 
            self.winner = None  
            self.initialize_game()  
            self.reset_timer()  
        self.reset_game = reset_game
        
    def countdown(self):
        if self.time_left > 0:
            self.player_canvas.itemconfig(self.timer_text, text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.countdown)
        else:
            self.switch_player()
            self.countdown()

    def reset_timer(self):
        self.time_left = 30
        self.player_canvas.itemconfig(self.timer_text ,text=f"Time left: {self.time_left}s")
        
    def guess_hero_name(self, row, col):
        hero_id, hero_data = self.board[row][col]
        correct_name = hero_data['name'] 
        guess = simpledialog.askstring("Guess the Hero", f"Player {self.current_player}, guess the hero's name:")
        if guess and guess.strip(): 
            if guess.lower() == correct_name.lower():
                messagebox.showinfo("Correct!", f"You guessed it right! The hero is {correct_name}.")
                self.mark_block(row, col)
                self.switch_player()
            else:
                messagebox.showerror("Incorrect!", f"Wrong guess! It's not {guess}. Please try again.")
                self.switch_player()
        else:
            return
        
    def mark_block(self, row, col):
        self.occupied[row][col] = self.current_player
        color = "#2567ab" if self.current_player == 'X' else "#d33a39"
        
        self.frames[row][col].configure(bg="#577595")
        hero_id, hero_data = self.board[row][col]
        hero_images = os.listdir("heroimage")
        if hero_images:
            chosen_image = f"{hero_data.get("name")}.webp"
            image_path = os.path.join("heroimage", chosen_image)
            image = Image.open(image_path)
            image = image.resize((130, 130))
            tk_image = ImageTk.PhotoImage(image)
            
            self.buttons[row][col].config(image=tk_image,bg=color)
            self.buttons[row][col].image = tk_image 
        self.check_winner()

    def check_winner(self):
        """Check if there is a winner and update the GUI with color for the winner."""
        for i in range(3):
            if self.occupied[i][0] == self.occupied[i][1] == self.occupied[i][2] != '':
                self.winner = self.occupied[i][0]
            if self.occupied[0][i] == self.occupied[1][i] == self.occupied[2][i] != '':
                self.winner = self.occupied[0][i]
        
        if self.occupied[0][0] == self.occupied[1][1] == self.occupied[2][2] != '':
            self.winner = self.occupied[0][0]
        if self.occupied[0][2] == self.occupied[1][1] == self.occupied[2][0] != '':
            self.winner = self.occupied[0][2]
        
        if self.winner:
            winner_color = "blue" if self.winner == 'X' else "red"
            self.display_victory(winner_color)
        else:
            player1_count = sum(self.occupied[row][col] == 'X' for row in range(3) for col in range(3))
            player2_count = sum(self.occupied[row][col] == 'O' for row in range(3) for col in range(3))

        total_blocks_occupied = player1_count + player2_count
        if total_blocks_occupied == 9:
            self.display_victory(winner_color)         
                    
    def display_victory(self, winner_color):
        """Display the victory screen with an image and the winner's text."""
        victory_window = tk.Toplevel(self.root)
        victory_window.geometry("500x300")
        victory_window.title("Victory!")
        victory_window.transient(self.root)  
        victory_window.grab_set()  
        winner_color = "blue" if self.winner == 'X' else "red"
        canvas = tk.Canvas(victory_window, width=500, height=300, bg=winner_color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        victory_image = Image.open("victory.png")
        victory_image = victory_image.resize((500, 300)) 
        tk_victory_image = ImageTk.PhotoImage(victory_image)
        canvas.create_image(250,150, image=tk_victory_image, anchor="center")
        canvas.image = tk_victory_image 
        
        play_again_button = tk.Button(canvas, text="Play Again", font=("Arial", 12), bg="#cfd8e6", command=lambda: (self.reset_game(),victory_window.destroy()))
        play_again_button.place(relx=0.3, rely=0.8, anchor='center')

        quit_button = tk.Button(canvas, text="Quit", font=("Arial", 12), bg="#cfd8e6", command=lambda: self.root.quit())
        quit_button.place(relx=0.7, rely=0.8, anchor='center')
        
        victory_window.update_idletasks()
        width = victory_window.winfo_width()
        height = victory_window.winfo_height()
        x = (victory_window.winfo_screenwidth() // 2) - (width // 2)
        y = (victory_window.winfo_screenheight() // 2) - (height // 2)
        victory_window.geometry(f"{width}x{height}+{x}+{y}")

    def switch_player(self):
        """Switch the current player and update the GUI label with color."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.update_player_label()
        self.reset_timer() 

    def update_player_label(self):
        """Update the color of the player circles depending on the current player."""
        if self.current_player == 'X':
            self.player_canvas.itemconfig(self.player_x_circle, fill="#2567ab")
            self.player_canvas.itemconfig(self.player_o_circle, fill="gray")
        else:
            self.player_canvas.itemconfig(self.player_o_circle, fill="#d33a39")
            self.player_canvas.itemconfig(self.player_x_circle, fill="gray")
            
if __name__ == "__main__":
    root = tk.Tk()
    game = MBLLXOXO(root)
    root.mainloop()
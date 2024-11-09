from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#FF6B6B'  
symbol_O_color = '#4ECDC4'  
line_color = '#FFEB3B'  
background_color = '#1A1A1D'  
button_background_color = '#4A90E2'  
button_text_color = '#ff0000'
button_font = ("Arial", 12, "bold")

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.configure(bg=background_color)
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, bg=background_color)
        self.canvas.pack()

        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        # Setting up the Play Again button
        self.play_again_button = Button(
            self.window, text="Play Again", command=self.play_again, state=DISABLED, 
            bg=button_background_color, fg=button_text_color, font=button_font,
            activebackground=button_background_color, activeforeground=button_text_color,
            highlightbackground=button_background_color
        )
        self.play_again_button.pack(side=LEFT, padx=10, pady=10)

        # Setting up the Quit button
        self.quit_button = Button(
            self.window, text="Quit", command=self.window.quit, 
            bg=button_background_color, fg=button_text_color, font=button_font,
            activebackground=button_background_color, activeforeground=button_text_color,
            highlightbackground=button_background_color
        )
        self.quit_button.pack(side=RIGHT, padx=10, pady=10)

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        self.reset_board = False
        self.play_again_button.config(state=DISABLED)

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'It\'s a Tie!'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores\n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill="green",
                                text=score_text)

        score_text = f'Player 1 (X): {self.X_score}\nPlayer 2 (O): {self.O_score}\nTie: {self.tie_score}'
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill="green",
                                text=score_text)

        self.reset_board = True
        self.play_again_button.config(state=NORMAL)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        player_val = -1 if player == 'X' else 1
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player_val:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player_val:
                return True
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player_val:
            return True
        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player_val:
            return True
        return False

    def is_tie(self):
        return not np.any(self.board_status == 0)

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        self.O_wins = not self.X_wins and self.is_winner('O')
        self.tie = not self.X_wins and not self.O_wins and self.is_tie()

        if self.X_wins:
            print('X wins')
        elif self.O_wins:
            print('O wins')
        elif self.tie:
            print('It\'s a Tie!')

        return self.X_wins or self.O_wins or self.tie

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns and not self.is_grid_occupied(logical_position):
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                self.player_X_turns = not self.player_X_turns
            elif not self.is_grid_occupied(logical_position):
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
                self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()
        else:
            self.play_again()

game_instance = TicTacToe()
game_instance.mainloop()

# program: reakcnidoba.py - hra na měření reakční doby
# autor: Jakub Skalka 8.E <skalkaj@jirovcovka.net>
#        Kryštof Maxera 8.E
#        Barbora Bočkayová 8.E

##### MODULY
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

##### Deklarace tříd
class KeyboardKing(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard King")
        self.geometry("800x600")



        self.create_menu()
        self.create_canvas()
        #self.show_rules()

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Start", command=self.start_game) #napsat start_game
        game_menu.add_command(label="End", command=self.quit)

        #zobrazení pravidel?

    def create_canvas(self):
        self.canvas = rk.canvas(self, width=800, height=500, bg="white")

    #def start_game(self):
        

if __name__ == "__main__":
    app = KeyboardKing()
    app.mainloop()
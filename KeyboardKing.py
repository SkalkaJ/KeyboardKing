# program: reakcnidoba.py - hra na měření reakční doby
# autor: Jakub Skalka 7.E <skalkaj@jirovcovka.net>

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

if __name__ == "__main__":
    app = KeyboardKing()
    app.mainloop()
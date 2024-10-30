import tkinter as tk
from tkinter import messagebox
import random

class KeyboardKing(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard King")
        self.geometry("800x600")

        # Inicializace proměnných
        self.score = 0
        self.rounds_left = 10
        self.speed = 1000  # počáteční rychlost pádu kruhu v ms
        self.current_rect = None
        self.rect_pressed = False
        self.game_running = False

        # Vytvoření GUI
        self.create_menu()
        self.create_canvas()
        self.create_labels()

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        # Menu Hra
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Hra", menu=game_menu)
        game_menu.add_command(label="Start", command=self.start_game)
        game_menu.add_command(label="Konec", command=self.quit)

        # Menu Help
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Nápověda", command=self.show_help)
        help_menu.add_command(label="O hře", command=self.show_about)

    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=800, height=500, bg="white")
        self.canvas.pack()

        # Vytvoření obdélníků a přiřazení kláves
        self.rects = []
        keys = ['S', 'D', 'F', 'J', 'K', 'L']
        x_start = 50
        for i in range(6):
            rect = self.canvas.create_rectangle(x_start, 450, x_start + 100, 500, fill="grey", tags=keys[i])
            self.rects.append(rect)
            x_start += 120

        self.bind("<KeyPress>", self.key_pressed)

    def create_labels(self):
        self.score_label = tk.Label(self, text=f"Skóre: {self.score}")
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.rounds_label = tk.Label(self, text=f"Kola: {self.rounds_left}")
        self.rounds_label.pack(side=tk.RIGHT, padx=20)

    def show_help(self):
        help_text = (
            "Nápověda:\n\n"
            "1. Stiskněte 'Start' pro spuštění hry.\n"
            "2. Po rozsvícení obdélníku stiskněte odpovídající klávesu (S, D, F, J, K, L).\n"
            "3. Získejte bod, pokud stisknete správnou klávesu před začátkem dalšího kola.\n"
            "4. Hra má 10 kol a rychlost se postupně zvyšuje.\n"
            "5. Po skončení hry se zobrazí vaše celkové skóre."
        )
        messagebox.showinfo("Nápověda", help_text)

    def show_about(self):
        about_text = (
            "O hře:\n\n"
            "Verze: 1.0\n"
            "Autor: Vaše Jméno\n"
            "Email: váš_email@example.com"
        )
        messagebox.showinfo("O hře", about_text)

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.score = 0
            self.rounds_left = 10
            self.speed = 1000
            self.update_labels()
            self.next_round()

    def next_round(self):
        if self.rounds_left > 0:
            self.rounds_left -= 1
            self.rect_pressed = False
            self.update_labels()
            self.highlight_rectangle()
            self.drop_circle()
        else:
            self.end_game()

    def highlight_rectangle(self):
        # Reset barev obdélníků
        for rect in self.rects:
            self.canvas.itemconfig(rect, fill="grey")
        # Náhodně vybereme obdélník k rozsvícení
        self.current_rect = random.choice(self.rects)
        self.canvas.itemconfig(self.current_rect, fill="yellow")

    def drop_circle(self):
        # Vytvoření kruhu na vrcholu canvasu
        self.circle = self.canvas.create_oval(375, 0, 425, 50, fill="blue")
        self.move_circle()

    def move_circle(self):
        if self.game_running:
            self.canvas.move(self.circle, 0, 5)
            pos = self.canvas.coords(self.circle)
            if pos[3] < 450:
                self.after(20, self.move_circle)
            else:
                self.canvas.delete(self.circle)
                # Konec kola, nastavení obdélníku zpět na šedou
                if not self.rect_pressed:
                    self.canvas.itemconfig(self.current_rect, fill="red")
                else:
                    self.canvas.itemconfig(self.current_rect, fill="grey")
                self.speed = max(200, self.speed - 80)
                self.next_round()

    def key_pressed(self, event):
        if self.game_running and not self.rect_pressed:
            key = event.keysym.upper()
            rect_tag = self.canvas.gettags(self.current_rect)[0]
            if key == rect_tag:
                self.score += 1
                self.canvas.itemconfig(self.current_rect, fill="green")
                self.canvas.itemconfig(self.circle, fill="black")
            else:
                self.canvas.itemconfig(self.current_rect, fill="black")
            self.rect_pressed = True
            self.update_labels()

    def update_labels(self):
        self.score_label.config(text=f"Skóre: {self.score}")
        self.rounds_label.config(text=f"Kola: {self.rounds_left}")

    def end_game(self):
        self.game_running = False
        messagebox.showinfo("Konec hry", f"Hra skončila!\nVaše skóre: {self.score}")

if __name__ == "__main__":
    game = KeyboardKing()
    game.mainloop()
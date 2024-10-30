### Hra Keyboard King, která testuje rychlost a přesnost stisku kláves. Po spuštění hry se na obrazovce zobrazí 6 obdélníků,
# každý s jednou klávesou (S, D, F, J, K, L). Obdélníky se náhodně rozsvítí a hráč musí stisknout odpovídající klávesu, než kruh dosáhne
# spodní části obrazovky. Po každém kole se rychlost zvyšuje a hráč musí stisknout správnou klávesu rychleji.
# Hra má 5 kol a po skončení se zobrazí celkové skóre.
# autor: Kryštof Maxera, 8.E, <maxerak@jirovcovka.net>/ Jakub Skalka, 8.E, <skalkaj@jirovcovka.net>/ Barbora Bočkayová, 8.E, <bockayovab@jirovcovka.net> 

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

        # Nastavení ikony aplikace
        icon = tk.PhotoImage(file='icon.png')
        self.iconphoto(False, icon)

        # Inicializace proměnných
        self.score = 0
        self.total_rounds = 5  # Celkový počet kol nastaven na 5
        self.rounds_left = self.total_rounds
        self.speed = 1000  # počáteční rychlost pádu kruhu v ms
        self.current_rect = None
        self.game_running = False
        self.circle_reached_bottom = False
        self.can_press = True  # Flag pro kontrolu stisků kláves

        # Vytvoření GUI
        self.create_menu()
        self.create_canvas()
        self.create_labels()

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        # Menu Hra a nastavení klikátek v menu
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Hra", menu=game_menu)
        game_menu.add_command(label="Start", command=self.start_game)
        game_menu.add_command(label="Konec", command=self.quit)

        # Menu Help a naastavení klikátek v menu
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Nápověda", command=self.show_help)
        help_menu.add_command(label="O hře", command=self.show_about)

    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=800, height=500, bg="white")
        self.canvas.pack()

        # Vytvoření obdélníků a přiřazení kláves
        self.rects = []
        self.keys = ['S', 'D', 'F', 'J', 'K', 'L'] # Klávesy pro obdélníky
        x_start = 50
        for i in range(6):
            rect = self.canvas.create_rectangle(
                x_start, 450, x_start + 100, 500,
                fill="grey", tags=self.keys[i]
            )
            self.rects.append(rect)
            x_start += 120

        self.bind("<KeyPress>", self.key_pressed)

    def create_labels(self):
        self.score_label = tk.Label(self, text=f"Skóre: {self.score}")
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.rounds_label = tk.Label(self, text=f"Kola: {self.rounds_left}")
        self.rounds_label.pack(side=tk.RIGHT, padx=20)

    def show_help(self): # Text nápovědy
        help_text = (
            "Nápověda:\n\n"
            "1. Stiskněte 'Start' pro spuštění hry.\n"
            "2. Po rozsvícení obdélníku stiskněte odpovídající klávesu (S, D, F, J, K, L).\n"
            "3. Pokud stisknete špatnou klávesu, v kole již nemůžete pokračovat.\n"
            "4. Hra má 5 kol a rychlost se postupně zvyšuje.\n"
            "5. Po skončení hry se zobrazí vaše celkové skóre."
        )
        messagebox.showinfo("Nápověda", help_text)

    def show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title("O hře")
        about_window.geometry("300x400")

        # Načtení obrázku a úprava velikosti
        image = tk.PhotoImage(file='foto.png')
        image = image.subsample(17, 17)  # Zmenšení obrázku na polovinu

        # Přidání obrázku do okna
        img_label = tk.Label(about_window, image=image)
        img_label.image = image  # Udržení reference na obrázek
        img_label.pack(pady=10)

        # Text s informacemi o hře
        about_text = (
            "Verze: 1.9.42\n"
            "Autor: Jakub Skalka, Kryštof Maxera, Barbora Bočkayová\n"
            "Email: skalkaj@jirovcovka.net\nmaxerak@jirovcovka.net\nbockayovab@jirovcovka.net"
        )
        text_label = tk.Label(about_window, text=about_text, justify="center")
        text_label.pack(pady=10)

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.score = 0
            self.rounds_left = self.total_rounds  # Reset počtu kol na začátku hry
            self.speed = 1000
            self.update_labels()
            self.next_round()

    def next_round(self):
        if self.rounds_left > 0:
            self.update_labels()
            self.circle_reached_bottom = False
            self.canvas.delete("circle")
            self.highlight_rectangle()
            self.drop_circle()
            self.can_press = True  # Umožní stisk kláves v novém kole
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
        self.circle = self.canvas.create_oval(375, 0, 425, 50, fill="blue", tags="circle")
        self.move_circle()

    def move_circle(self):
        if self.game_running:
            self.canvas.move("circle", 0, 5)
            pos = self.canvas.coords("circle")
            if pos[3] < 450:
                self.after(20, self.move_circle)
            else:
                # Kruh dosáhl spodní části - konec kola
                self.circle_reached_bottom = True
                self.canvas.delete("circle")
                # Reset barvy obdélníku
                self.canvas.itemconfig(self.current_rect, fill="grey")
                self.speed = max(200, self.speed - 80)
                self.rounds_left -= 1  # Snížení počtu kol zde
                self.next_round()
        else:
            self.canvas.delete("circle")

    def key_pressed(self, event):
        if self.game_running and not self.circle_reached_bottom and self.can_press:
            key = event.keysym.upper()
            rect_tag = self.canvas.gettags(self.current_rect)[0]
            if key == rect_tag:
                self.score += 1
                self.canvas.itemconfig(self.current_rect, fill="green")
                self.update_labels()
                # Po správném stisknutí zvýrazníme nový obdélník
                self.highlight_rectangle()
            else:
                self.canvas.itemconfig(self.current_rect, fill="black")
                self.can_press = False  # Zamezí dalším stiskům v tomto kole

    def update_labels(self):
        self.score_label.config(text=f"Skóre: {self.score}")
        self.rounds_label.config(text=f"Kola: {self.rounds_left}")

    def end_game(self):
        self.game_running = False
        messagebox.showinfo("Konec hry", f"Hra skončila!\nVaše skóre: {self.score}")
        # Reset barev obdélníků a smazání kruhu
        for rect in self.rects:
            self.canvas.itemconfig(rect, fill="grey")
        self.canvas.delete("circle")

# Spuštění hry při spuštění skriptu
if __name__ == "__main__":
    game = KeyboardKing()
    game.mainloop()
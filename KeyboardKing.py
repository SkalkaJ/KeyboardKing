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
        
        self.kola = 10
        self.skore = 0
        self.rychlost = 1000
        self.aktualni_obdelnik = None
        self.hra_bezi = False
        
        self.vytvor_menu()
        self.vytvor_canvas()
        self.zobraz_pravidla()
        
    def vytvor_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
        
        hra_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Hra", menu=hra_menu)
        hra_menu.add_command(label="Start", command=self.start_hra)
        hra_menu.add_command(label="Konec", command=self.quit)
        
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Nápověda", command=self.zobraz_napovedu)
        help_menu.add_command(label="O hře", command=self.zobraz_o_hre)
        
    def vytvor_canvas(self):
        self.canvas = tk.Canvas(self, width=800, height=500, bg="white")
        self.canvas.pack(pady=20)
        
        self.obdelniky = []
        barvy = ["red", "green", "blue", "yellow", "purple", "orange"]
        klavesy = ["S", "D", "F", "J", "K", "L"]
        
        for i in range(6):
            obdelnik = self.canvas.create_rectangle(100 + i*100, 400, 200 + i*100, 500, fill=barvy[i])
            self.obdelniky.append((obdelnik, klavesy[i]))
        
        self.skore_label = tk.Label(self, text=f"Skóre: {self.skore}")
        self.skore_label.pack()
        
        self.kola_label = tk.Label(self, text=f"Zbývající kola: {self.kola}")
        self.kola_label.pack()
        
        self.bind("<KeyPress>", self.stisk_klavesy)
        
    def zobraz_pravidla(self):
        pravidla = (
            "Vítejte ve hře Keyboard King!\n\n"
            "Pravidla:\n"
            "1. Stiskněte START pro začátek hry.\n"
            "2. Počkejte, až se rozsvítí obdélník a stiskněte odpovídající klávesu (S, D, F, J, K, L).\n"
            "3. Získejte bod za každý správný stisk klávesy.\n"
            "4. Hra se hraje na 10 kol.\n"
            "5. Po každém kole se zvyšuje rychlost padajícího kruhu.\n"
            "6. Na konci hry budete informováni o výsledku.\n"
        )
        messagebox.showinfo("Pravidla", pravidla)
        
    def zobraz_napovedu(self):
        napoveda = (
            "Nápověda:\n"
            "1. Stiskněte START pro začátek hry.\n"
            "2. Počkejte, až se rozsvítí obdélník a stiskněte odpovídající klávesu (S, D, F, J, K, L).\n"
            "3. Získejte bod za každý správný stisk klávesy.\n"
            "4. Hra se hraje na 10 kol.\n"
            "5. Po každém kole se zvyšuje rychlost padajícího kruhu.\n"
            "6. Na konci hry budete informováni o výsledku.\n"
        )
        messagebox.showinfo("Nápověda", napoveda)
        
    def zobraz_o_hre(self):
        o_hre = (
            "O hře:\n"
            "Verze: 1.0\n"
            "Autor: Jakub Skalka\n"
            "Email: skalkaj@jirovcovka.net\n"
        )
        messagebox.showinfo("O hře", o_hre)
        
    def start_hra(self):
        self.hra_bezi = True
        self.skore = 0
        self.kola = 10
        self.rychlost = 1000
        self.skore_label.config(text=f"Skóre: {self.skore}")
        self.kola_label.config(text=f"Zbývající kola: {self.kola}")
        self.dalsi_kolo()
        
    def dalsi_kolo(self):
        if self.kola > 0:
            self.kola -= 1
            self.kola_label.config(text=f"Zbývající kola: {self.kola}")
            self.aktualni_obdelnik = random.choice(self.obdelniky)
            self.canvas.itemconfig(self.aktualni_obdelnik[0], fill="black")
            self.after(self.rychlost, self.padajici_kruh)
        else:
            self.konec_hry()
        
    def padajici_kruh(self):
        self.canvas.delete("kruh")
        self.kruh = self.canvas.create_oval(350, 0, 450, 100, fill="red", tags="kruh")
        self.pohyb_kruhu()
        
    def pohyb_kruhu(self):
        if self.hra_bezi:
            self.canvas.move("kruh", 0, 10)
            pozice = self.canvas.coords("kruh")
            if pozice[3] < 400:
                self.after(50, self.pohyb_kruhu)
            else:
                self.canvas.delete("kruh")
                self.canvas.itemconfig(self.aktualni_obdelnik[0], fill=self.aktualni_obdelnik[1].lower())
                self.rychlost = max(100, self.rychlost - 100)
                self.dalsi_kolo()
        
    def stisk_klavesy(self, event):
        if self.hra_bezi and self.aktualni_obdelnik:
            if event.keysym.upper() == self.aktualni_obdelnik[1]:
                self.skore += 1
                self.skore_label.config(text=f"Skóre: {self.skore}")
                self.canvas.itemconfig("kruh", fill="black")
            else:
                self.canvas.itemconfig(self.aktualni_obdelnik[0], fill="red")
            self.aktualni_obdelnik = None
        
    def konec_hry(self):
        self.hra_bezi = False
        messagebox.showinfo("Konec hry", f"Konec hry! Vaše skóre je: {self.skore}")

if __name__ == "__main__":
    app = KeyboardKing()
    app.mainloop()
import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import os

PHRASES = [
    "asdf jklö",
    "Die schnelle braune Füchsin",
    "Python macht Spaß",
    "Tippen ist Übung"
]

STATS_FILE = "stats.json"

class TypingTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AlphaTast Clone")
        self.geometry("500x300")
        self.resizable(False, False)
        self._build_start()

    def _build_start(self):
        for w in self.winfo_children():
            w.destroy()
        tk.Label(self, text="AlphaTast Clone", font=("Arial", 20)).pack(pady=30)
        tk.Button(self, text="Training starten", command=self._start_training, width=20).pack(pady=10)
        tk.Button(self, text="Statistik", command=self._show_stats, width=20).pack(pady=10)

    # Training logic
    def _start_training(self):
        for w in self.winfo_children():
            w.destroy()
        self.phrase = random.choice(PHRASES)
        tk.Label(self, text=self.phrase, font=("Arial", 16)).pack(pady=20)
        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=10)
        self.entry.focus_set()
        self.start_time = time.time()
        tk.Button(self, text="Fertig", command=self._finish_training).pack(pady=10)

    def _finish_training(self):
        typed = self.entry.get()
        elapsed = max(time.time() - self.start_time, 1)
        accuracy = sum(1 for a, b in zip(typed, self.phrase) if a == b) / len(self.phrase) * 100
        wpm = len(typed) / 5 / (elapsed / 60)
        self._save_stats(wpm, accuracy)
        messagebox.showinfo("Ergebnis", f"WPM: {wpm:.2f}\nGenauigkeit: {accuracy:.2f}%")
        self._build_start()

    # Stats logic
    def _save_stats(self, wpm, accuracy):
        data = []
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        data.append({"wpm": wpm, "accuracy": accuracy})
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _show_stats(self):
        for w in self.winfo_children():
            w.destroy()
        tk.Label(self, text="Statistik", font=("Arial", 20)).pack(pady=20)
        data = []
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        if not data:
            tk.Label(self, text="Keine Daten").pack(pady=10)
        else:
            avg_wpm = sum(d["wpm"] for d in data) / len(data)
            avg_acc = sum(d["accuracy"] for d in data) / len(data)
            tk.Label(self, text=f"Durchschnitt WPM: {avg_wpm:.2f}").pack(pady=5)
            tk.Label(self, text=f"Durchschnitt Genauigkeit: {avg_acc:.2f}%").pack(pady=5)
        tk.Button(self, text="Zurück", command=self._build_start).pack(pady=20)

if __name__ == "__main__":
    app = TypingTrainer()
    app.mainloop()

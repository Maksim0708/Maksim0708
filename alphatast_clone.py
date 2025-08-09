import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import json
import os

USERS_DIR = "users"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
BADGE_THRESHOLDS = {100: "Starter", 500: "Fortgeschritten", 1000: "Meister"}

LANGUAGES = {
    "Deutsch": {
        "words": [
            "der", "die", "das", "Fuchs", "springt", "über", "den", "Hund",
            "schnell", "braun", "faul", "Lehrer", "Schüler", "Tastatur"
        ],
        "phrases": [
            "Die schnelle braune Füchsin springt über den faulen Hund",
            "Python macht Spaß",
            "Tippen ist Übung"
        ]
    },
    "English": {
        "words": [
            "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
            "teacher", "student", "keyboard", "practice", "speed", "accuracy"
        ],
        "phrases": [
            "The quick brown fox jumps over the lazy dog",
            "Typing is fun",
            "Practice makes perfect"
        ]
    }
}

THEMES = {
    "light": {"bg": "white", "fg": "black"},
    "dark": {"bg": "#2e2e2e", "fg": "white"}
}


class StatsManager:
    """Manage persistent statistics and settings per user."""

    def __init__(self, username: str):
        self.username = username
        os.makedirs(USERS_DIR, exist_ok=True)
        self.file = os.path.join(USERS_DIR, f"{username}.json")
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "role": "student",
                "language": "Deutsch",
                "theme": "light",
                "points": 0,
                "badges": [],
                "stats": []
            }
            self._save()

    def _save(self) -> None:
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_stat(self, wpm: float, accuracy: float) -> None:
        self.data["stats"].append({"wpm": wpm, "accuracy": accuracy, "time": time.time()})
        points = int(wpm * (accuracy / 100))
        self.data["points"] += points
        self._update_badges()
        self._save()

    def _update_badges(self) -> None:
        for threshold, badge in BADGE_THRESHOLDS.items():
            if self.data["points"] >= threshold and badge not in self.data["badges"]:
                self.data["badges"].append(badge)

    def level(self) -> int:
        return self.data["points"] // 100


class TypingTrainer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AlphaTast Clone")
        self.geometry("600x400")
        self.resizable(False, False)
        self.user: str | None = None
        self.stats_manager: StatsManager | None = None
        self.colors = THEMES["light"]
        self._user_selection()

    # ----- helpers -----------------------------------------------------
    def _clear(self) -> None:
        for w in self.winfo_children():
            w.destroy()
        self.configure(bg=self.colors["bg"])

    def _apply_theme(self) -> None:
        self.colors = THEMES[self.stats_manager.data.get("theme", "light")]  # type: ignore[arg-type]
        self.configure(bg=self.colors["bg"])

    # ----- user management ---------------------------------------------
    def _user_selection(self) -> None:
        self.stats_manager = None
        self.user = None
        self._clear()
        tk.Label(self, text="Benutzer wählen", font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        self.user_list = tk.Listbox(self)
        self.user_list.pack(pady=10)
        if os.path.exists(USERS_DIR):
            for f in os.listdir(USERS_DIR):
                if f.endswith(".json"):
                    self.user_list.insert(tk.END, f[:-5])
        tk.Button(self, text="Login", command=self._login).pack(pady=5)
        tk.Button(self, text="Neuer Benutzer", command=self._new_user).pack(pady=5)

    def _login(self) -> None:
        sel = self.user_list.curselection()
        if not sel:
            messagebox.showwarning("Benutzer", "Bitte Benutzer wählen")
            return
        name = self.user_list.get(sel[0])
        self.stats_manager = StatsManager(name)
        self.user = name
        self._apply_theme()
        self._build_start()

    def _new_user(self) -> None:
        name = simpledialog.askstring("Neuer Benutzer", "Name:")
        if not name:
            return
        role = messagebox.askyesno("Lehrer", "Ist dies ein Lehrer-Konto?")
        sm = StatsManager(name)
        if role:
            sm.data["role"] = "teacher"
            sm._save()
        self.stats_manager = sm
        self.user = name
        self._apply_theme()
        self._build_start()

    # ----- main menu ---------------------------------------------------
    def _build_start(self) -> None:
        assert self.stats_manager is not None
        self._clear()
        data = self.stats_manager.data
        tk.Label(
            self,
            text=f"Willkommen {self.stats_manager.username}",
            font=("Arial", 18),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
        ).pack(pady=10)
        tk.Label(
            self,
            text=f"Level {self.stats_manager.level()} - Punkte {data['points']}",
            bg=self.colors["bg"],
            fg=self.colors["fg"],
        ).pack(pady=5)
        tk.Button(self, text="Training starten", command=self._start_training, width=20).pack(pady=5)
        tk.Button(self, text="Statistik", command=self._show_stats, width=20).pack(pady=5)
        tk.Button(self, text="Einstellungen", command=self._settings, width=20).pack(pady=5)
        if data.get("role") == "teacher":
            tk.Button(self, text="Reporting", command=self._reporting, width=20).pack(pady=5)
        tk.Button(self, text="Abmelden", command=self._user_selection, width=20).pack(pady=5)

    # ----- training ----------------------------------------------------
    def _start_training(self) -> None:
        self._clear()
        tk.Label(self, text="Modus wählen", font=("Arial", 16), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        modes = ["Buchstaben-Mix", "Wortreihen", "Satzaufbau", "Eigener Text"]
        self.mode_var = tk.StringVar(value=modes[0])
        ttk.OptionMenu(self, self.mode_var, modes[0], *modes).pack(pady=5)
        tk.Button(self, text="Los", command=self._begin_training).pack(pady=10)
        tk.Button(self, text="Zurück", command=self._build_start).pack(pady=5)

    def _begin_training(self) -> None:
        mode = self.mode_var.get()
        lang = self.stats_manager.data["language"]  # type: ignore[index]
        if mode == "Eigener Text":
            phrase = simpledialog.askstring("Eigener Text", "Text eingeben:")
            if not phrase:
                self._build_start()
                return
            self.phrase = phrase
        elif mode == "Buchstaben-Mix":
            self.phrase = "".join(random.choice(LETTERS) for _ in range(20))
        elif mode == "Wortreihen":
            words = random.sample(LANGUAGES[lang]["words"], 5)
            self.phrase = " ".join(words)
        else:  # Satzaufbau
            self.phrase = random.choice(LANGUAGES[lang]["phrases"])
        self._training_screen()

    def _training_screen(self) -> None:
        self._clear()
        tk.Label(self, text=self.phrase, font=("Arial", 16), wraplength=550, bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=20)
        self.entry = tk.Entry(self, width=60)
        self.entry.pack(pady=10)
        self.entry.focus_set()
        self.start_time = time.time()
        tk.Button(self, text="Fertig", command=self._finish_training).pack(pady=10)

    def _finish_training(self) -> None:
        assert self.stats_manager is not None
        typed = self.entry.get()
        elapsed = max(time.time() - self.start_time, 1)
        accuracy = (
            sum(1 for a, b in zip(typed, self.phrase) if a == b) / max(len(self.phrase), 1) * 100
        )
        wpm = len(typed) / 5 / (elapsed / 60)
        self.stats_manager.add_stat(wpm, accuracy)
        messagebox.showinfo(
            "Ergebnis",
            f"WPM: {wpm:.2f}\nGenauigkeit: {accuracy:.2f}%\nPunkte: {self.stats_manager.data['points']}\nLevel: {self.stats_manager.level()}",
        )
        self._build_start()

    # ----- statistics --------------------------------------------------
    def _show_stats(self) -> None:
        assert self.stats_manager is not None
        self._clear()
        tk.Label(self, text="Statistik", font=("Arial", 20), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        stats = self.stats_manager.data["stats"]
        if not stats:
            tk.Label(self, text="Keine Daten", bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        else:
            avg_wpm = sum(d["wpm"] for d in stats) / len(stats)
            avg_acc = sum(d["accuracy"] for d in stats) / len(stats)
            tk.Label(self, text=f"Durchschnitt WPM: {avg_wpm:.2f}", bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=5)
            tk.Label(self, text=f"Durchschnitt Genauigkeit: {avg_acc:.2f}%", bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=5)
            tk.Label(
                self,
                text=f"Punkte: {self.stats_manager.data['points']} (Level {self.stats_manager.level()})",
                bg=self.colors["bg"],
                fg=self.colors["fg"],
            ).pack(pady=5)
            if self.stats_manager.data["badges"]:
                tk.Label(
                    self,
                    text="Abzeichen: " + ", ".join(self.stats_manager.data["badges"]),
                    bg=self.colors["bg"],
                    fg=self.colors["fg"],
                ).pack(pady=5)
        tk.Button(self, text="Zurück", command=self._build_start).pack(pady=20)

    # ----- settings ----------------------------------------------------
    def _settings(self) -> None:
        assert self.stats_manager is not None
        self._clear()
        tk.Label(self, text="Einstellungen", font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        tk.Label(self, text="Sprache:", bg=self.colors["bg"], fg=self.colors["fg"]).pack()
        langs = list(LANGUAGES.keys())
        self.lang_var = tk.StringVar(value=self.stats_manager.data["language"])
        ttk.OptionMenu(self, self.lang_var, self.lang_var.get(), *langs).pack(pady=5)
        tk.Label(self, text="Theme:", bg=self.colors["bg"], fg=self.colors["fg"]).pack()
        themes = list(THEMES.keys())
        self.theme_var = tk.StringVar(value=self.stats_manager.data["theme"])
        ttk.OptionMenu(self, self.theme_var, self.theme_var.get(), *themes).pack(pady=5)
        tk.Button(self, text="Speichern", command=self._save_settings).pack(pady=10)
        tk.Button(self, text="Zurück", command=self._build_start).pack(pady=5)

    def _save_settings(self) -> None:
        assert self.stats_manager is not None
        self.stats_manager.data["language"] = self.lang_var.get()
        self.stats_manager.data["theme"] = self.theme_var.get()
        self.stats_manager._save()
        self._apply_theme()
        self._build_start()

    # ----- reporting for teachers -------------------------------------
    def _reporting(self) -> None:
        self._clear()
        tk.Label(self, text="Reporting", font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        if not os.path.exists(USERS_DIR):
            tk.Label(self, text="Keine Benutzer", bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        else:
            for fname in os.listdir(USERS_DIR):
                if fname.endswith(".json"):
                    with open(os.path.join(USERS_DIR, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    name = fname[:-5]
                    pts = data.get("points", 0)
                    level = pts // 100
                    tk.Label(
                        self,
                        text=f"{name}: Level {level}, Punkte {pts}",
                        bg=self.colors["bg"],
                        fg=self.colors["fg"],
                    ).pack()
        tk.Button(self, text="Zurück", command=self._build_start).pack(pady=20)


if __name__ == "__main__":
    app = TypingTrainer()
    app.mainloop()


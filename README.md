# AlphaTast Clone

Ein erweiterter Tipptrainer inspiriert von [alphatast.de](http://alphatast.de/).

## Funktionen

- Benutzerverwaltung mit Schüler- und Lehrer-Konten
- Verschiedene Übungsmodi (Buchstaben-Mix, Wortreihen, Satzaufbau, eigener Text)
- Gamification (Punkte, Level, Abzeichen)
- Unterstützung für Deutsch und Englisch
- Lernstatistiken über mehrere Sitzungen
- Anpassbare Themes (hell/dunkel)

## Ausführen

```bash
python alphatast_clone.py
```

## Setup.exe erstellen

1. [PyInstaller](https://pyinstaller.org/) installieren.
2. Mit PyInstaller das Programm bauen:
   ```bash
   pyinstaller --onefile alphatast_clone.py
   ```
3. Mit [Inno Setup](https://jrsoftware.org/isinfo.php) und dem Skript `setup_script.iss` eine `setup.exe` erzeugen.


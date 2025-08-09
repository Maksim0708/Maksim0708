# AlphaTast Clone

Ein einfacher Tipptrainer ähnlich der Software von [alphatast.de](http://alphatast.de/).

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


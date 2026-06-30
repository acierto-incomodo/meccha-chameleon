./Clear.ps1
python -m PyInstaller --onefile --windowed --noconsole --icon=meccha-chameleon.ico NoCompatibleToInstall.py
echo v2.2.1 > GameVersion.txt
./Clear.ps1
python -m PyInstaller --onefile --windowed --noconsole --icon=meccha-chameleon.ico NoCompatibleToInstall.py
echo v1.1.1 > GameVersion.txt
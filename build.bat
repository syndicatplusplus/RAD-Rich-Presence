@echo off
py -m PyInstaller --noconfirm --onedir --noconsole --name RADRichPresence rad_rich_presence.py
copy .env dist\RADRichPresence\
copy ra_logo.png dist\RADRichPresence\
echo Build complete!
pause
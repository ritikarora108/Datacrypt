@echo off
 
set /p filename=Please enter the file name:
 
pyinstaller --onefile --noconsole --icon=logo_icon.ico  --splash "splashscr.png" --add-data ".\*;directory" %filename%.py
 
pause
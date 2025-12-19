@echo off
echo Сборка минимального исполняемого файла...
pyinstaller --onefile --windowed --name "МиМиПереводчик" ^
--add-data "tesseract;tesseract" ^
--hidden-import=pytesseract ^
--hidden-import=googletrans ^
--hidden-import=pynput.keyboard ^
--hidden-import=PIL.Image ^
--upx-dir "C:\upx" ^
main_app.py

echo.
echo Готово! Минимальный исполняемый файл создан.
pause
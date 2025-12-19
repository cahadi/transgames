@echo off
chcp 65001 > nul
echo Установка Tesseract OCR для переводчика...
echo.

where tesseract >nul 2>&1
if %errorlevel% equ 0 (
    echo Tesseract уже установлен в системе.
    goto :end
)

echo Скачивание Tesseract OCR...
powershell -Command "Invoke-WebRequest -Uri 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe' -OutFile 'tesseract-setup.exe'"

if exist "tesseract-setup.exe" (
    echo Запуск установки Tesseract...
    start /wait tesseract-setup.exe
    del tesseract-setup.exe
    echo Tesseract успешно установлен!
) else (
    echo Не удалось скачать Tesseract.
    echo Пожалуйста, установите вручную с:
    echo https://github.com/UB-Mannheim/tesseract/wiki
)

:end
echo.
pause
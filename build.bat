@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    Ми-Ми Переводчик - Умная Сборка
echo ========================================

title Ми-Ми Переводчик - Сборка

:: Проверка прав администратора
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ЗАМЕЧАНИЕ: Запуск без прав администратора
    echo Для полной функциональности рекомендуется запуск от имени администратора
    echo.
)

:: Функция проверки Python
call :check_python
if !python_ok! neq 1 (
    echo.
    echo Установка Python 3.11.5...
    call :install_python
    if !python_ok! neq 1 (
        echo НЕУДАЧА: Не удалось установить Python
        echo Пожалуйста, установите Python вручную с https://python.org
        pause
        exit /b 1
    )
)

echo.
echo Python !python_version! обнаружен и готов к работе!

:: Установка библиотек
call :install_dependencies

:: Сборка
call :build_exe

echo.
echo ========================================
echo СБОРКА ЗАВЕРШЕНА УСПЕШНО!
echo ========================================
echo.
echo Ваш исполняемый файл: dist\МиМиПереводчик.exe
echo.
echo Перенесите его в удобное место и запускайте!
echo.
pause
exit /b 0

:check_python
set python_ok=0
for %%I in (python.exe) do set "python_path=%%~$PATH:I"
if defined python_path (
    for /f "tokens=*" %%V in ('python --version 2^>^&1') do (
        set "python_version=%%V"
        set python_ok=1
    )
)
exit /b 0

:install_python
echo Скачивание установщика Python...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe" -OutFile "python_setup.exe" -UserAgent "Mozilla/5.0"
if not exist "python_setup.exe" (
    echo Не удалось скачать Python. Пожалуйста, установите вручную.
    exit /b 0
)

echo Установка Python... (это может занять несколько минут)
start /wait python_setup.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_launcher=1
del python_setup.exe

:: Обновление переменной PATH в текущей сессии
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts

:: Повторная проверка
call :check_python
exit /b 0

:install_dependencies
echo.
echo Установка необходимых библиотек...
echo.

set libs=pyinstaller googletrans==3.1.0a0 pytesseract pyautogui pynput pillow

for %%L in (!libs!) do (
    echo Установка: %%L
    pip install %%L --quiet
    if !errorlevel! neq 0 (
        echo Проблема с установкой %%L, пробуем с флагом --user...
    pip install %%L --user --quiet
)

:: Проверка установленных библиотек
echo.
echo Проверка установленных библиотек...
python -c "import pyautogui, pytesseract, pynput, PIL, googletrans; print('Все библиотеки установлены успешно!')" 2>nul
if !errorlevel! neq 0 (
    echo ВНИМАНИЕ: Не все библиотеки установились корректно
    echo Продолжаем сборку...
)
exit /b 0

:build_exe
echo.
echo Начало сборки исполняемого файла...
echo.

set build_success=0

:: Попытка 1 - Полная сборка
echo Попытка 1: Полная сборка со всеми зависимостями...
pyinstaller --onefile --windowed --name "МиМиПереводчик" ^
--add-data "tesseract;tesseract" ^
--hidden-import=pytesseract ^
--hidden-import=googletrans ^
--hidden-import=pynput.keyboard ^
--hidden-import=PIL.Image ^
--collect-all googletrans ^
--collect-all pytesseract ^
main_app.py

if !errorlevel! equ 0 (
    set build_success=1
    echo Полная сборка успешна!
) else (
    echo Полная сборка не удалась, пробуем упрощенную...
    
    :: Попытка 2 - Упрощенная сборка
    echo Попытка 2: Упрощенная сборка...
    pyinstaller --onefile --windowed --name "МиМиПереводчик" main_app.py
    
    if !errorlevel! equ 0 (
        set build_success=1
        echo Упрощенная сборка успешна!
    ) else (
        echo ОШИБКА: Не удалось собрать исполняемый файл
    echo Попробуйте запустить от имени администратора
    )
)

if !build_success! equ 1 (
    if exist "dist\МиМиПереводчик.exe" (
        echo Исполняемый файл создан успешно!
        echo Размер файла: 
        for %%F in (dist\МиМиПереводчик.exe) do echo   %%F - %%~zF байт
) else (
    echo Файл не найден в папке dist\
    )
)
exit /b 0
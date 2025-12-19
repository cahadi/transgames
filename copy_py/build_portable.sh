echo "=== Создание готового portable пакета ==="

mkdir -p CuteTranslator
cd CuteTranslator

cp ../updated_cute_window.py .
cp ../updated_translator.py .

cat > install_dependencies.bat << 'EOF'
@echo off
chcp 65001 > nul
echo Установка зависимостей для переводчика...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден в системе!
    echo Пожалуйста, установите Python с https://www.python.org/downloads/
    echo При установке отметьте "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Установка pyautogui...
pip install pyautogui==0.9.54

echo Установка pytesseract...
pip install pytesseract==0.3.10

echo Установка Pillow...
pip install Pillow==10.2.0

echo Установка googletrans...
pip install googletrans==3.1.0a0

echo Установка pynput...
pip install pynput==1.7.6

echo.
echo Все зависимости успешно установлены!
echo Запуск приложения: python updated_cute_window.py
echo.
pause
EOF

cat > README.txt << 'EOF'
МИ-МИ-МИ ПЕРЕВОДЧИК ДЛЯ ИГР

ПРЕДВАРИТЕЛЬНЫЕ ТРЕБОВАНИЯ:
1. Python 3.6+ для Windows
2. Tesseract OCR для Windows

ИНСТРУКЦИЯ:

1. Установите Python: https://www.python.org/downloads/
   - При установке отметьте "Add Python to PATH"

2. Установите Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

3. Запустите install_dependencies.bat

4. Запустите приложение: python updated_cute_window.py

ГОРЯЧИЕ КЛАВИШИ:
- F2: Распознать текст вокруг курсора
- F3: Перевести распознанный текст
- F4: Выход

Проблемы?
- Проверьте, что Python добавлен в PATH
- Запустите командную строку от имени администратора

Приятного использования! :3
EOF

cd ..

zip -r CuteTranslator_Windows.zip CuteTranslator/

rm -rf CuteTranslator

echo
echo "=== ГОТОВО! ==="
echo "Создан файл: CuteTranslator_Windows.zip"
echo
echo "Пользователю на Windows нужно:"
echo "1. Распаковать архив"
echo "2. Запустить install_dependencies.bat"
echo "3. Запустить: python updated_cute_window.py"
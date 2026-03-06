@echo off
chcp 65001 >nul
color 0a
title Bot Launcher

echo ========================================
echo       Bot Launcher - Запуск бота
echo ========================================

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: Python не установлен или не добавлен в PATH.
    echo Убедитесь, что Python установлен и доступен из командной строки.
    pause
    exit /b 1
)

:: Проверка существования файла bot.py
if not exist "bot.py" (
    echo.
    echo ОШИБКА: Файл bot.py не найден в текущей директории.
    pause
    exit /b 1
)

:: Установка зависимостей из requirements.txt (если файл существует)
if exist "requirements.txt" (
    echo.
    echo Установка зависимостей из requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ОШИБКА при установке зависимостей. Проверьте интернет-соединение и файл requirements.txt.
        pause
        exit /b 1
    )
) else (
    :: Если requirements.txt нет, устанавливаем telebot
    echo.
    echo Установка библиотеки telebot...
    python -m pip install telebot
    if %errorlevel% neq 0 (
        echo.
        echo ОШИБКА при установке telebot. Проверьте интернет-соединение.
        pause
        exit /b 1
    )
)

:: Запуск бота
echo.
echo Запуск бота...
echo --------------------------------------
py bot.py

:: Ждём нажатия клавиши перед закрытием (на случай, если бот аварийно завершит работу)
pause

@echo off
chcp 65001 >nul
color 0a
title Bot Launcher

echo ========================================
echo       Bot Launcher - Запуск бота
echo ========================================

:: Проверка существования файла bot.py
if not exist "bot.py" (
    echo.
    echo ОШИБКА: Файл bot.py не найден в текущей директории.
    pause
    exit /b 1
)

:: Проверка существования виртуального окружения .venv
if not exist ".venv" (
    echo.
    echo ОШИБКА: Виртуальное окружение .venv не найдено в текущей директории.
    echo Создайте его с помощью команды: python -m venv .venv
    pause
    exit /b 1
)

:: Активация виртуального окружения
echo.
echo Активация виртуального окружения .venv...
call ".venv\Scripts\activate.bat"

if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: Не удалось активировать виртуальное окружение.
    pause
    exit /b 1
)

:: Запуск бота
echo.
echo Запуск бота...
echo --------------------------------------
py bot.py

:: Ждём нажатия клавиши перед закрытием (на случай, если бот аварийно завершит работу)
pause

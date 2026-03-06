import telebot
import subprocess
import time
import platform
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
TOKEN = '8693747716:AAF-2nfOQypgqEnWJ5kMSJpim0iJmlgQ6E4'
CHAT_ID = '-1003437057605'

HOSTS = {
    '172.20.98.1': None,
    '172.20.98.8': None,
}

CHECK_INTERVAL = 10
# --------------------

bot = telebot.TeleBot(TOKEN)


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def check_ping(ip):
    timeout_val = "5000" if platform.system().lower() == "windows" else "5"

    if platform.system().lower() == "windows":
        command = f"ping -n 1 -w {timeout_val} {ip}"
    else:
        command = f"ping -c 1 -W {timeout_val} {ip}"

    try:
        encoding = "cp866" if platform.system().lower() == "windows" else "utf-8"

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding=encoding
        )

        output = (result.stdout + result.stderr).lower()

        unreachable_keywords = [
            "заданный узел недоступен",
            "destination host unreachable",
            "превышен интервал",
            "request timed out",
            "general failure",
            "размер пакета превышен"
        ]

        for keyword in unreachable_keywords:
            if keyword in output:
                return False

        if f"ответ от {ip}:" in output or f"reply from {ip}:" in output:
            return True

        return False

    except Exception as e:
        print(f"[{get_time()}] Ошибка: {e}")
        return False


def send_message(text):
    try:
        bot.send_message(CHAT_ID, text, parse_mode='HTML')
    except Exception as e:
        print(f"[{get_time()}] Ошибка отправки: {e}")


def main():
    print("=" * 50)
    print(f"Мониторинг запущен | {get_time()}")
    print(f"ОС: {platform.system()}")
    print("Хосты:")
    for ip in HOSTS:
        print(f"  • {ip}")
    print(f"Интервал: {CHECK_INTERVAL} сек")
    print("=" * 50)

    while True:
        print(f"\n[{get_time()}] Начало проверки...")

        for ip in HOSTS:
            is_up = check_ping(ip)
            status_text = "ОК" if is_up else "Упал"
            print(f"[{get_time()}] {ip}: {status_text}")

            if is_up:
                if HOSTS[ip] is False:
                    msg = f"✅ <b>Восстановлено</b>: {ip} снова в сети!"
                    print(f"[{get_time()}] >>> {msg}")
                    send_message(msg)
                    HOSTS[ip] = True
                elif HOSTS[ip] is None:
                    HOSTS[ip] = True
            else:
                if HOSTS[ip] is True or HOSTS[ip] is None:
                    msg = f"🚨 <b>Тревога</b>: {ip} недоступен!"
                    print(f"[{get_time()}] >>> {msg}")
                    send_message(msg)
                    HOSTS[ip] = False

        print(f"[{get_time()}] Ожидание {CHECK_INTERVAL} сек...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

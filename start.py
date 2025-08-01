#!/usr/bin/env python3
"""
Скрипт для запуска всех компонентов магазина
"""

import subprocess
import sys
import time
import os
from threading import Thread

def run_server(script_name, description):
    """Запуск сервера в отдельном потоке"""
    try:
        print(f"🚀 Запуск {description}...")
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска {description}: {e}")
    except KeyboardInterrupt:
        print(f"⏹️ Остановка {description}")

def check_dependencies():
    """Проверка зависимостей"""
    try:
        import telegram
        import flask
        import flask_cors
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False

def check_config():
    """Проверка конфигурации"""
    if not os.path.exists('.env'):
        print("⚠️ Файл .env не найден")
        print("Создайте файл .env с содержимым:")
        print("BOT_TOKEN=your_bot_token_here")
        return False
    
    print("✅ Конфигурация проверена")
    return True

def main():
    """Главная функция"""
    print("🛍️ Запуск Telegram Mini App - Магазин")
    print("=" * 50)
    
    # Проверки
    if not check_dependencies():
        return
    
    if not check_config():
        return
    
    print("\n📋 Запуск серверов:")
    print("• API сервер (порт 5000)")
    print("• Веб-сервер (порт 8000)")
    print("• Telegram бот")
    print("\nНажмите Ctrl+C для остановки всех серверов")
    print("=" * 50)
    
    # Запуск серверов в отдельных потоках
    threads = []
    
    # API сервер
    api_thread = Thread(target=run_server, args=('api_server.py', 'API сервера'))
    api_thread.daemon = True
    api_thread.start()
    threads.append(api_thread)
    
    # Небольшая задержка между запусками
    time.sleep(2)
    
    # Веб-сервер
    web_thread = Thread(target=run_server, args=('web_server.py', 'веб-сервера'))
    web_thread.daemon = True
    web_thread.start()
    threads.append(web_thread)
    
    # Небольшая задержка между запусками
    time.sleep(2)
    
    # Telegram бот
    bot_thread = Thread(target=run_server, args=('bot.py', 'Telegram бота'))
    bot_thread.daemon = True
    bot_thread.start()
    threads.append(bot_thread)
    
    try:
        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n⏹️ Остановка всех серверов...")
        print("👋 До свидания!")

if __name__ == '__main__':
    main() 
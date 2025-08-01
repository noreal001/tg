#!/usr/bin/env python3
"""
Скрипт для запуска приложения на Render
Запускает API сервер и веб-сервер в одном процессе
"""

import os
import sys
from flask import Flask, send_from_directory
from api_server import app as api_app
from database import Database

# Инициализация базы данных
db = Database()

# Создаем веб-приложение для статических файлов
web_app = Flask(__name__)
web_app.static_folder = 'web_app'

@web_app.route('/')
def index():
    return send_from_directory('web_app', 'index.html')

@web_app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('web_app', filename)

# Объединяем API и веб-сервер
def create_app():
    """Создаем объединенное приложение"""
    # Добавляем API маршруты к веб-приложению
    for rule in api_app.url_map.iter_rules():
        # Пропускаем статические маршруты, чтобы избежать конфликтов
        if rule.endpoint != 'static':
            web_app.add_url_rule(
                rule.rule,
                endpoint=rule.endpoint,
                view_func=api_app.view_functions[rule.endpoint],
                methods=rule.methods
            )
    return web_app

if __name__ == '__main__':
    app = create_app()
    
    # Получаем порт из переменной окружения Render
    port = int(os.environ.get('PORT', 8000))
    
    print(f"🚀 Запуск приложения на порту {port}")
    print("📱 Mini App доступен по адресу: /")
    print("🔌 API доступен по адресу: /api/")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Отключаем debug для продакшена
    ) 
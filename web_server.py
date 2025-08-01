from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Настройка статических файлов
app.static_folder = 'web_app'

@app.route('/')
def index():
    return send_from_directory('web_app', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('web_app', filename)

if __name__ == '__main__':
    print("🌐 Веб-сервер запущен на http://localhost:8000")
    print("📱 Mini App доступен по адресу: http://localhost:8000")
    app.run(debug=True, host='0.0.0.0', port=8000) 
#!/usr/bin/env python3
"""
WSGI файл для запуска на Render с Gunicorn
"""

import os
from render_start import create_app

# Создаем приложение
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 
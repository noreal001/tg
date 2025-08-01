#!/usr/bin/env python3
"""
WSGI файл для запуска на Render с Gunicorn
"""

from app import app

if __name__ == "__main__":
    app.run() 
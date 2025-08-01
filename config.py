import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('TOKEN', os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE'))

# Database
DATABASE_PATH = 'shop.db'

# Categories
CATEGORIES = {
    'oils': '🛢️ Масла',
    'bottles': '🧪 Флаконы', 
    'solutions': '💧 Растворы'
}

# Admin user IDs (замените на свои)
ADMIN_IDS = [123456789]  # Замените на ваш Telegram ID

# Delivery settings
DELIVERY_COST = 300  # Стоимость доставки в рублях
MIN_ORDER_FOR_FREE_DELIVERY = 2000  # Минимальная сумма для бесплатной доставки 
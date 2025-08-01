import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS
from database import Database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Создаем кнопку для запуска Mini App
    keyboard = [
        [InlineKeyboardButton("🛍️ Открыть магазин", web_app={"url": "https://your-domain.com/shop"})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🎉 Добро пожаловать в наш магазин!

Здесь вы найдете качественные масла, флаконы и растворы.

Нажмите кнопку ниже, чтобы открыть магазин:
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админская панель"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ У вас нет доступа к админ-панели.")
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("📦 Управление товарами", callback_data="admin_products")],
        [InlineKeyboardButton("📋 Заказы", callback_data="admin_orders")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔧 Админ-панель\n\nВыберите действие:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "admin_stats":
        await show_admin_stats(query)
    elif query.data == "admin_products":
        await show_admin_products(query)
    elif query.data == "admin_orders":
        await show_admin_orders(query)

async def show_admin_stats(query):
    """Показать статистику"""
    # Здесь можно добавить реальную статистику
    stats_text = """
📊 Статистика магазина:

🛢️ Масла: 3 товара
🧪 Флаконы: 3 товара  
💧 Растворы: 3 товара

📦 Всего заказов: 0
💰 Общая выручка: 0 ₽
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(stats_text, reply_markup=reply_markup)

async def show_admin_products(query):
    """Показать управление товарами"""
    products = db.get_all_products()
    
    text = "📦 Управление товарами:\n\n"
    for product in products:
        text += f"• {product['name']} - {product['price']} ₽ (остаток: {product['stock']})\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Добавить товар", callback_data="add_product")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_admin_orders(query):
    """Показать заказы"""
    text = "📋 Заказы:\n\nПока нет заказов."
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("🤖 Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main() 
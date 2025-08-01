# 🛍️ Telegram Mini App - Магазин

Современный минималистичный магазин в Telegram с красивым черно-белым дизайном.

## ✨ Особенности

- 🎨 **Минималистичный дизайн** - черно-белая цветовая схема
- 📱 **Telegram Mini App** - полноценное веб-приложение в Telegram
- 🛒 **Корзина** - добавление, изменение количества, удаление товаров
- 💳 **Оформление заказа** - форма с адресом доставки
- 🚚 **Доставка** - бесплатная от 2000₽, 300₽ при меньшей сумме
- 👨‍💼 **Админ-панель** - управление товарами через бота
- 📊 **База данных** - SQLite для хранения товаров и заказов

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка бота

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен бота
3. Создайте файл `.env`:

```env
BOT_TOKEN=your_bot_token_here
```

4. Обновите `config.py` - замените `ADMIN_IDS` на ваш Telegram ID

### 3. Запуск серверов

#### Запуск API сервера (порт 5000):
```bash
python api_server.py
```

#### Запуск веб-сервера (порт 8000):
```bash
python web_server.py
```

#### Запуск Telegram бота:
```bash
python bot.py
```

### 4. Настройка Mini App

1. В [@BotFather](https://t.me/BotFather) настройте Mini App:
   - `/newapp` - создайте новое приложение
   - Укажите название и описание
   - В поле URL введите: `http://localhost:8000`

2. Обновите URL в `bot.py`:
```python
web_app={"url": "http://localhost:8000"}
```

## 📁 Структура проекта

```
├── bot.py              # Telegram бот
├── api_server.py       # API сервер (Flask)
├── web_server.py       # Веб-сервер для Mini App
├── database.py         # Работа с базой данных
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
├── web_app/           # Mini App файлы
│   ├── index.html     # Главная страница
│   ├── styles.css     # Стили
│   └── app.js         # JavaScript логика
└── shop.db            # База данных SQLite
```

## 🛢️ Категории товаров

### Масла
- Кокосовое масло - 1200₽
- Масло жожоба - 1500₽  
- Аргановое масло - 1800₽

### Флаконы
- Стеклянный флакон 30мл - 250₽
- Флакон с распылителем - 350₽
- Дозатор-роллер - 400₽

### Растворы
- Глицериновый раствор - 800₽
- Спиртовой раствор - 600₽
- Масляный раствор - 950₽

## 🔧 Админ-функции

### Через бота:
- `/admin` - админ-панель
- Просмотр статистики
- Управление товарами
- Просмотр заказов

### Через API:
- `GET /api/admin/products` - все товары
- `POST /api/admin/products` - добавить товар
- `PUT /api/admin/products/{id}` - обновить товар
- `DELETE /api/admin/products/{id}` - удалить товар

## 🎨 Дизайн

- **Цветовая схема**: Черно-белая
- **Шрифты**: Системные (Apple/Google)
- **Анимации**: Плавные переходы
- **Адаптивность**: Мобильная оптимизация
- **Интерактивность**: Hover эффекты

## 📱 Использование

1. **Открытие магазина**: Нажмите кнопку "🛍️ Открыть магазин" в боте
2. **Просмотр категорий**: Выберите категорию товаров
3. **Добавление в корзину**: Нажмите "Добавить в корзину"
4. **Корзина**: Нажмите на иконку корзины в шапке
5. **Оформление заказа**: Заполните форму доставки

## 🔄 API Endpoints

### Товары
- `GET /api/products/{category}` - товары по категории
- `GET /api/products/{id}` - товар по ID

### Корзина
- `GET /api/cart/{user_id}` - корзина пользователя
- `POST /api/cart/add` - добавить в корзину
- `POST /api/cart/update` - обновить количество

### Заказы
- `POST /api/orders/create` - создать заказ
- `GET /api/orders/{user_id}` - заказы пользователя

## 🚀 Развертывание

### Локально
1. Установите зависимости
2. Настройте `.env` файл
3. Запустите все серверы
4. Настройте Mini App в BotFather

### На сервере
1. Загрузите файлы на сервер
2. Установите зависимости
3. Настройте домен и SSL
4. Обновите URL в боте
5. Запустите через systemd или Docker

## 🐛 Отладка

- **Логи бота**: В консоли при запуске
- **API логи**: Flask debug режим
- **База данных**: Файл `shop.db`
- **Веб-приложение**: Консоль браузера

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи серверов
2. Убедитесь, что все порты свободны
3. Проверьте настройки в `config.py`
4. Убедитесь, что база данных создана

## 🔮 Планы развития

- [ ] Интеграция с платежными системами
- [ ] Система отзывов
- [ ] Уведомления о статусе заказа
- [ ] Система скидок и промокодов
- [ ] Мобильное приложение
- [ ] Интеграция с CRM

---

**Создано с ❤️ для Telegram Mini Apps** 
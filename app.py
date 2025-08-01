#!/usr/bin/env python3
"""
Единое Flask приложение для Render
Объединяет API и веб-сервер
"""

import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from database import Database
from config import ADMIN_IDS, DELIVERY_COST, MIN_ORDER_FOR_FREE_DELIVERY

# Создаем приложение
app = Flask(__name__)
CORS(app)

# Инициализация базы данных
db = Database()

# Настройка статических файлов
app.static_folder = 'web_app'

# Веб-маршруты
@app.route('/')
def index():
    return send_from_directory('web_app', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('web_app', filename)

# API маршруты
@app.route('/api/products/<category>', methods=['GET'])
def get_products_by_category(category):
    """Получение товаров по категории"""
    try:
        products = db.get_products_by_category(category)
        return jsonify({
            'success': True,
            'products': products
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получение товара по ID"""
    try:
        product = db.get_product_by_id(product_id)
        if product:
            return jsonify({
                'success': True,
                'product': product
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Товар не найден'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Добавление товара в корзину"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not user_id or not product_id:
            return jsonify({
                'success': False,
                'error': 'Необходимы user_id и product_id'
            }), 400
        
        db.add_to_cart(user_id, product_id, quantity)
        
        return jsonify({
            'success': True,
            'message': 'Товар добавлен в корзину'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """Получение корзины пользователя"""
    try:
        cart_items = db.get_cart(user_id)
        return jsonify({
            'success': True,
            'cart': cart_items
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cart/update', methods=['POST'])
def update_cart_item():
    """Обновление количества товара в корзине"""
    try:
        data = request.get_json()
        cart_id = data.get('cart_id')
        quantity = data.get('quantity')
        
        if cart_id is None or quantity is None:
            return jsonify({
                'success': False,
                'error': 'Необходимы cart_id и quantity'
            }), 400
        
        db.update_cart_item(cart_id, quantity)
        
        return jsonify({
            'success': True,
            'message': 'Корзина обновлена'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders/create', methods=['POST'])
def create_order():
    """Создание заказа"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        delivery_address = data.get('delivery_address')
        
        if not user_id or not delivery_address:
            return jsonify({
                'success': False,
                'error': 'Необходимы user_id и delivery_address'
            }), 400
        
        # Получаем корзину пользователя
        cart_items = db.get_cart(user_id)
        
        if not cart_items:
            return jsonify({
                'success': False,
                'error': 'Корзина пуста'
            }), 400
        
        # Рассчитываем общую сумму
        total_amount = sum(item['total'] for item in cart_items)
        
        # Рассчитываем стоимость доставки
        delivery_cost = 0 if total_amount >= MIN_ORDER_FOR_FREE_DELIVERY else DELIVERY_COST
        
        # Создаем заказ
        order_id = db.create_order(user_id, total_amount, delivery_address, delivery_cost)
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'total_amount': total_amount + delivery_cost,
            'delivery_cost': delivery_cost
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Получение заказов пользователя"""
    try:
        orders = db.get_user_orders(user_id)
        return jsonify({
            'success': True,
            'orders': orders
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Админские эндпоинты
@app.route('/api/admin/products', methods=['GET'])
def admin_get_products():
    """Получение всех товаров (админ)"""
    try:
        products = db.get_all_products()
        return jsonify({
            'success': True,
            'products': products
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/products', methods=['POST'])
def admin_add_product():
    """Добавление товара (админ)"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')
        stock = data.get('stock')
        image_url = data.get('image_url', '')
        
        if not all([name, description, price, category, stock]):
            return jsonify({
                'success': False,
                'error': 'Необходимы все поля'
            }), 400
        
        product_id = db.add_product(name, description, price, category, stock, image_url)
        
        return jsonify({
            'success': True,
            'product_id': product_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
def admin_update_product(product_id):
    """Обновление товара (админ)"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')
        stock = data.get('stock')
        image_url = data.get('image_url', '')
        
        if not all([name, description, price, category, stock]):
            return jsonify({
                'success': False,
                'error': 'Необходимы все поля'
            }), 400
        
        db.update_product(product_id, name, description, price, category, stock, image_url)
        
        return jsonify({
            'success': True,
            'message': 'Товар обновлен'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
def admin_delete_product(product_id):
    """Удаление товара (админ)"""
    try:
        db.delete_product(product_id)
        
        return jsonify({
            'success': True,
            'message': 'Товар удален'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Запуск приложения на порту {port}")
    print("📱 Mini App доступен по адресу: /")
    print("🔌 API доступен по адресу: /api/")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    ) 
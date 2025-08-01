import sqlite3
import json
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица товаров
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image_url TEXT,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица корзин
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Таблица заказов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                delivery_address TEXT NOT NULL,
                delivery_cost REAL DEFAULT 0,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица элементов заказа
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Добавляем тестовые товары
        self.add_sample_products()
    
    def add_sample_products(self):
        """Добавление тестовых товаров"""
        sample_products = [
            # Масла
            ('Кокосовое масло', 'Натуральное кокосовое масло холодного отжима', 1200, 'oils', '', 50),
            ('Масло жожоба', 'Увлажняющее масло жожоба для ухода за кожей', 1500, 'oils', '', 30),
            ('Аргановое масло', 'Питательное аргановое масло для волос', 1800, 'oils', '', 25),
            
            # Флаконы
            ('Стеклянный флакон 30мл', 'Стильный стеклянный флакон с пипеткой', 250, 'bottles', '', 100),
            ('Флакон с распылителем', 'Удобный флакон с мелкодисперсным распылителем', 350, 'bottles', '', 80),
            ('Дозатор-роллер', 'Практичный дозатор-роллер для масел', 400, 'bottles', '', 60),
            
            # Растворы
            ('Глицериновый раствор', 'Увлажняющий раствор на основе глицерина', 800, 'solutions', '', 40),
            ('Спиртовой раствор', 'Антисептический спиртовой раствор', 600, 'solutions', '', 70),
            ('Масляный раствор', 'Концентрированный масляный раствор', 950, 'solutions', '', 35)
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже товары
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO products (name, description, price, category, image_url, stock)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_products)
        
        conn.commit()
        conn.close()
    
    def get_products_by_category(self, category):
        """Получение товаров по категории"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, price, stock, image_url
            FROM products 
            WHERE category = ? AND stock > 0
            ORDER BY name
        ''', (category,))
        
        products = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': p[0],
                'name': p[1],
                'description': p[2],
                'price': p[3],
                'stock': p[4],
                'image_url': p[5]
            }
            for p in products
        ]
    
    def get_product_by_id(self, product_id):
        """Получение товара по ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, price, stock, image_url, category
            FROM products 
            WHERE id = ?
        ''', (product_id,))
        
        product = cursor.fetchone()
        conn.close()
        
        if product:
            return {
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': product[3],
                'stock': product[4],
                'image_url': product[5],
                'category': product[6]
            }
        return None
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        """Добавление товара в корзину"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже товар в корзине
        cursor.execute('''
            SELECT id, quantity FROM carts 
            WHERE user_id = ? AND product_id = ?
        ''', (user_id, product_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Обновляем количество
            new_quantity = existing[1] + quantity
            cursor.execute('''
                UPDATE carts SET quantity = ? WHERE id = ?
            ''', (new_quantity, existing[0]))
        else:
            # Добавляем новый товар
            cursor.execute('''
                INSERT INTO carts (user_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (user_id, product_id, quantity))
        
        conn.commit()
        conn.close()
    
    def get_cart(self, user_id):
        """Получение корзины пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.quantity, p.id, p.name, p.price, p.stock
            FROM carts c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (user_id,))
        
        cart_items = cursor.fetchall()
        conn.close()
        
        return [
            {
                'cart_id': item[0],
                'quantity': item[1],
                'product_id': item[2],
                'name': item[3],
                'price': item[4],
                'stock': item[5],
                'total': item[1] * item[4]
            }
            for item in cart_items
        ]
    
    def update_cart_item(self, cart_id, quantity):
        """Обновление количества товара в корзине"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if quantity <= 0:
            cursor.execute('DELETE FROM carts WHERE id = ?', (cart_id,))
        else:
            cursor.execute('UPDATE carts SET quantity = ? WHERE id = ?', (quantity, cart_id))
        
        conn.commit()
        conn.close()
    
    def clear_cart(self, user_id):
        """Очистка корзины пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM carts WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def create_order(self, user_id, total_amount, delivery_address, delivery_cost):
        """Создание заказа"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем заказ
        cursor.execute('''
            INSERT INTO orders (user_id, total_amount, delivery_address, delivery_cost)
            VALUES (?, ?, ?, ?)
        ''', (user_id, total_amount, delivery_address, delivery_cost))
        
        order_id = cursor.lastrowid
        
        # Получаем товары из корзины
        cart_items = self.get_cart(user_id)
        
        # Добавляем элементы заказа
        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity'], item['price']))
            
            # Уменьшаем остаток на складе
            cursor.execute('''
                UPDATE products SET stock = stock - ? WHERE id = ?
            ''', (item['quantity'], item['product_id']))
        
        # Очищаем корзину
        self.clear_cart(user_id)
        
        conn.commit()
        conn.close()
        
        return order_id
    
    def get_user_orders(self, user_id):
        """Получение заказов пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, total_amount, delivery_address, delivery_cost, status, created_at
            FROM orders 
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        orders = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': order[0],
                'total_amount': order[1],
                'delivery_address': order[2],
                'delivery_cost': order[3],
                'status': order[4],
                'created_at': order[5]
            }
            for order in orders
        ]
    
    # Админские методы
    def add_product(self, name, description, price, category, stock, image_url=''):
        """Добавление нового товара (админ)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, description, price, category, stock, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, category, stock, image_url))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def update_product(self, product_id, name, description, price, category, stock, image_url=''):
        """Обновление товара (админ)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products 
            SET name = ?, description = ?, price = ?, category = ?, stock = ?, image_url = ?
            WHERE id = ?
        ''', (name, description, price, category, stock, image_url, product_id))
        
        conn.commit()
        conn.close()
    
    def delete_product(self, product_id):
        """Удаление товара (админ)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_products(self):
        """Получение всех товаров (админ)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, price, category, stock, image_url
            FROM products 
            ORDER BY category, name
        ''')
        
        products = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': p[0],
                'name': p[1],
                'description': p[2],
                'price': p[3],
                'category': p[4],
                'stock': p[5],
                'image_url': p[6]
            }
            for p in products
        ] 
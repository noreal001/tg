// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// Состояние приложения
let state = {
    currentView: 'categories',
    currentCategory: null,
    currentProduct: null,
    cart: [],
    user: tg.initDataUnsafe?.user || null
};

// API endpoints (замените на ваши реальные URL)
const API_BASE = 'http://localhost:5000/api';

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Настройка темы Telegram
    if (tg.colorScheme === 'dark') {
        document.body.style.background = '#000';
    }
    
    // Загружаем корзину из localStorage
    loadCart();
    updateCartCount();
}

function setupEventListeners() {
    // Категории
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            showProducts(category);
        });
    });

    // Кнопки навигации
    document.getElementById('cart-btn').addEventListener('click', showCart);
    document.getElementById('back-btn').addEventListener('click', showCategories);
    document.getElementById('back-to-products').addEventListener('click', showProducts);
    document.getElementById('back-to-main').addEventListener('click', showCategories);
    document.getElementById('back-to-cart').addEventListener('click', showCart);
}

// Навигация
function showCategories() {
    state.currentView = 'categories';
    hideAllSections();
    document.querySelector('.categories').style.display = 'block';
    document.querySelector('.categories').classList.add('fade-in');
}

function showProducts(category) {
    state.currentView = 'products';
    state.currentCategory = category;
    
    hideAllSections();
    document.getElementById('products-section').style.display = 'block';
    document.getElementById('products-section').classList.add('fade-in');
    
    // Обновляем заголовок
    const categoryNames = {
        'oils': '🛢️ Масла',
        'bottles': '🧪 Флаконы',
        'solutions': '💧 Растворы'
    };
    document.getElementById('category-title').textContent = categoryNames[category];
    
    // Загружаем товары
    loadProducts(category);
}

function showProductDetail(productId) {
    state.currentView = 'product-detail';
    state.currentProduct = productId;
    
    hideAllSections();
    document.getElementById('product-detail').style.display = 'block';
    document.getElementById('product-detail').classList.add('fade-in');
    
    loadProductDetail(productId);
}

function showCart() {
    state.currentView = 'cart';
    
    hideAllSections();
    document.getElementById('cart-section').style.display = 'block';
    document.getElementById('cart-section').classList.add('fade-in');
    
    renderCart();
}

function showCheckout() {
    state.currentView = 'checkout';
    
    hideAllSections();
    document.getElementById('checkout-section').style.display = 'block';
    document.getElementById('checkout-section').classList.add('fade-in');
    
    renderCheckout();
}

function hideAllSections() {
    document.querySelectorAll('section').forEach(section => {
        section.style.display = 'none';
        section.classList.remove('fade-in');
    });
}

// Загрузка данных
async function loadProducts(category) {
    const productsGrid = document.getElementById('products-grid');
    productsGrid.innerHTML = '<div class="loading">Загрузка товаров...</div>';
    
    try {
        // В реальном приложении здесь будет API запрос
        // Пока используем моковые данные
        const products = getMockProducts(category);
        renderProducts(products);
    } catch (error) {
        productsGrid.innerHTML = '<div class="empty-state">Ошибка загрузки товаров</div>';
    }
}

function loadProductDetail(productId) {
    const detailContent = document.getElementById('product-detail-content');
    detailContent.innerHTML = '<div class="loading">Загрузка...</div>';
    
    try {
        // В реальном приложении здесь будет API запрос
        const product = getMockProduct(productId);
        renderProductDetail(product);
    } catch (error) {
        detailContent.innerHTML = '<div class="empty-state">Ошибка загрузки товара</div>';
    }
}

// Рендеринг
function renderProducts(products) {
    const productsGrid = document.getElementById('products-grid');
    
    if (products.length === 0) {
        productsGrid.innerHTML = '<div class="empty-state"><h3>Товары не найдены</h3></div>';
        return;
    }
    
    productsGrid.innerHTML = products.map(product => `
        <div class="product-card" onclick="showProductDetail(${product.id})">
            <div class="product-image">
                ${getProductIcon(product.category)}
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <div class="product-price">${product.price} ₽</div>
                <div class="product-stock">Остаток: ${product.stock} шт.</div>
                <button class="add-to-cart-btn" onclick="event.stopPropagation(); addToCart(${product.id})">
                    Добавить в корзину
                </button>
            </div>
        </div>
    `).join('');
}

function renderProductDetail(product) {
    const detailContent = document.getElementById('product-detail-content');
    
    detailContent.innerHTML = `
        <div class="product-detail-image">
            ${getProductIcon(product.category)}
        </div>
        <div class="product-detail-info">
            <h3>${product.name}</h3>
            <div class="product-detail-description">${product.description}</div>
            <div class="product-detail-price">${product.price} ₽</div>
            <div class="quantity-controls">
                <button class="quantity-btn" onclick="changeQuantity(-1)">-</button>
                <span class="quantity-display" id="quantity-display">1</span>
                <button class="quantity-btn" onclick="changeQuantity(1)">+</button>
            </div>
            <button class="add-to-cart-btn" onclick="addToCartWithQuantity(${product.id})">
                Добавить в корзину
            </button>
        </div>
    `;
}

function renderCart() {
    const cartContent = document.getElementById('cart-content');
    
    if (state.cart.length === 0) {
        cartContent.innerHTML = '<div class="empty-state"><h3>Корзина пуста</h3></div>';
        return;
    }
    
    const cartItems = state.cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <div class="cart-item-price">${item.price} ₽</div>
            </div>
            <div class="cart-item-quantity">
                <button class="quantity-btn" onclick="updateCartItemQuantity(${item.id}, ${item.quantity - 1})">-</button>
                <span>${item.quantity}</span>
                <button class="quantity-btn" onclick="updateCartItemQuantity(${item.id}, ${item.quantity + 1})">+</button>
            </div>
        </div>
    `).join('');
    
    const total = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    cartContent.innerHTML = `
        ${cartItems}
        <div class="cart-total">
            Итого: ${total} ₽
        </div>
        <button class="checkout-btn" onclick="showCheckout()">
            Оформить заказ
        </button>
    `;
}

function renderCheckout() {
    const checkoutContent = document.getElementById('checkout-content');
    const total = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const deliveryCost = total >= 2000 ? 0 : 300;
    const finalTotal = total + deliveryCost;
    
    checkoutContent.innerHTML = `
        <div class="order-summary">
            <h3>Сводка заказа</h3>
            <div class="summary-item">
                <span>Товары:</span>
                <span>${total} ₽</span>
            </div>
            <div class="summary-item">
                <span>Доставка:</span>
                <span>${deliveryCost} ₽</span>
            </div>
            <div class="summary-total">
                <span>Итого:</span>
                <span>${finalTotal} ₽</span>
            </div>
        </div>
        
        <form id="checkout-form">
            <div class="form-group">
                <label for="name">Имя</label>
                <input type="text" id="name" required>
            </div>
            <div class="form-group">
                <label for="phone">Телефон</label>
                <input type="tel" id="phone" required>
            </div>
            <div class="form-group">
                <label for="address">Адрес доставки</label>
                <textarea id="address" rows="3" required></textarea>
            </div>
            <button type="submit" class="place-order-btn">Оформить заказ</button>
        </form>
    `;
    
    // Обработчик отправки формы
    document.getElementById('checkout-form').addEventListener('submit', handleOrderSubmit);
}

// Корзина
function addToCart(productId) {
    addToCartWithQuantity(productId, 1);
}

function addToCartWithQuantity(productId, quantity) {
    const product = getMockProduct(productId);
    
    const existingItem = state.cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        state.cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            quantity: quantity
        });
    }
    
    saveCart();
    updateCartCount();
    
    // Показываем уведомление
    tg.showAlert('Товар добавлен в корзину!');
}

function updateCartItemQuantity(productId, newQuantity) {
    if (newQuantity <= 0) {
        state.cart = state.cart.filter(item => item.id !== productId);
    } else {
        const item = state.cart.find(item => item.id === productId);
        if (item) {
            item.quantity = newQuantity;
        }
    }
    
    saveCart();
    updateCartCount();
    renderCart();
}

function loadCart() {
    const savedCart = localStorage.getItem('shop_cart');
    if (savedCart) {
        state.cart = JSON.parse(savedCart);
    }
}

function saveCart() {
    localStorage.setItem('shop_cart', JSON.stringify(state.cart));
}

function updateCartCount() {
    const count = state.cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

// Оформление заказа
async function handleOrderSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const orderData = {
        name: formData.get('name') || document.getElementById('name').value,
        phone: formData.get('phone') || document.getElementById('phone').value,
        address: formData.get('address') || document.getElementById('address').value,
        items: state.cart,
        total: state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    };
    
    try {
        // В реальном приложении здесь будет отправка на сервер
        console.log('Order data:', orderData);
        
        // Очищаем корзину
        state.cart = [];
        saveCart();
        updateCartCount();
        
        // Показываем успешное сообщение
        tg.showAlert('Заказ успешно оформлен! Мы свяжемся с вами в ближайшее время.');
        
        // Возвращаемся к категориям
        showCategories();
        
    } catch (error) {
        tg.showAlert('Ошибка при оформлении заказа. Попробуйте еще раз.');
    }
}

// Вспомогательные функции
function getProductIcon(category) {
    const icons = {
        'oils': '🛢️',
        'bottles': '🧪',
        'solutions': '💧'
    };
    return icons[category] || '📦';
}

function changeQuantity(delta) {
    const display = document.getElementById('quantity-display');
    let currentQuantity = parseInt(display.textContent);
    currentQuantity = Math.max(1, currentQuantity + delta);
    display.textContent = currentQuantity;
}

// Моковые данные (замените на реальные API вызовы)
function getMockProducts(category) {
    const products = {
        'oils': [
            { id: 1, name: 'Кокосовое масло', description: 'Натуральное кокосовое масло холодного отжима', price: 1200, stock: 50, category: 'oils' },
            { id: 2, name: 'Масло жожоба', description: 'Увлажняющее масло жожоба для ухода за кожей', price: 1500, stock: 30, category: 'oils' },
            { id: 3, name: 'Аргановое масло', description: 'Питательное аргановое масло для волос', price: 1800, stock: 25, category: 'oils' }
        ],
        'bottles': [
            { id: 4, name: 'Стеклянный флакон 30мл', description: 'Стильный стеклянный флакон с пипеткой', price: 250, stock: 100, category: 'bottles' },
            { id: 5, name: 'Флакон с распылителем', description: 'Удобный флакон с мелкодисперсным распылителем', price: 350, stock: 80, category: 'bottles' },
            { id: 6, name: 'Дозатор-роллер', description: 'Практичный дозатор-роллер для масел', price: 400, stock: 60, category: 'bottles' }
        ],
        'solutions': [
            { id: 7, name: 'Глицериновый раствор', description: 'Увлажняющий раствор на основе глицерина', price: 800, stock: 40, category: 'solutions' },
            { id: 8, name: 'Спиртовой раствор', description: 'Антисептический спиртовой раствор', price: 600, stock: 70, category: 'solutions' },
            { id: 9, name: 'Масляный раствор', description: 'Концентрированный масляный раствор', price: 950, stock: 35, category: 'solutions' }
        ]
    };
    
    return products[category] || [];
}

function getMockProduct(productId) {
    const allProducts = [
        ...getMockProducts('oils'),
        ...getMockProducts('bottles'),
        ...getMockProducts('solutions')
    ];
    
    return allProducts.find(p => p.id === productId);
} 
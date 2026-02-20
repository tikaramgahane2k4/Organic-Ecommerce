# ==================== USER ORDERS ====================
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

from functools import wraps
from flask_pymongo import PyMongo
from backend.config import Config
from backend.forms import RegistrationForm, LoginForm, CheckoutForm, ProductForm


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))
TEMPLATE_DIR = os.path.join(FRONTEND_DIR, 'templates')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)
app.config.from_object(Config)

# User Orders Route (moved here to ensure 'app' is defined)
@app.route('/orders')
@login_required
def orders():
    """Display user's orders (MongoDB)"""
    from bson import ObjectId
    user_orders = list(mongo.db.orders.find({'user_id': str(current_user.id)}))
    # Attach product details to each order (if needed)
    for order in user_orders:
        order['id'] = str(order['_id'])
    return render_template('orders.html', orders=user_orders)

# Initialize MongoDB
mongo = PyMongo(app, uri=app.config['MONGODB_URI'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'


# User class for Flask-Login with MongoDB
class MongoUser(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.name = user_doc.get('name')
        self.email = user_doc.get('email')
        self.password_hash = user_doc.get('password_hash')
        self.is_admin = user_doc.get('is_admin', False)

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    from bson import ObjectId
    user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return MongoUser(user_doc)
    return None


# ==================== ADMIN DECORATOR ====================
def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== DATA SEED (SAFETY) ====================
def seed_if_empty():
    """Populate baseline categories/products if the database is empty (MongoDB)."""
    if mongo.db.products.count_documents({}) > 0:
        return

    products = [
        # Vegetables
        {'name': 'Organic Tomatoes', 'description': 'Fresh, vine-ripened organic tomatoes. Perfect for salads and cooking. Rich in vitamins and antioxidants.', 'price': 49, 'stock': 50, 'category': 'Fresh Vegetables', 'image': 'tomatoes.jpg'},
        {'name': 'Organic Spinach', 'description': 'Tender organic spinach leaves, packed with iron and nutrients. Great for smoothies and salads.', 'price': 49, 'stock': 30, 'category': 'Fresh Vegetables', 'image': 'spinach.png'},
        {'name': 'Organic Carrots', 'description': 'Sweet and crunchy organic carrots. High in beta-carotene and fiber.', 'price': 49, 'stock': 60, 'category': 'Fresh Vegetables', 'image': 'carrot.png'},
        {'name': 'Organic Broccoli', 'description': 'Fresh organic broccoli crowns. Excellent source of vitamins C and K.', 'price': 150, 'stock': 40, 'category': 'Fresh Vegetables', 'image': 'broccoli.jpg'},
        # Fruits
        {'name': 'Organic Apples', 'description': 'Crisp and sweet organic apples. Perfect for snacking or baking.', 'price': 200, 'stock': 80, 'category': 'Organic Fruits', 'image': 'red-apple.png'},
        {'name': 'Organic Bananas', 'description': 'Naturally ripened organic bananas. Great source of potassium.', 'price': 49, 'stock': 100, 'category': 'Organic Fruits', 'image': 'banana.png'},
        {'name': 'Organic Strawberries', 'description': 'Sweet and juicy organic strawberries. Rich in vitamin C and antioxidants.', 'price': 300, 'stock': 35, 'category': 'Organic Fruits', 'image': 'strawberries.jpg'},
        {'name': 'Organic Oranges', 'description': 'Fresh and tangy organic oranges. Perfect for juice or eating fresh.', 'price': 150, 'stock': 70, 'category': 'Organic Fruits', 'image': 'orange.png'},
        {'name': 'Fresh Avocado', 'description': 'Creamy organic avocados. Perfect for toast, salads, and guacamole.', 'price': 350, 'stock': 45, 'category': 'Organic Fruits', 'image': 'avocado.png'},
        {'name': 'Fresh Guava', 'description': 'Sweet and fragrant organic guavas. Rich in vitamin C and fiber.', 'price': 150, 'stock': 55, 'category': 'Organic Fruits', 'image': 'gwava.png'},
        # Grains
        {'name': 'Organic Brown Rice', 'description': 'Premium quality organic brown rice. High in fiber and nutrients.', 'price': 200, 'stock': 100, 'category': 'Grains & Cereals', 'image': 'brown-rice.jpg'},
        {'name': 'Organic Quinoa', 'description': 'Protein-rich organic quinoa. Perfect for healthy meals.', 'price': 300, 'stock': 50, 'category': 'Grains & Cereals', 'image': 'quinoa.jpg'},
        {'name': 'Organic Oats', 'description': 'Whole grain organic oats. Perfect for breakfast and baking.', 'price': 150, 'stock': 80, 'category': 'Grains & Cereals', 'image': 'oats.png'},
        # Dairy
        {'name': 'Organic Milk', 'description': 'Fresh organic milk from grass-fed cows. Rich and creamy.', 'price': 49, 'stock': 45, 'category': 'Dairy Products', 'image': 'milk.png'},
        {'name': 'Organic Cheese', 'description': 'Artisan organic cheese. Made from organic milk with no additives.', 'price': 500, 'stock': 30, 'category': 'Dairy Products', 'image': 'cheese.jpg'},
        {'name': 'Organic Yogurt', 'description': 'Creamy organic yogurt with live cultures. Great for digestion.', 'price': 49, 'stock': 60, 'category': 'Dairy Products', 'image': 'yogurt.jpg'},
        {'name': 'Farm Fresh Eggs', 'description': 'Organic free-range eggs. Rich in protein and omega-3.', 'price': 150, 'stock': 65, 'category': 'Dairy Products', 'image': 'eggs.png'},
        # Herbs & Spices
        {'name': 'Organic Basil', 'description': 'Fresh organic basil leaves. Perfect for Italian dishes.', 'price': 49, 'stock': 40, 'category': 'Herbs & Spices', 'image': 'basil.jpg'},
        {'name': 'Organic Turmeric', 'description': 'Premium organic turmeric powder. Known for anti-inflammatory properties.', 'price': 200, 'stock': 50, 'category': 'Herbs & Spices', 'image': 'turmeric.jpg'},
        {'name': 'Extra Virgin Olive Oil', 'description': 'Cold-pressed organic olive oil. Perfect for cooking and salads.', 'price': 500, 'stock': 40, 'category': 'Herbs & Spices', 'image': 'olive oil.png'},
        # Honey
        {'name': 'Raw Organic Honey', 'description': 'Pure, unfiltered organic honey. Natural sweetener with health benefits.', 'price': 350, 'stock': 35, 'category': 'Organic Honey', 'image': 'honey.png'},
        {'name': 'Organic Oranges', 'description': 'Fresh and tangy organic oranges. Perfect for juice or eating fresh.', 'price': 399, 'stock': 70, 'category': 'Organic Fruits', 'image': 'orange.png'},
        {'name': 'Fresh Avocado', 'description': 'Creamy organic avocados. Perfect for toast, salads, and guacamole.', 'price': 599, 'stock': 45, 'category': 'Organic Fruits', 'image': 'avocado.png'},
        {'name': 'Fresh Guava', 'description': 'Sweet and fragrant organic guavas. Rich in vitamin C and fiber.', 'price': 359, 'stock': 55, 'category': 'Organic Fruits', 'image': 'gwava.png'},
        # Grains
        {'name': 'Organic Brown Rice', 'description': 'Premium quality organic brown rice. High in fiber and nutrients.', 'price': 719, 'stock': 100, 'category': 'Grains & Cereals', 'image': 'brown-rice.jpg'},
        {'name': 'Organic Quinoa', 'description': 'Protein-rich organic quinoa. Perfect for healthy meals.', 'price': 1039, 'stock': 50, 'category': 'Grains & Cereals', 'image': 'quinoa.jpg'},
        {'name': 'Organic Oats', 'description': 'Whole grain organic oats. Perfect for breakfast and baking.', 'price': 559, 'stock': 80, 'category': 'Grains & Cereals', 'image': 'oats.png'},
        # Dairy
        {'name': 'Organic Milk', 'description': 'Fresh organic milk from grass-fed cows. Rich and creamy.', 'price': 439, 'stock': 45, 'category': 'Dairy Products', 'image': 'milk.png'},
        {'name': 'Organic Cheese', 'description': 'Artisan organic cheese. Made from organic milk with no additives.', 'price': 799, 'stock': 30, 'category': 'Dairy Products', 'image': 'cheese.jpg'},
        {'name': 'Organic Yogurt', 'description': 'Creamy organic yogurt with live cultures. Great for digestion.', 'price': 359, 'stock': 60, 'category': 'Dairy Products', 'image': 'yogurt.jpg'},
        {'name': 'Farm Fresh Eggs', 'description': 'Organic free-range eggs. Rich in protein and omega-3.', 'price': 529, 'stock': 65, 'category': 'Dairy Products', 'image': 'eggs.png'},
        # Herbs & Spices
        {'name': 'Organic Basil', 'description': 'Fresh organic basil leaves. Perfect for Italian dishes.', 'price': 239, 'stock': 40, 'category': 'Herbs & Spices', 'image': 'basil.jpg'},
        {'name': 'Organic Turmeric', 'description': 'Premium organic turmeric powder. Known for anti-inflammatory properties.', 'price': 639, 'stock': 50, 'category': 'Herbs & Spices', 'image': 'turmeric.jpg'},
        {'name': 'Extra Virgin Olive Oil', 'description': 'Cold-pressed organic olive oil. Perfect for cooking and salads.', 'price': 1299, 'stock': 40, 'category': 'Herbs & Spices', 'image': 'olive oil.png'},
        # Honey
        {'name': 'Raw Organic Honey', 'description': 'Pure, unfiltered organic honey. Natural sweetener with health benefits.', 'price': 1199, 'stock': 35, 'category': 'Organic Honey', 'image': 'honey.png'},
    ]
    for prod in products:
        if mongo.db.products.find_one({'name': prod['name']}):
            continue
        # Find category _id
        cat_doc = mongo.db.categories.find_one({'name': prod['category']})
        if not cat_doc:
            continue
        prod['category_id'] = cat_doc['_id']
        mongo.db.products.insert_one(prod)


def create_default_admin():
    """Create default admin user if not exists (MongoDB)"""
    ADMIN_EMAIL = "admin@greenharvest.com"
    ADMIN_PASSWORD = "admin123"
    ADMIN_NAME = "Admin User"
    admin = mongo.db.users.find_one({'email': ADMIN_EMAIL})
    from werkzeug.security import generate_password_hash
    if not admin:
        user_doc = {
            'name': ADMIN_NAME,
            'email': ADMIN_EMAIL,
            'password_hash': generate_password_hash(ADMIN_PASSWORD),
            'is_admin': True
        }
        mongo.db.users.insert_one(user_doc)
        print(f"✓ Default admin created: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    elif not admin.get('is_admin', False):
        mongo.db.users.update_one({'_id': admin['_id']}, {'$set': {'is_admin': True}})
        print(f"✓ User {ADMIN_EMAIL} promoted to admin")


# ==================== HOME PAGE ====================

from backend.api import api as api_blueprint
app.register_blueprint(api_blueprint)
# Ensure baseline data and indexes exist on import (gunicorn)
def ensure_indexes():
    # Index for fast product lookup by category and sorting
    mongo.db.products.create_index([('category_id', 1)])
    mongo.db.products.create_index([('created_at', -1)])
    # Index for fast category name lookup
    mongo.db.categories.create_index([('name', 1)])
    # Index for fast order lookup by user
    mongo.db.orders.create_index([('user_id', 1)])

with app.app_context():
    seed_if_empty()
    create_default_admin()
    ensure_indexes()


@app.route('/')
def index():
    """Home page with featured products and categories (MongoDB)"""
    categories = list(mongo.db.categories.find().limit(4))
    featured_products = list(mongo.db.products.find().limit(8))
    return render_template('index.html', categories=categories, products=featured_products)


# ==================== CATEGORIES ====================

@app.route('/categories')
def categories():
    """Display all categories with products (MongoDB)"""
    from bson import ObjectId
    category_id = request.args.get('category')
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', '')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)

    # Get all categories with product counts
    all_categories = list(mongo.db.categories.find())
    for cat in all_categories:
        cat['product_count'] = mongo.db.products.count_documents({'category_id': cat['_id']})

    # Build product query
    query = {}
    if category_id:
        try:
            query['category_id'] = ObjectId(category_id)
        except Exception:
            query['category_id'] = category_id
        current_category = mongo.db.categories.find_one({'_id': query['category_id']})
    else:
        current_category = None
    if search_query:
        query['$or'] = [
            {'name': {'$regex': search_query, '$options': 'i'}},
            {'description': {'$regex': search_query, '$options': 'i'}}
        ]
    if price_min is not None:
        query['price'] = query.get('price', {})
        query['price']['$gte'] = price_min
    if price_max is not None:
        query['price'] = query.get('price', {})
        query['price']['$lte'] = price_max

    # Sorting
    sort = None
    if sort_by == 'high_to_low':
        sort = [('price', -1)]
    elif sort_by == 'low_to_high':
        sort = [('price', 1)]

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    skip = (page - 1) * per_page

    # Get min/max price for slider
    price_stats = mongo.db.products.aggregate([
        {"$group": {"_id": None, "min": {"$min": "$price"}, "max": {"$max": "$price"}}}
    ])
    price_stats = list(price_stats)
    min_price = int(price_stats[0]['min']) if price_stats else 0
    max_price = int(price_stats[0]['max']) if price_stats else 10000

    total_products = mongo.db.products.count_documents(query)
    products_cursor = mongo.db.products.find(query, sort=sort) if sort else mongo.db.products.find(query)
    products = list(products_cursor.skip(skip).limit(per_page))

    # Attach category name and wishlist state to each product
    category_map = {str(cat['_id']): cat['name'] for cat in all_categories}
    wishlist_ids = set()
    if current_user.is_authenticated:
        wishlist_items = list(mongo.db.wishlist.find({'user_id': str(current_user.id)}))
        wishlist_ids = set(item['product_id'] for item in wishlist_items)
    for prod in products:
        cat_id = str(prod.get('category_id'))
        prod['category_name'] = category_map.get(cat_id, '')
        prod['id'] = str(prod['_id'])
        prod['in_wishlist'] = str(prod['_id']) in wishlist_ids

    # Prefill cart quantities for inline controls
    cart_quantities = {}
    if current_user.is_authenticated:
        cart_items = list(mongo.db.cart.find({'user_id': str(current_user.id)}))
        cart_quantities = {item['product_id']: item['quantity'] for item in cart_items}

    total_pages = (total_products + per_page - 1) // per_page

    return render_template('categories.html',
                         categories=all_categories,
                         products=products,
                         current_category=current_category,
                         search_query=search_query,
                         cart_quantities=cart_quantities,
                         min_price=min_price,
                         max_price=max_price,
                         page=page,
                         total_pages=total_pages,
                         total_products=total_products)


# ==================== SHOP / PRODUCTS ====================

@app.route('/shop')
def shop():
    """Display all products with optional category filter (MongoDB)"""
    from bson import ObjectId
    category_id = request.args.get('category')
    if category_id:
        try:
            cat_id = ObjectId(category_id)
        except Exception:
            cat_id = category_id
        products = list(mongo.db.products.find({'category_id': cat_id}))
        current_category = mongo.db.categories.find_one({'_id': cat_id})
    else:
        products = list(mongo.db.products.find())
        current_category = None
    categories = list(mongo.db.categories.find())
    cart_quantities = {}
    if current_user.is_authenticated:
        cart_items = list(mongo.db.cart.find({'user_id': str(current_user.id)}))
        cart_quantities = {item['product_id']: item['quantity'] for item in cart_items}
    return render_template('shop.html', products=products, categories=categories,
                         current_category=current_category, cart_quantities=cart_quantities)



@app.route('/product/<product_id>')
def product_detail(product_id):
    """Display product details (MongoDB)"""
    from bson import ObjectId
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return abort(404)
    in_wishlist = False
    item_quantity = 0
    if current_user.is_authenticated:
        in_wishlist = mongo.db.wishlist.find_one({'user_id': str(current_user.id), 'product_id': product_id}) is not None
        cart_item = mongo.db.cart.find_one({'user_id': str(current_user.id), 'product_id': product_id})
        if cart_item:
            item_quantity = cart_item.get('quantity', 1)
    # Get related products from the same category
    related_products = list(mongo.db.products.find({
        'category_id': product['category_id'],
        '_id': {'$ne': product['_id']}
    }).limit(4))
    return render_template('product.html', product=product,
                         in_wishlist=in_wishlist,
                         related_products=related_products,
                         item_quantity=item_quantity)


# ==================== AUTHENTICATION ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login (MongoDB)"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_doc = mongo.db.users.find_one({'email': form.email.data})
        if user_doc:
            from werkzeug.security import check_password_hash
            if check_password_hash(user_doc['password_hash'], form.password.data):
                user = MongoUser(user_doc)
                login_user(user)
                flash('Login successful!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration (MongoDB)"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user with this email already exists
        existing_user = mongo.db.users.find_one({'email': form.email.data})
        if existing_user:
            flash('Email address already registered. Please use a different email or login.', 'danger')
            return render_template('register.html', form=form)
        from werkzeug.security import generate_password_hash
        user_doc = {
            'name': form.name.data,
            'email': form.email.data,
            'password_hash': generate_password_hash(form.password.data),
            'is_admin': False
        }
        mongo.db.users.insert_one(user_doc)
        # Auto-login after registration
        user_doc = mongo.db.users.find_one({'email': form.email.data})
        from flask_login import login_user
        user = MongoUser(user_doc)
        login_user(user)
        flash('Registration successful! Welcome, {}!'.format(user.name.split()[0]), 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ==================== ABOUT US & CONTACT ====================
@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Contact Us page"""
    return render_template('contact.html')


# ==================== WISHLIST ====================

@app.route('/wishlist')
@login_required
def wishlist():
    """Display user's wishlist (MongoDB)"""
    from bson import ObjectId
    wishlist_items = list(mongo.db.wishlist.find({'user_id': str(current_user.id)}))
    # Fetch product details for each wishlist item
    product_ids = [ObjectId(item['product_id']) for item in wishlist_items]
    products = {str(prod['_id']): prod for prod in mongo.db.products.find({'_id': {'$in': product_ids}})}
    for item in wishlist_items:
        item['product'] = products.get(item['product_id'])
    return render_template('wishlist.html', wishlist_items=wishlist_items)



@app.route('/wishlist/add/<product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """Add product to wishlist (MongoDB)"""
    from bson import ObjectId
    # Check if product exists
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    # Check if already in wishlist
    existing = mongo.db.wishlist.find_one({'user_id': str(current_user.id), 'product_id': product_id})
    if existing:
        mongo.db.wishlist.delete_one({'_id': existing['_id']})
        wishlist_count = mongo.db.wishlist.count_documents({'user_id': str(current_user.id)})
        return jsonify({
            'success': True,
            'message': 'Removed from wishlist',
            'wishlist_count': wishlist_count,
            'action': 'removed'
        })
    # Add to wishlist
    mongo.db.wishlist.insert_one({'user_id': str(current_user.id), 'product_id': product_id})
    wishlist_count = mongo.db.wishlist.count_documents({'user_id': str(current_user.id)})
    return jsonify({
        'success': True,
        'message': 'Added to wishlist',
        'wishlist_count': wishlist_count,
        'action': 'added'
    })



@app.route('/wishlist/remove/<product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    """Remove product from wishlist (MongoDB)"""
    existing = mongo.db.wishlist.find_one({'user_id': str(current_user.id), 'product_id': product_id})
    if existing:
        mongo.db.wishlist.delete_one({'_id': existing['_id']})
        flash('Product removed from wishlist', 'success')
    else:
        flash('Product not found in wishlist', 'warning')
    return redirect(url_for('wishlist'))


# ==================== CART ====================

@app.route('/cart')
@login_required
def cart():
    """Display shopping cart (MongoDB)"""
    from bson import ObjectId
    cart_items = list(mongo.db.cart.find({'user_id': str(current_user.id)}))
    # Fetch product details for each cart item
    product_ids = [ObjectId(item['product_id']) for item in cart_items]
    products = {str(prod['_id']): prod for prod in mongo.db.products.find({'_id': {'$in': product_ids}})}
    total = 0
    for item in cart_items:
        prod = products.get(item['product_id'])
        item['product'] = prod
        if prod:
            total += prod.get('price', 0) * item.get('quantity', 1)
    return render_template('cart.html', cart_items=cart_items, total=total)



@app.route('/cart/add/<product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart (MongoDB)"""
    from bson import ObjectId
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        try:
            quantity = int(payload.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
    else:
        quantity = request.form.get('quantity', 1, type=int)
    # Check if already in cart
    cart_item = mongo.db.cart.find_one({'user_id': str(current_user.id), 'product_id': product_id})
    if cart_item:
        new_quantity = cart_item.get('quantity', 1) + quantity
        mongo.db.cart.update_one({'_id': cart_item['_id']}, {'$set': {'quantity': new_quantity}})
    else:
        mongo.db.cart.insert_one({'user_id': str(current_user.id), 'product_id': product_id, 'quantity': quantity})
    cart_count = sum(item.get('quantity', 1) for item in mongo.db.cart.find({'user_id': str(current_user.id)}))
    if is_ajax:
        return jsonify({
            'success': True,
            'message': 'Product added to cart',
            'quantity': new_quantity if cart_item else quantity,
            'cart_count': cart_count
        })
    if request.form.get('next') == 'checkout':
        return redirect(url_for('checkout'))
    if request.form.get('redirect_to') == 'cart':
        flash('Product added to cart', 'success')
        return redirect(url_for('cart'))
    flash('Product added to cart', 'success')
    return redirect(request.referrer or url_for('categories'))



@app.route('/cart/update/<cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    """Update cart item quantity (MongoDB)"""
    from bson import ObjectId
    cart_item = mongo.db.cart.find_one({'_id': ObjectId(cart_id), 'user_id': str(current_user.id)})
    if not cart_item:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404
    quantity = request.form.get('quantity', 1, type=int)
    if quantity > 0:
        mongo.db.cart.update_one({'_id': cart_item['_id']}, {'$set': {'quantity': quantity}})
        return jsonify({'success': True, 'message': 'Cart updated'})
    else:
        mongo.db.cart.delete_one({'_id': cart_item['_id']})
        return jsonify({'success': True, 'message': 'Item removed from cart'})



@app.route('/cart/set/<product_id>', methods=['POST'])
@login_required
def set_cart_quantity(product_id):
    """Set cart quantity by product (MongoDB, AJAX friendly)"""
    data = request.get_json() or {}
    quantity = data.get('quantity', 1)
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    cart_item = mongo.db.cart.find_one({'user_id': str(current_user.id), 'product_id': product_id})
    if quantity <= 0:
        if cart_item:
            mongo.db.cart.delete_one({'_id': cart_item['_id']})
        cart_count = sum(item.get('quantity', 1) for item in mongo.db.cart.find({'user_id': str(current_user.id)}))
        return jsonify({'success': True, 'quantity': 0, 'cart_count': cart_count, 'message': 'Item removed'})
    if cart_item:
        mongo.db.cart.update_one({'_id': cart_item['_id']}, {'$set': {'quantity': quantity}})
    else:
        mongo.db.cart.insert_one({'user_id': str(current_user.id), 'product_id': product_id, 'quantity': quantity})
    cart_item = mongo.db.cart.find_one({'user_id': str(current_user.id), 'product_id': product_id})
    cart_count = sum(item.get('quantity', 1) for item in mongo.db.cart.find({'user_id': str(current_user.id)}))
    return jsonify({
        'success': True,
        'quantity': cart_item.get('quantity', 1),
        'cart_count': cart_count,
        'message': 'Cart updated'
    })



@app.route('/cart/remove/<cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    """Remove item from cart (MongoDB)"""
    from bson import ObjectId
    cart_item = mongo.db.cart.find_one({'_id': ObjectId(cart_id), 'user_id': str(current_user.id)})
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if cart_item:
        mongo.db.cart.delete_one({'_id': cart_item['_id']})
        if is_ajax:
            return jsonify({'success': True, 'message': 'Item removed from cart'})
        flash('Item removed from cart', 'success')
    else:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Cart item not found'}), 404
        flash('Cart item not found', 'warning')
    return redirect(url_for('cart'))


@app.route('/cart/remove/', methods=['POST'])
@login_required
def remove_from_cart_empty():
    flash('No cart item specified.', 'warning')
    return redirect(url_for('cart'))


# ==================== CHECKOUT ====================
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    from bson import ObjectId
    cart_items = list(mongo.db.cart.find({'user_id': str(current_user.id)}))
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('categories'))
    # Fetch product details for each cart item
    product_ids = [ObjectId(item['product_id']) for item in cart_items]
    products = {str(prod['_id']): prod for prod in mongo.db.products.find({'_id': {'$in': product_ids}})}
    for item in cart_items:
        item['product'] = products.get(item['product_id'])
    # Calculate total
    total = sum((item['product']['price'] if item['product'] else 0) * item.get('quantity', 1) for item in cart_items)
    form = CheckoutForm()
    # Pre-fill form with user data
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        from datetime import datetime
        from bson import ObjectId
        # Create order document
        order_doc = {
            'user_id': str(current_user.id),
            'total_amount': total,
            'shipping_name': form.name.data,
            'shipping_email': form.email.data,
            'shipping_address': form.address.data,
            'shipping_city': form.city.data,
            'shipping_postal_code': form.postal_code.data,
            'shipping_country': form.country.data,
            'status': 'pending',
            'created_at': datetime.utcnow(),
            'items': []
        }
        # Add order items
        for cart_item in cart_items:
            order_doc['items'].append({
                'product_id': cart_item['product_id'] if isinstance(cart_item, dict) else str(cart_item.product_id),
                'quantity': cart_item['quantity'] if isinstance(cart_item, dict) else cart_item.quantity,
                'price': cart_item['product']['price'] if isinstance(cart_item, dict) and 'product' in cart_item else (cart_item.product.price if hasattr(cart_item, 'product') else 0),
                'unit': cart_item['product']['unit'] if isinstance(cart_item, dict) and 'product' in cart_item and 'unit' in cart_item['product'] else (cart_item.product.unit if hasattr(cart_item, 'product') and hasattr(cart_item.product, 'unit') else 'kg')
            })
        # Insert order
        result = mongo.db.orders.insert_one(order_doc)
        order_id = str(result.inserted_id)
        # Clear cart
        mongo.db.cart.delete_many({'user_id': str(current_user.id)})
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_success', order_id=order_id))
    
    return render_template('checkout.html', form=form, cart_items=cart_items, total=total)



@app.route('/success/<order_id>')
@login_required
def order_success(order_id):
    """Order confirmation page (MongoDB)"""
    from bson import ObjectId
    order = mongo.db.orders.find_one({'_id': ObjectId(order_id), 'user_id': str(current_user.id)})
    if not order:
        return abort(404)
    return render_template('success.html', order=order)


# ==================== USER ACCOUNT ====================

@app.route('/account')
@login_required
def account():
    """User account page with orders (MongoDB)"""
    orders = list(mongo.db.orders.find({'user_id': str(current_user.id)}).sort('created_at', -1))
    return render_template('account.html', orders=orders)



@app.route('/order/<order_id>')
@login_required
def order_detail(order_id):
    """View detailed order information (MongoDB)"""
    from bson import ObjectId
    order = mongo.db.orders.find_one({'_id': ObjectId(order_id), 'user_id': str(current_user.id)})
    if not order:
        return abort(404)
    return render_template('order_detail.html', order=order)

@app.route('/order/<order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel an order if it's still pending or processing (MongoDB)"""
    from bson import ObjectId
    order = mongo.db.orders.find_one({'_id': ObjectId(order_id), 'user_id': str(current_user.id)})
    if not order:
        return abort(404)
    if order.get('status', '').lower() not in ['pending', 'processing']:
        flash('This order can no longer be cancelled.', 'warning')
        return redirect(request.referrer or url_for('account'))
    mongo.db.orders.update_one({'_id': order['_id']}, {'$set': {'status': 'cancelled'}})
    flash('Your order has been cancelled.', 'success')
    return redirect(request.referrer or url_for('account'))


# ==================== ADMIN PANEL ====================
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with stats (MongoDB)"""
    total_products = mongo.db.products.count_documents({})
    total_categories = mongo.db.categories.count_documents({})
    total_orders = mongo.db.orders.count_documents({})
    total_users = mongo.db.users.count_documents({'is_admin': False})
    
    # Get category-wise product counts
    category_stats = mongo.db.categories.aggregate([
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "category_id",
                "as": "products"
            }
        },
        {
            "$project": {
                "name": "$name",
                "product_count": {"$size": "$products"}
            }
        }
    ])
    
    # Recent products
    recent_products = list(mongo.db.products.find().sort("created_at", -1).limit(10))
    # Attach category_name and id to each product
    all_categories = list(mongo.db.categories.find())
    category_map = {str(cat['_id']): cat['name'] for cat in all_categories}
    for prod in recent_products:
        cat_id = str(prod.get('category_id'))
        prod['category_name'] = category_map.get(cat_id, '')
        prod['id'] = str(prod['_id'])
    
    # Get all registered users (excluding admins) with their order counts
    users = list(mongo.db.users.aggregate([
        {
            "$match": {"is_admin": False}
        },
        {
            "$lookup": {
                "from": "orders",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "orders"
            }
        },
        {
            "$project": {
                "user": "$$ROOT",
                "order_count": {"$size": "$orders"}
            }
        }
    ]))
    
    return render_template('admin_dashboard.html',
                           total_products=total_products,
                           total_categories=total_categories,
                           total_orders=total_orders,
                           total_users=total_users,
                           category_stats=category_stats,
                           recent_products=recent_products,
                           users=users,
                           hide_shopping_nav=True)


@app.route('/admin/products')
@admin_required
def admin_products():
    """List all products for admin management"""
    products = list(mongo.db.products.find().sort('created_at', -1))
    return render_template('admin_products.html', products=products, hide_shopping_nav=True)


@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    form = ProductForm()
    # Populate category choices from MongoDB
    categories = list(mongo.db.categories.find().sort('name', 1))
    form.category_id.choices = [(str(c['_id']), c['name']) for c in categories]
    if form.validate_on_submit():
        from bson import ObjectId
        # Handle image source type
        image_filename = None
        image_url = None
        if form.image_source.data == 'file':
            if not form.image.data:
                flash('Please enter image filename', 'danger')
                return render_template('admin_add_product.html', form=form, hide_shopping_nav=True)
            image_filename = form.image.data
        else:  # url
            if not form.image_url.data:
                flash('Please enter image URL', 'danger')
                return render_template('admin_add_product.html', form=form, hide_shopping_nav=True)
            image_url = form.image_url.data
        category_id = ObjectId(form.category_id.data)
        product_doc = {
            'name': form.name.data,
            'description': form.description.data,
            'price': form.price.data,
            'stock': form.stock.data,
            'category_id': category_id,
            'image': image_filename,
            'image_url': image_url
        }
        mongo.db.products.insert_one(product_doc)
        flash(f'Product "{form.name.data}" added successfully!', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_add_product.html', form=form, hide_shopping_nav=True)


@app.route('/admin/product/<product_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit existing product"""
    from bson import ObjectId
    from bson import ObjectId
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        abort(404)
    # Pre-populate form with product data
    form = ProductForm(data={
        'name': product.get('name'),
        'description': product.get('description'),
        'price': product.get('price'),
        'stock': product.get('stock'),
        'category_id': str(product.get('category_id')),
        'image': product.get('image'),
        'image_url': product.get('image_url'),
    })
    # Populate category choices from MongoDB
    categories = list(mongo.db.categories.find().sort('name', 1))
    form.category_id.choices = [(str(c['_id']), c['name']) for c in categories]
    if form.validate_on_submit():
        update_doc = {
            'name': form.name.data,
            'description': form.description.data,
            'price': form.price.data,
            'stock': form.stock.data,
            'category_id': ObjectId(form.category_id.data)
        }
        # Handle image source type
        if form.image_source.data == 'file':
            if not form.image.data:
                flash('Please enter image filename', 'danger')
                return render_template('admin_edit_product.html', form=form, product=product, hide_shopping_nav=True)
            update_doc['image'] = form.image.data
            update_doc['image_url'] = None
        else:
            if not form.image_url.data:
                flash('Please enter image URL', 'danger')
                return render_template('admin_edit_product.html', form=form, product=product, hide_shopping_nav=True)
            update_doc['image'] = None
            update_doc['image_url'] = form.image_url.data
        mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': update_doc})
        flash(f'Product "{form.name.data}" updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_edit_product.html', form=form, product=product, hide_shopping_nav=True)


@app.route('/admin/product/<product_id>/delete', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete a product"""
    from bson import ObjectId
    from bson import ObjectId
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        abort(404)
    product_name = product.get('name')
    mongo.db.products.delete_one({'_id': ObjectId(product_id)})
    flash(f'Product "{product_name}" deleted successfully!', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/categories')
@admin_required
def admin_categories():
    """List all categories with product counts"""
    # Get all categories and count products in each (MongoDB)
    categories = list(mongo.db.categories.find())
    for cat in categories:
        cat['product_count'] = mongo.db.products.count_documents({'category_id': cat['_id']})
    return render_template('admin_categories.html', category_stats=categories, hide_shopping_nav=True)


@app.route('/admin/user/<user_id>/orders')
@admin_required
def admin_user_orders(user_id):
    """View a specific user's order history"""
    from bson import ObjectId
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(404)
    orders = list(mongo.db.orders.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))
    return render_template('admin_user_orders.html', user=user, orders=orders, hide_shopping_nav=True)

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    # No db.session to rollback with MongoDB
    return render_template('500.html'), 500


# ==================== CONTEXT PROCESSOR ====================
@app.context_processor

def inject_cart_count():
    """Inject cart item count and categories into all templates (MongoDB)"""
    all_categories = list(mongo.db.categories.find())
    cart_count = 0
    wishlist_count = 0
    if current_user.is_authenticated:
        cart_items = list(mongo.db.cart.find({'user_id': str(current_user.id)}))
        cart_count = sum(item.get('quantity', 1) for item in cart_items)
        wishlist_count = mongo.db.wishlist.count_documents({'user_id': str(current_user.id)})
    return dict(cart_count=cart_count, wishlist_count=wishlist_count, all_categories=all_categories, hide_shopping_nav=False)


if __name__ == '__main__':
    import os
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host='0.0.0.0', port=port)

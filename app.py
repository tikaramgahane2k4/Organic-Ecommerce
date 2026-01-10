from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Category, Product, Wishlist, Cart, Order, OrderItem
from forms import RegistrationForm, LoginForm, CheckoutForm
from sqlalchemy import func

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
# Override with instance config if it exists
try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    pass

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# ==================== DATA SEED (SAFETY) ====================
def seed_if_empty():
    """Populate baseline categories/products if the database is empty."""
    if Product.query.count() > 0:
        return

    categories = [
        {'name': 'Fresh Vegetables', 'description': 'Farm-fresh organic vegetables delivered daily', 'image': 'category-vegetables.png'},
        {'name': 'Organic Fruits', 'description': 'Sweet and juicy organic fruits', 'image': 'category-fruits.png'},
        {'name': 'Grains & Cereals', 'description': 'Whole grains and organic cereals', 'image': 'oats.png'},
        {'name': 'Dairy Products', 'description': 'Fresh organic dairy from local farms', 'image': 'category-dairy.png'},
        {'name': 'Herbs & Spices', 'description': 'Aromatic organic herbs and spices', 'image': 'herbs.jpg'},
        {'name': 'Organic Honey', 'description': 'Pure natural honey from organic farms', 'image': 'honey.png'},
    ]

    products = [
        # Vegetables
        {'name': 'Organic Tomatoes', 'description': 'Fresh, vine-ripened organic tomatoes. Perfect for salads and cooking. Rich in vitamins and antioxidants.', 'price': 399, 'stock': 50, 'category': 'Fresh Vegetables', 'image': 'tomatoes.jpg'},
        {'name': 'Organic Spinach', 'description': 'Tender organic spinach leaves, packed with iron and nutrients. Great for smoothies and salads.', 'price': 279, 'stock': 30, 'category': 'Fresh Vegetables', 'image': 'spinach.png'},
        {'name': 'Organic Carrots', 'description': 'Sweet and crunchy organic carrots. High in beta-carotene and fiber.', 'price': 239, 'stock': 60, 'category': 'Fresh Vegetables', 'image': 'carrot.png'},
        {'name': 'Organic Broccoli', 'description': 'Fresh organic broccoli crowns. Excellent source of vitamins C and K.', 'price': 319, 'stock': 40, 'category': 'Fresh Vegetables', 'image': 'broccoli.jpg'},
        # Fruits
        {'name': 'Organic Apples', 'description': 'Crisp and sweet organic apples. Perfect for snacking or baking.', 'price': 479, 'stock': 80, 'category': 'Organic Fruits', 'image': 'red-apple.png'},
        {'name': 'Organic Bananas', 'description': 'Naturally ripened organic bananas. Great source of potassium.', 'price': 319, 'stock': 100, 'category': 'Organic Fruits', 'image': 'banana.png'},
        {'name': 'Organic Strawberries', 'description': 'Sweet and juicy organic strawberries. Rich in vitamin C and antioxidants.', 'price': 559, 'stock': 35, 'category': 'Organic Fruits', 'image': 'strawberries.jpg'},
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

    name_to_id = {}
    for cat in categories:
        existing = Category.query.filter_by(name=cat['name']).first()
        if not existing:
            existing = Category(name=cat['name'], description=cat['description'], image=cat['image'])
            db.session.add(existing)
            db.session.flush()
        name_to_id[existing.name] = existing.id

    for prod in products:
        if Product.query.filter_by(name=prod['name']).first():
            continue
        cat_id = name_to_id.get(prod['category'])
        if not cat_id:
            continue
        item = Product(
            name=prod['name'],
            description=prod['description'],
            price=prod['price'],
            stock=prod['stock'],
            category_id=cat_id,
            image=prod['image']
        )
        db.session.add(item)

    db.session.commit()


# ==================== HOME PAGE ====================
@app.route('/')
def index():
    """Home page with featured products and categories"""
    categories = Category.query.limit(4).all()
    featured_products = Product.query.limit(8).all()
    return render_template('index.html', categories=categories, products=featured_products)


# ==================== CATEGORIES ====================
@app.route('/categories')
def categories():
    """Display all categories with products"""
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', '')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    
    all_categories = Category.query.all()
    
    # Build query
    query = Product.query
    
    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)
        current_category = Category.query.get(category_id)
    else:
        current_category = None
    
    # Apply search filter
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            db.or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern)
            )
        )
    
    # Apply price range filters
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    
    # Apply price sorting
    if sort_by == 'high_to_low':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'low_to_high':
        query = query.order_by(Product.price.asc())
    
    products = query.all()

    # Prefill cart quantities for inline controls
    cart_quantities = {}
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        cart_quantities = {item.product_id: item.quantity for item in cart_items}
    
    return render_template('categories.html', 
                         categories=all_categories, 
                         products=products, 
                         current_category=current_category,
                         search_query=search_query,
                         cart_quantities=cart_quantities)


# ==================== SHOP / PRODUCTS ====================
@app.route('/shop')
def shop():
    """Display all products with optional category filter"""
    category_id = request.args.get('category', type=int)
    
    if category_id:
        products = Product.query.filter_by(category_id=category_id).all()
        current_category = Category.query.get(category_id)
    else:
        products = Product.query.all()
        current_category = None
    
    categories = Category.query.all()

    # Prefill cart quantities similar to categories page
    cart_quantities = {}
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        cart_quantities = {item.product_id: item.quantity for item in cart_items}

    return render_template('shop.html', products=products, categories=categories, 
                         current_category=current_category, cart_quantities=cart_quantities)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Display product details"""
    product = Product.query.get_or_404(product_id)
    
    # Check if product is in wishlist (for logged-in users)
    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first() is not None
    
    # Get related products from the same category
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product_id
    ).limit(4).all()
    
    return render_template('product.html', product=product, 
                         in_wishlist=in_wishlist, 
                         related_products=related_products)


# ==================== AUTHENTICATION ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login with your credentials.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ==================== WISHLIST ====================
@app.route('/wishlist')
@login_required
def wishlist():
    """Display user's wishlist"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)


@app.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """Add product to wishlist"""
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id
    ).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()
        return jsonify({
            'success': True, 
            'message': 'Removed from wishlist',
            'wishlist_count': wishlist_count,
            'action': 'removed'
        })
    
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()
    
    wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()
    return jsonify({
        'success': True, 
        'message': 'Added to wishlist',
        'wishlist_count': wishlist_count,
        'action': 'added'
    })


@app.route('/wishlist/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    """Remove product from wishlist"""
    wishlist_item = Wishlist.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id
    ).first_or_404()
    
    db.session.delete(wishlist_item)
    db.session.commit()
    
    flash('Product removed from wishlist', 'success')
    return redirect(url_for('wishlist'))


# ==================== CART ====================
@app.route('/cart')
@login_required
def cart():
    """Display shopping cart"""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart"""
    product = Product.query.get_or_404(product_id)
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
    cart_item = Cart.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id
    ).first()
    
    if cart_item:
        # Update quantity
        cart_item.quantity += quantity
    else:
        # Add new item
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()

    if is_ajax:
        cart_count = db.session.query(func.coalesce(func.sum(Cart.quantity), 0))\
            .filter(Cart.user_id == current_user.id).scalar() or 0
        return jsonify({
            'success': True,
            'message': 'Product added to cart',
            'quantity': cart_item.quantity,
            'cart_count': cart_count
        })

    if request.form.get('next') == 'checkout':
        return redirect(url_for('checkout'))
    
    # Check if redirect_to parameter is set to cart
    if request.form.get('redirect_to') == 'cart':
        flash('Product added to cart', 'success')
        return redirect(url_for('cart'))
        
    flash('Product added to cart', 'success')
    return redirect(request.referrer or url_for('categories'))


@app.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    """Update cart item quantity"""
    cart_item = Cart.query.filter_by(
        id=cart_id, 
        user_id=current_user.id
    ).first_or_404()
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cart updated'})
    else:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item removed from cart'})


@app.route('/cart/set/<int:product_id>', methods=['POST'])
@login_required
def set_cart_quantity(product_id):
    """Set cart quantity by product (AJAX friendly)"""
    data = request.get_json() or {}
    quantity = data.get('quantity', 1)

    # Guard against invalid quantity
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if quantity <= 0:
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
        cart_count = db.session.query(func.coalesce(func.sum(Cart.quantity), 0))\
            .filter(Cart.user_id == current_user.id).scalar() or 0
        return jsonify({'success': True, 'quantity': 0, 'cart_count': cart_count, 'message': 'Item removed'})

    if cart_item:
        cart_item.quantity = quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()

    cart_count = db.session.query(func.coalesce(func.sum(Cart.quantity), 0))\
        .filter(Cart.user_id == current_user.id).scalar() or 0

    return jsonify({
        'success': True,
        'quantity': cart_item.quantity,
        'cart_count': cart_count,
        'message': 'Cart updated'
    })


@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    """Remove item from cart"""
    cart_item = Cart.query.filter_by(
        id=cart_id, 
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))


# ==================== CHECKOUT ====================
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('categories'))
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    form = CheckoutForm()
    
    # Pre-fill form with user data
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_name=form.name.data,
            shipping_email=form.email.data,
            shipping_address=form.address.data,
            shipping_city=form.city.data,
            shipping_postal_code=form.postal_code.data,
            shipping_country=form.country.data
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        # Clear cart
        Cart.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_success', order_id=order.id))
    
    return render_template('checkout.html', form=form, cart_items=cart_items, total=total)


@app.route('/success/<int:order_id>')
@login_required
def order_success(order_id):
    """Order confirmation page"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('success.html', order=order)


# ==================== USER ACCOUNT ====================
@app.route('/account')
@login_required
def account():
    """User account page with orders"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('account.html', orders=orders)


@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """View detailed order information"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_detail.html', order=order)

@app.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel an order if it's still pending or processing"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()

    if order.status.lower() not in ['pending', 'processing']:
        flash('This order can no longer be cancelled.', 'warning')
        return redirect(request.referrer or url_for('account'))

    order.status = 'cancelled'
    db.session.commit()
    flash('Your order has been cancelled.', 'success')
    return redirect(request.referrer or url_for('account'))

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== CONTEXT PROCESSOR ====================
@app.context_processor
def inject_cart_count():
    """Inject cart item count and categories into all templates"""
    all_categories = Category.query.all()
    cart_count = 0
    wishlist_count = 0
    if current_user.is_authenticated:
        cart_count = db.session.query(func.sum(Cart.quantity)).filter_by(user_id=current_user.id).scalar() or 0
        wishlist_count = db.session.query(func.count(Wishlist.id)).filter_by(user_id=current_user.id).scalar() or 0
    return dict(cart_count=cart_count, wishlist_count=wishlist_count, all_categories=all_categories)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_if_empty()
    app.run(debug=True)

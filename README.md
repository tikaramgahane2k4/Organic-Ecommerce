# Green Harvest - Organic E-Commerce Platform

A fully functional multi-page organic e-commerce website built with Flask, PostgreSQL, and vanilla JavaScript.

## 🌿 Features

- **User Authentication**: Secure registration and login system with password hashing
- **Product Management**: Browse products by category with detailed product pages
- **Shopping Cart**: Add, update, and remove items from cart
- **Wishlist**: Save favorite products for later
- **Checkout System**: Complete order placement with shipping information
- **Order Management**: View order history and details
- **User Account**: Manage profile and view past orders
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Tech Stack

- **Backend**: Python (Flask framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Icons**: Font Awesome

## 📋 Requirements

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure PostgreSQL Database

Make sure PostgreSQL is installed and running. Create a database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE green_harvest;

# Exit PostgreSQL
\q
```

### 3. Update Database Configuration

Edit `config.py` if needed to match your PostgreSQL credentials:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/green_harvest'
```

Replace `postgres:postgres` with your PostgreSQL username and password.

### 4. Initialize Database

Run the initialization script to create tables and populate with sample data:

```bash
python init_db.py
```

This will create:
- Database tables
- Sample categories (Vegetables, Fruits, Grains, Dairy, Herbs, Honey)
- Sample products (~17 products)
- Test user accounts

### 5. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 👤 Test Accounts

After running `init_db.py`, you can login with these accounts:

**User Account 1:**
- Email: `john@example.com`
- Password: `password123`

**User Account 2:**
- Email: `jane@example.com`
- Password: `password123`

**Admin Account:**
- Email: `admin@greenharvest.com`
- Password: `admin123`

## 📁 Project Structure

```
/green_harvest
│
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # WTForms for user input
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
│
├── /templates            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── categories.html   # Categories listing
│   ├── shop.html         # Products listing
│   ├── product.html      # Product details
│   ├── wishlist.html     # User wishlist
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout page
│   ├── success.html      # Order confirmation
│   ├── account.html      # User account
│   ├── login.html        # Login page
│   └── register.html     # Registration page
│
├── /static
│   ├── /css
│   │   └── style.css     # Main stylesheet
│   ├── /js
│   │   └── main.js       # JavaScript functionality
│   └── /images           # Product and category images
│
└── /instance             # Instance folder (created automatically)
    └── (database files)
```

## 🎯 Key Routes

- `/` - Home page with featured products
- `/categories` - Browse all categories
- `/shop` - View all products (with category filter)
- `/product/<id>` - Product detail page
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/wishlist` - User's wishlist
- `/cart` - Shopping cart
- `/checkout` - Checkout page
- `/success/<order_id>` - Order confirmation
- `/account` - User account and order history

## 🔐 Security Features

- Password hashing using Werkzeug
- CSRF protection on all forms
- Login required decorators for protected routes
- Secure session management
- SQL injection prevention through SQLAlchemy ORM

## 📱 Responsive Design

The website is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🎨 Color Scheme

- Primary: #4CAF50 (Green)
- Secondary: #8BC34A (Light Green)
- Accent: #FF9800 (Orange)
- Text: #333333 (Dark Gray)

## 🔄 Database Models

- **User**: User authentication and profile
- **Category**: Product categories
- **Product**: Product information
- **Wishlist**: User's saved products
- **Cart**: Shopping cart items
- **Order**: Customer orders
- **OrderItem**: Individual items in orders

## 📝 Environment Variables

For production, set these environment variables:

```bash
export SECRET_KEY='your-secret-key-here'
export DATABASE_URL='postgresql://user:pass@localhost/dbname'
```

## 🚨 Troubleshooting

### Database Connection Error

If you get a database connection error:
1. Make sure PostgreSQL is running
2. Verify database credentials in `config.py`
3. Check if the database exists: `psql -U postgres -l`

### Port Already in Use

If port 5000 is already in use, modify `app.py`:

```python
app.run(debug=True, port=5001)
```

### Module Import Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## 🎓 For Learning/Portfolio

This project demonstrates:
- Full-stack web development
- RESTful API design
- Database design and relationships
- User authentication and authorization
- Form validation and security
- Responsive web design
- Modern JavaScript (ES6+)

## 📄 License

This project is created for educational and portfolio purposes.

## 👨‍💻 Developer

Created as a portfolio project demonstrating full-stack development skills with Flask and PostgreSQL.

## 🔮 Future Enhancements

- Product search functionality
- Product reviews and ratings
- Admin dashboard for product management
- Payment gateway integration
- Email notifications
- Order tracking
- Product image upload
- Advanced filtering and sorting
- Password reset functionality
- Social media authentication

## 📞 Support

For issues or questions, please check the code comments or modify the configuration as needed.

---

**Happy Shopping! 🌱**

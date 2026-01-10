"""
Database Initialization Script
This script creates the database tables and populates them with sample data
"""

from app import app, db
from models import User, Category, Product
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and sample data"""
    
    with app.app_context():
        # Drop all tables and recreate (for development only)
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        print("✓ Tables created successfully!")
        
        # Create sample users
        print("\nCreating sample users...")
        users = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'password': 'password123'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'password': 'password123'
            },
            {
                'name': 'Admin User',
                'email': 'admin@greenharvest.com',
                'password': 'admin123'
            }
        ]
        
        for user_data in users:
            user = User(
                name=user_data['name'],
                email=user_data['email']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"  ✓ Created user: {user_data['email']}")
        
        db.session.commit()
        
        # Create categories
        print("\nCreating categories...")
        categories = [
            {
                'name': 'Fresh Vegetables',
                'description': 'Farm-fresh organic vegetables delivered daily',
                'image': 'category-vegetables.png'
            },
            {
                'name': 'Organic Fruits',
                'description': 'Sweet and juicy organic fruits',
                'image': 'category-fruits.png'
            },
            {
                'name': 'Grains & Cereals',
                'description': 'Whole grains and organic cereals',
                'image': 'oats.png'
            },
            {
                'name': 'Dairy Products',
                'description': 'Fresh organic dairy from local farms',
                'image': 'category-dairy.png'
            },
            {
                'name': 'Herbs & Spices',
                'description': 'Aromatic organic herbs and spices',
                'image': 'herbs.jpg'
            },
            {
                'name': 'Organic Honey',
                'description': 'Pure natural honey from organic farms',
                'image': 'honey.png'
            }
        ]
        
        category_objects = []
        for cat_data in categories:
            category = Category(
                name=cat_data['name'],
                description=cat_data['description'],
                image=cat_data['image']
            )
            db.session.add(category)
            category_objects.append(category)
            print(f"  ✓ Created category: {cat_data['name']}")
        
        db.session.commit()
        
        # Create products
        print("\nCreating products...")
        products = [
            # Vegetables
            {
                'name': 'Organic Tomatoes',
                'description': 'Fresh, vine-ripened organic tomatoes. Perfect for salads and cooking. Rich in vitamins and antioxidants.',
                'price': 399,
                'stock': 50,
                'category': 'Fresh Vegetables',
                'image': 'tomatoes.jpg'
            },
            {
                'name': 'Organic Spinach',
                'description': 'Tender organic spinach leaves, packed with iron and nutrients. Great for smoothies and salads.',
                'price': 279,
                'stock': 30,
                'category': 'Fresh Vegetables',
                'image': 'spinach.png'
            },
            {
                'name': 'Organic Carrots',
                'description': 'Sweet and crunchy organic carrots. High in beta-carotene and fiber.',
                'price': 239,
                'stock': 60,
                'category': 'Fresh Vegetables',
                'image': 'carrot.png'
            },
            {
                'name': 'Organic Broccoli',
                'description': 'Fresh organic broccoli crowns. Excellent source of vitamins C and K.',
                'price': 319,
                'stock': 40,
                'category': 'Fresh Vegetables',
                'image': 'broccoli.jpg'
            },
            
            # Fruits
            {
                'name': 'Organic Apples',
                'description': 'Crisp and sweet organic apples. Perfect for snacking or baking.',
                'price': 479,
                'stock': 80,
                'category': 'Organic Fruits',
                'image': 'red-apple.png'
            },
            {
                'name': 'Organic Bananas',
                'description': 'Naturally ripened organic bananas. Great source of potassium.',
                'price': 319,
                'stock': 100,
                'category': 'Organic Fruits',
                'image': 'banana.png'
            },
            {
                'name': 'Organic Strawberries',
                'description': 'Sweet and juicy organic strawberries. Rich in vitamin C and antioxidants.',
                'price': 559,
                'stock': 35,
                'category': 'Organic Fruits',
                'image': 'strawberries.jpg'
            },
            {
                'name': 'Organic Oranges',
                'description': 'Fresh and tangy organic oranges. Perfect for juice or eating fresh.',
                'price': 399,
                'stock': 70,
                'category': 'Organic Fruits',
                'image': 'orange.png'
            },
            {
                'name': 'Fresh Avocado',
                'description': 'Creamy organic avocados. Perfect for toast, salads, and guacamole.',
                'price': 599,
                'stock': 45,
                'category': 'Organic Fruits',
                'image': 'avocado.png'
            },
            {
                'name': 'Fresh Guava',
                'description': 'Sweet and fragrant organic guavas. Rich in vitamin C and fiber.',
                'price': 359,
                'stock': 55,
                'category': 'Organic Fruits',
                'image': 'gwava.png'
            },
            
            # Grains
            {
                'name': 'Organic Brown Rice',
                'description': 'Premium quality organic brown rice. High in fiber and nutrients.',
                'price': 719,
                'stock': 100,
                'category': 'Grains & Cereals',
                'image': 'brown-rice.jpg'
            },
            {
                'name': 'Organic Quinoa',
                'description': 'Protein-rich organic quinoa. Perfect for healthy meals.',
                'price': 1039,
                'stock': 50,
                'category': 'Grains & Cereals',
                'image': 'quinoa.jpg'
            },
            {
                'name': 'Organic Oats',
                'description': 'Whole grain organic oats. Perfect for breakfast and baking.',
                'price': 559,
                'stock': 80,
                'category': 'Grains & Cereals',
                'image': 'oats.png'
            },
            
            # Dairy
            {
                'name': 'Organic Milk',
                'description': 'Fresh organic milk from grass-fed cows. Rich and creamy.',
                'price': 439,
                'stock': 45,
                'category': 'Dairy Products',
                'image': 'milk.png'
            },
            {
                'name': 'Organic Cheese',
                'description': 'Artisan organic cheese. Made from organic milk with no additives.',
                'price': 799,
                'stock': 30,
                'category': 'Dairy Products',
                'image': 'cheese.jpg'
            },
            {
                'name': 'Organic Yogurt',
                'description': 'Creamy organic yogurt with live cultures. Great for digestion.',
                'price': 359,
                'stock': 60,
                'category': 'Dairy Products',
                'image': 'yogurt.jpg'
            },
            {
                'name': 'Farm Fresh Eggs',
                'description': 'Organic free-range eggs. Rich in protein and omega-3.',
                'price': 529,
                'stock': 65,
                'category': 'Dairy Products',
                'image': 'eggs.png'
            },
            
            # Herbs & Spices
            {
                'name': 'Organic Basil',
                'description': 'Fresh organic basil leaves. Perfect for Italian dishes.',
                'price': 239,
                'stock': 40,
                'category': 'Herbs & Spices',
                'image': 'basil.jpg'
            },
            {
                'name': 'Organic Turmeric',
                'description': 'Premium organic turmeric powder. Known for anti-inflammatory properties.',
                'price': 639,
                'stock': 50,
                'category': 'Herbs & Spices',
                'image': 'turmeric.jpg'
            },
            {
                'name': 'Extra Virgin Olive Oil',
                'description': 'Cold-pressed organic olive oil. Perfect for cooking and salads.',
                'price': 1299,
                'stock': 40,
                'category': 'Herbs & Spices',
                'image': 'olive oil.png'
            },
            
            # Honey
            {
                'name': 'Raw Organic Honey',
                'description': 'Pure, unfiltered organic honey. Natural sweetener with health benefits.',
                'price': 1199,
                'stock': 35,
                'category': 'Organic Honey',
                'image': 'honey.png'
            }
        ]
        
        for prod_data in products:
            # Find the category
            category = Category.query.filter_by(name=prod_data['category']).first()
            
            if category:
                product = Product(
                    name=prod_data['name'],
                    description=prod_data['description'],
                    price=prod_data['price'],
                    stock=prod_data['stock'],
                    category_id=category.id,
                    image=prod_data['image']
                )
                db.session.add(product)
                print(f"  ✓ Created product: {prod_data['name']}")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database initialization completed successfully!")
        print("="*50)
        print("\nSample Login Credentials:")
        print("-" * 30)
        for user in users:
            print(f"Email: {user['email']}")
            print(f"Password: {user['password']}")
            print("-" * 30)
        print("\nYou can now run the application with: python app.py")
        print("Then visit: http://localhost:5000")


if __name__ == '__main__':
    init_database()

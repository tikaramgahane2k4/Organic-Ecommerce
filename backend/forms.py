from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange


class RegistrationForm(FlaskForm):
    """User registration form"""
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        """Check if email already exists (MongoDB)"""
        try:
            from backend.app import mongo
        except ImportError:
            mongo = None
        user = mongo.db.users.find_one({'email': email.data}) if mongo else None
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    submit = SubmitField('Login')


class CheckoutForm(FlaskForm):
    """Checkout form for order placement"""
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    address = TextAreaField('Address', validators=[
        DataRequired(message='Address is required'),
        Length(min=10, max=500, message='Address must be between 10 and 500 characters')
    ])
    city = StringField('City', validators=[
        DataRequired(message='City is required'),
        Length(min=2, max=100)
    ])
    postal_code = StringField('Postal Code', validators=[
        DataRequired(message='Postal code is required'),
        Length(min=3, max=20)
    ])
    country = StringField('Country', validators=[
        DataRequired(message='Country is required'),
        Length(min=2, max=100)
    ])
    submit = SubmitField('Place Order')


class ProductForm(FlaskForm):
    """Form for adding/editing products"""
    name = StringField('Product Name', validators=[
        DataRequired(message='Product name is required'),
        Length(min=2, max=200, message='Product name must be between 2 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
    ])
    price = FloatField('Price (₹)', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
    stock = IntegerField('Stock Quantity', validators=[
        DataRequired(message='Stock quantity is required'),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    category_id = SelectField('Category', coerce=str, validators=[
        DataRequired(message='Please select a category')
    ])
    image_source = RadioField('Image Source', choices=[('file', 'Upload Local File'), ('url', 'Use Image Link')], default='file')
    image = StringField('Image Filename', validators=[
        Length(max=255, message='Filename must be less than 255 characters')
    ])
    image_url = StringField('Image URL', validators=[
        Length(max=500, message='URL must be less than 500 characters')
    ])
    submit = SubmitField('Add Product')


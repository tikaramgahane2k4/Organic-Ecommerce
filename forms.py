from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from models import User

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
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
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

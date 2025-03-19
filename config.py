from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, 
                    FloatField, IntegerField, SelectField, TextAreaField,
                    FileField)
from wtforms.validators import (DataRequired, Length, Email, 
                               EqualTo, ValidationError)
from models import User, Category
from flask_uploads import UploadSet, IMAGES
photos = UploadSet('photos', IMAGES)

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
        validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    JWT_SECRET_KEY = 'test-jwt-secret'

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock Quantity', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    image = FileField('Product Image')
    submit = SubmitField('Save Product')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) 
                               for c in Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('Category Name', 
        validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    submit = SubmitField('Create Category')

class OrderForm(FlaskForm):
    status = SelectField('Order Status',
        choices=[('pending', 'Pending'), 
                ('processing', 'Processing'),
                ('completed', 'Completed'),
                ('cancelled', 'Cancelled')])
    submit = SubmitField('Update Status')
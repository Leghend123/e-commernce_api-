from datetime import datetime
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    profile = db.Column(
        db.String(120), unique=False, nullable=False, default="profile.jpg"
    )
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self) -> str:
        return "User>>>{self.username}"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=False, nullable=False)
    lastname = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    contact = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    registration_date = db.Column(db.DateTime(), default=datetime.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return "Customer>>>{self.username}"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now())

    products = db.relationship("Product", backref="category", lazy=True)

    def __repo__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(110), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now())
    
    
    def __repo__(self):
        return f"<Product {self.name}, Price: {self.price}>"

from datetime import datetime,timedelta
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON


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
    category_name = db.Column(
        db.Integer, db.ForeignKey("categories.name"), nullable=False
    )
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now())

    def __repo__(self):
        return f"<Product {self.name}, Price: {self.price}>"


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    cart_data = db.Column(JSON, nullable=False, default={})
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    expires_at = db.Column(db.DateTime, nullable=True)

    customer = db.relationship("Customer", backref="carts")

    def __repr__(self):
        return f"<Cart id={self.id} customer_id={self.customer_id}>"

    def save_cart_data(self, cart_items, expire_in_days=3):
        self.cart_data = cart_items
        self.total_price = sum(
            (item.get("price", 0) or 0) * (item.get("quantity", 0) or 0)
            for item in cart_items
        )
        self.expires_at =  datetime.now() + timedelta(days=expire_in_days)
        db.session.commit()

    def load_cart_data(self):
        return self.cart_data
    


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    customer = db.relationship("Customer", backref="cart_items")
    products = db.relationship("Product", backref="cart_items")

    def __repr__(self):
        return f"<CratItems customer_id {self.customer_id} product_id {self.product_id} quantity {self.quantity}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.Float, nullable=False)

    customer = db.relationship("Customer", backref="orders")
    order_items = db.relationship("OrderItem", backref="order", lazy=True)


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship("Product", backref="order_items")

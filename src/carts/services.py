from ..extensions import db
from src.constants.Http_status_code import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)
from flask import session
from ..model import Product, Customer, Cart
from flask_jwt_extended import get_jwt_identity


# cart services .....................
class CartServices:
    @staticmethod
    def add_to_guest_cart(data):
        try:
            product_id = data.get("product_id")
            quantity = data.get("quantity", 1)

            product = Product.query.filter_by(id=product_id).first()

            product_name = product.name
            price = product.price

            if not product_id or not product_name or not price:
                return {
                    "error": "Product ID, name, and price are required"
                }, HTTP_400_BAD_REQUEST

            cart = session.get("cart", [])

            product_found = False

            # Check if the product already exists in the cart
            for item in cart:
                if item["product_id"] == product_id:
                    item["quantity"] += quantity
                    product_found = True
                    break

            # If the product wasn't found, add it as a new entry
            if not product_found:
                cart.append(
                    {
                        "product_id": product_id,
                        "product_name": product_name,
                        "price": float(price),
                        "quantity": quantity,
                    }
                )

            # Save the updated cart back to the session
            session["cart"] = cart

            return {"msg": "Product added to guest cart successfully"}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def view_guest_cart():
        # Get the cart from the session, or initialize as an empty list if not available
        cart = session.get("cart", [])

        # print(f"Cart on view: {cart}")

        total_price = sum(
            item.get("price", 0) * item.get("quantity", 0) for item in cart
        )

        return {"cart": cart, "total_price": total_price}, HTTP_200_OK

    @staticmethod
    def view_guest_cart():
        # Get the cart from the session, or initialize as an empty list if not available
        cart = session.get("cart", [])

        # print(f"Cart on view: {cart}")

        total_price = sum(
            item.get("price", 0) * item.get("quantity", 0) for item in cart
        )

        return {"cart": cart, "total_price": total_price}, HTTP_200_OK

    @staticmethod
    def save_to_cart_db(customer_id):
        try:
            customer_id = get_jwt_identity()

            cart = session.get("cart", [])
            if not cart:
                return {"error": "session is empty"}, HTTP_400_BAD_REQUEST

            customer = Customer.query.filter_by(id=customer_id).first()
            if not customer:
                return {"error": "customer not found"}, HTTP_400_BAD_REQUEST

            total_price = sum(
                item.get("price", 0) * item.get("quantity", 0) for item in cart
            )

            existing_cart = Cart.query.filter_by(customer_id=customer_id).first()
            if existing_cart:
                existing_cart.save_cart_data(cart)
                existing_cart.total_price = total_price
            else:
                new_cart = Cart(
                    customer_id=customer_id, cart_data=cart, total_price=total_price
                )
                db.session.add(new_cart)
                db.session.commit()

            session.pop("cart", None)

            return {"msg": "Cart successfully saved to the database"}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    # load the saved cart from db...................
    def load_saved_cart(customer_id):
        try:
            customer_id = get_jwt_identity()

            cart = Cart.query.filter_by(customer_id=customer_id).first()
            if not cart:
                return {"error": "cart not found"}, HTTP_400_BAD_REQUEST

            session["cart"] = cart.load_cart_data()

            return {
                "cart": session["cart"],
                "total_price": cart.total_price,
            }, HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

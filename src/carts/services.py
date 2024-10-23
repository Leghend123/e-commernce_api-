from ..extensions import db
from src.constants.Http_status_code import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from flask import session
from ..model import Product, Customer, Cart, Order, OrderItem
from flask_jwt_extended import get_jwt_identity
from datetime import datetime


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

            # Get cart data from session
            session_cart = session.get("cart", [])
            if not session_cart:
                return {"error": "Session cart is empty"}, HTTP_400_BAD_REQUEST

            # Retrieve the customer and ensure they exist
            customer = Customer.query.filter_by(id=customer_id).first()
            if not customer:
                return {"error": "Customer not found"}, HTTP_404_NOT_FOUND

            # Check if the customer already has a saved cart
            existing_cart = Cart.query.filter_by(customer_id=customer_id).first()

            if existing_cart:
                # If the customer has a saved cart, merge it with the session cart
                saved_cart_data = existing_cart.load_cart_data()
                merged_cart = Cart_Utils.merge_carts(session_cart, saved_cart_data)
                existing_cart.save_cart_data(merged_cart)
            else:
                # If no saved cart exists, create a new cart for the customer
                new_cart = Cart(customer_id=customer_id, cart_data=session_cart)
                db.session.add(new_cart)

            # Commit the changes to the database
            db.session.commit()

            # Clear the session cart after saving to DB
            # session.pop("cart", None)

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

            cart_data = cart.load_cart_data()

            total_price = sum(
                item.get("price", 0) * item.get("quantity", 0) for item in cart_data
            )

            session["cart"] = cart.load_cart_data()

            return {
                "cart": session["cart"],
                "total_price": total_price,
            }, HTTP_200_OK
        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def checkout(customer_id,data):
        shipping_address = data.get("shipping_address")
        shipping_cost = data.get("shipping_cost")
        
        # Retrieve session cart
        session_cart = session.get("cart", [])

        if not session_cart:
            return {"error": "Cart is empty"}, HTTP_400_BAD_REQUEST

        try:
            # Validate cart (Check stock availability)
            for item in session_cart:
                product = Product.query.get(item["product_id"])
                if not product or product.stock < item["quantity"]:
                    return {
                        "error": f"Product {product.name if product else 'N/A'} is out of stock"
                    }, HTTP_400_BAD_REQUEST

            payment_status = (
                Payment.process_payment()
            )  # Dummy function, assumes successful payment
            if not payment_status:
                return {"error": "Payment failed"}, HTTP_400_BAD_REQUEST

            # Create Order
            order = Order(
                customer_id=customer_id,
                order_date=datetime.now(),
                shipping_address=shipping_address,
                shipping_cost = shipping_cost,
                total_amount=sum(
                    item["price"] * item["quantity"] for item in session_cart
                ) + float(shipping_cost),
                
            )
            db.session.add(order)
            db.session.commit()

            # Create OrderItems and update stock
            for item in session_cart:
                product = Product.query.get(item["product_id"])

                # Create OrderItem entry
                order_item = OrderItem(
                    order_id=order.id,
                    customer_id= customer_id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item["quantity"],
                    price=item["price"],
                    total_price=
                        item["price"] * item["quantity"],
                )
                db.session.add(order_item)

                # Update product stock
                product.stock -= item["quantity"]
                db.session.commit()

            # Clear session cart
            session.pop("cart", None)

            saved_cart = Cart.query.filter_by(customer_id=customer_id).first()
            if saved_cart:
                db.session.delete(saved_cart)
                db.session.commit()

            return {"msg": "Checkout successful", "order_id": order.id}, HTTP_200_OK

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def reomve_item_cart(data):
        try:
            product_id = data.get("product_id")
            if not product_id:
                return {"error": "Product_id not found"}, HTTP_404_NOT_FOUND

            session_cart = session.get("cart", [])
            if not session_cart:
                return {"error": "Cart not found"}, HTTP_404_NOT_FOUND

            item_removed = False
            updated_cart = []

            for item in session_cart:
                if item["product_id"] == product_id:
                    item_removed = True
                else:
                    updated_cart.append(item)

            if not item_removed:
                return {"error": "Item not found in the cart"}, HTTP_404_NOT_FOUND

            session["cart"] = updated_cart

            return {"msg": "Item successfully removed from cart"}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def update_quantity_of_items(data):
        try:
            product_id = data.get("product_id")
            action = data.get("action")

            session_cart = session.get("cart", [])
            if not session_cart:
                return {"error": "cart not found"}, HTTP_404_NOT_FOUND

            item_found = False

            for item in session_cart:
                if item['product_id'] == product_id:
                    if action == 'increase':
                        item['quantity'] += 1
                    elif action == 'decrease' and item['quantity'] > 1:
                        item["quantity"] -= 1

                    item_found = True
                    break

            if not item_found:
                return {"error": "item not found"}, HTTP_404_NOT_FOUND

            session['cart'] = session_cart

            return {"msg": " Cart is updated successfully "}, HTTP_200_OK

        except:
            ...


class Payment:
    @staticmethod
    def process_payment():
        # This is a placeholder function.
        # You would replace this with actual payment gateway integration.
        return True  # Simulate successful payment


class Cart_Utils:
    @staticmethod
    def merge_carts(session_cart, saved_cart):
        if not saved_cart:
            return session_cart

        merged_cart = {item["product_id"]: item for item in saved_cart}

        # Update quantities or add new items from session cart
        for session_item in session_cart:
            product_id = session_item["product_id"]
            if product_id in merged_cart:
                merged_cart[product_id]["quantity"] += session_item["quantity"]
            else:
                merged_cart[product_id] = session_item

        return list(merged_cart.values())

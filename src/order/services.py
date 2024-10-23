from ..extensions import db
from ..model import Order, OrderItem
from flask_jwt_extended import get_jwt_identity
from src.constants.Http_status_code import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)


class OrderServices:
    @staticmethod
    def order_list():
        try:
            customer_id = get_jwt_identity()

            orders = Order.query.filter_by(customer_id=customer_id).all()
            if not orders:
                return {"error": "Order not found"}, HTTP_404_NOT_FOUND

            data = []
            for order in orders:
                data.append(
                    {
                        "order_id": order.id,
                        "order_date": order.order_date,
                        "total_Amount": order.total_amount,
                    }
                )

            return {"data": data}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def order_details(data):
        try:
            customer_id = get_jwt_identity()
            order_id = data.get("order_id")
            
            order = Order.query.filter_by(id=order_id, customer_id=customer_id).first()
            if not order:
                return {"error": "Order detials not found"}, HTTP_404_NOT_FOUND

            order_items = OrderItem.query.filter_by(order_id = order.id).all()
            item_list = []
            subtotal = 0
            for item in order_items:

                item_list.append(
                    {
                            "order_id": order.id,
                            "product_id": item.product_id,
                            "product_name": item.product_name,
                            "quantity": item.quantity,
                            "price": item.price,
                            "total_price": item.total_price,
                        }
                    )
                subtotal +=item.total_price
            return {
                      "order_detial": item_list,
                      "subtotal": subtotal,
                      "shipping_cost":order.shipping_cost,
                      "total": subtotal + order.shipping_cost,
                      "shipping_address": order.shipping_address
                    },HTTP_200_OK
        except Exception as e:
            return {"error":str(e)},HTTP_500_INTERNAL_SERVER_ERROR

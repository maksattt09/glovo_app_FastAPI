from mysite.database.models import  (
    UserProfile, Category, Store, Product, Order, Courier,
    Review, Cart, CartItem, RefreshToken
)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.email, UserProfile.role]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class StoreAdmin(ModelView, model=Store):
    column_list = [
        Store.id, Store.store_name, Store.description,
        Store.category_id, Store.owner_id, Store.contact_info, Store.address
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id, Product.product_name, Product.description,
        Product.price, Product.quantity, Product.store_id
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id, Order.client_id, Order.products_id,
        Order.status, Order.delivery_address, Order.courier_id, Order.created_at
    ]


class CourierAdmin(ModelView, model=Courier):
    column_list = [
        Courier.id, Courier.user_id, Courier.status_courier, Courier.current_orders_id
    ]


class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id, Review.client_review_id, Review.store_review_id,
        Review.courier_review_id, Review.rating, Review.comment
    ]


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id, Cart.user_id]


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.id, CartItem.cart_id, CartItem.product_id, CartItem.quantity]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id]



from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, DateTime, ForeignKey, Text
from typing import List
from enum import Enum as PyEnum
from datetime import date, datetime


class StatusChoicesRole(str, PyEnum):
    admin = 'admin'
    client = 'client'
    owner = 'owner'
    courier = 'courier'


class StatusChoicesOrder(str, PyEnum):
    pending = 'pending'
    canceled = 'canceled'
    delivered = 'delivered'


class StatusChoicesCourier(str, PyEnum):
    free = 'free'
    busy = 'busy'


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    role: Mapped[StatusChoicesRole] = mapped_column(Enum(StatusChoicesRole), default=StatusChoicesRole.client)
    user_owner: Mapped[List['Store']] = relationship(back_populates='owner_user', cascade='all, delete-orphan')
    order_courier: Mapped[List['Order']] = relationship('Order',back_populates='courier_order',cascade='all, delete-orphan',foreign_keys='Order.courier_id')
    courier_users: Mapped[List['Courier']] = relationship(back_populates='user_courier', cascade='all, delete-orphan')
    review_client: Mapped[List['Review']] = relationship('Review',back_populates='client_review',cascade='all, delete-orphan',foreign_keys='Review.client_review_id')
    user_client: Mapped[List['Order']] = relationship('Order',back_populates='client_user',cascade='all, delete-orphan',foreign_keys='Order.client_id')
    cart_user: Mapped['Cart'] = relationship(back_populates='user', uselist=False)
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')


    def __str__(self):
        return self.username


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    store_category: Mapped[List['Store']] = relationship(back_populates='category_store', cascade='all, delete-orphan')

    def __str__(self):
        return self.category_name


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category_store: Mapped['Category'] = relationship(back_populates='store_category')
    contact_info: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    owner_user: Mapped['UserProfile'] = relationship(back_populates='user_owner')
    product_store: Mapped[List['Product']] = relationship(back_populates='store_product', cascade='all, delete-orphan')
    review_store: Mapped[List['Review']] = relationship(back_populates='store_review', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(51), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_product: Mapped['Store'] = relationship(back_populates='product_store')
    order_product: Mapped[List['Order']] = relationship(back_populates='product_order')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    client_user: Mapped['UserProfile'] = relationship('UserProfile',back_populates='user_client',foreign_keys=[client_id])
    products_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product_order: Mapped['Product'] = relationship(back_populates='order_product')
    status: Mapped[StatusChoicesOrder] = mapped_column(Enum(StatusChoicesOrder), default=StatusChoicesOrder.pending)
    delivery_address: Mapped[str] = mapped_column(String(60))
    courier_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    courier_order: Mapped['UserProfile'] = relationship('UserProfile',back_populates='order_courier',foreign_keys=[courier_id])
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
    orders_current: Mapped[List['Courier']] = relationship(back_populates='current_orders', cascade='all, delete-orphan')


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user_courier: Mapped['UserProfile'] = relationship(back_populates='courier_users')
    status_courier: Mapped[StatusChoicesCourier] = mapped_column(Enum(StatusChoicesCourier), default=StatusChoicesCourier.free)
    current_orders_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    current_orders: Mapped['Order'] = relationship(back_populates='orders_current')

    # правильная связь с отзывами
    reviews: Mapped[List['Review']] = relationship(
        'Review',
        back_populates='courier_review',
        cascade='all, delete-orphan',
        foreign_keys='Review.courier_review_id'
    )


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_review_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    client_review: Mapped['UserProfile'] = relationship('UserProfile', back_populates='review_client',
                                                        foreign_keys=[client_review_id])

    store_review_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_review: Mapped['Store'] = relationship('Store', back_populates='review_store')

    courier_review_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier_review: Mapped['Courier'] = relationship('Courier', back_populates='reviews',
                                                     foreign_keys=[courier_review_id])

    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id:  Mapped[int] = mapped_column(ForeignKey('profile.id'), unique=True)
    user: Mapped['UserProfile'] = relationship(UserProfile, back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Cart'] = relationship(Cart, back_populates='items')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship(Product)
    quantity: Mapped[int] = mapped_column(Integer, default=1)



class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'{self.token}'


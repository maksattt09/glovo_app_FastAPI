from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from .models import StatusChoicesRole, StatusChoicesOrder, StatusChoicesCourier


class UserProfileInputSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str


class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    role: StatusChoicesRole



class CategoryInputSchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    id: int
    category_name: str


class StoreInputSchema(BaseModel):
    store_name: str
    description: str
    category_id: int
    contact_info: str
    address: str
    owner_id: int


class StoreOutSchema(BaseModel):
    id: int
    store_name: str
    description: str
    category_id: int
    contact_info: str
    address: str
    owner_id: int


class ProductInputSchema(BaseModel):
    product_name: str
    description: str
    price: int
    quantity: int
    store_id: int


class ProductOutSchema(BaseModel):
    id: int
    product_name: str
    description: str
    price: int
    quantity: int
    store_id: int


class OrderInputSchema(BaseModel):
    client_id: int
    products_id: int
    delivery_address: str
    courier_id: int


class OrderOutSchema(BaseModel):
    id: int
    client_id: int
    products_id: int
    status: StatusChoicesOrder
    delivery_address: str
    courier_id: int
    created_at: date


class CourierInputSchema(BaseModel):
    user_id: int
    current_orders_id: int


class CourierOutSchema(BaseModel):
    id: int
    user_id: int
    status_courier: StatusChoicesCourier
    current_orders_id: int


class ReviewInputSchema(BaseModel):
    client_review_id: int
    store_review_id: int
    courier_review_id: int
    rating: int = Field(None, gt=0, lt=6)
    comment: str


class ReviewOutSchema(BaseModel):
    id: int
    client_review_id: int
    store_review_id: int
    courier_review_id: int
    rating: int = Field(None, gt=0, lt=6)
    comment: str


class CartInputSchema(BaseModel):
    id: int
    user_id: int


class CartOutSchema(BaseModel):
    id: int
    user_id: int



class CartItemInputSchema(BaseModel):
    product_id: int
    quantity: int

    product_name: Optional[str] = None
    product_price: Optional[int] = None

class CartItemOutSchema(BaseModel):
    id: int
    product_id: int
    quantity: int

    product_name: Optional[str] = None
    product_price: Optional[int] = None



class UserLoginSchema(BaseModel):
    username: str
    password: str
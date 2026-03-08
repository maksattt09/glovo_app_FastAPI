from .views import *

from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine

def setup_admin(mysite: FastAPI):
    admin = Admin(mysite, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(CourierAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)
    admin.add_view(RefreshTokenAdmin)


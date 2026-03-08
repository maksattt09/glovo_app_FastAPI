from fastapi import FastAPI
import uvicorn
from mysite.admin.setup import setup_admin


from mysite.api import auth, user, cart, store, review, product, order, courier, category


glovo_app = FastAPI(title='Store Project')

glovo_app.include_router(user.user_router)
glovo_app.include_router(category.category_router)
glovo_app.include_router(store.store_router)
glovo_app.include_router(product.product_router)
glovo_app.include_router(courier.courier_router)
glovo_app.include_router(order.order_router)
glovo_app.include_router(review.review_router)
glovo_app.include_router(cart.cart_router)
glovo_app.include_router(auth.auth_router)
setup_admin(glovo_app)


if __name__ == '__main__':
    uvicorn.run(glovo_app, host='127.0.0.1', port=8002)
from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Cart
from mysite.database.schema import CartInputSchema, CartOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

cart_router = APIRouter(prefix='/cart', tags=['Cart'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_router.post('/', response_model=CartOutSchema)
async def create_cart(item: CartInputSchema, db: Session = Depends(get_db)):
    cart_db = Cart(**item.dict())
    db.add(cart_db)
    db.commit()
    db.refresh(cart_db)
    return cart_db


@cart_router.get('/', response_model=List[CartOutSchema])
async def list_cart(db: Session = Depends(get_db)):
    return db.query(Cart).all()


@cart_router.get('/{cart_id}/', response_model=CartOutSchema)
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(detail='нету такой информации', status_code=400)
    return cart_db


@cart_router.put('/{cart_id}/', response_model=dict)
async def update_cart(cart_id: int, item: CartInputSchema, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(detail='мындай категору жок', status_code=400)

    for key, value in item.dict().items():
        setattr(cart_db, key, value)

    db.commit()
    db.refresh(cart_db)
    return {'message': 'cart озгорулду'}


@cart_router.delete('/{cart_id}/', response_model=dict)
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(detail='мындай cart жок', status_code=400)

    db.delete(cart_db)
    db.commit()
    return {'message': 'cart удалит этилди'}
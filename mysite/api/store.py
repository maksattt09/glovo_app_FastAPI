from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Store
from mysite.database.schema import StoreInputSchema, StoreOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_router = APIRouter(prefix='/store', tags=['Store'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_router.post('/', response_model=StoreOutSchema)
async def create_store(store: StoreInputSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.get('/', response_model=List[StoreOutSchema])
async def list_store(db: Session = Depends(get_db)):
    return db.query(Store).all()


@store_router.get('/{store_id}/', response_model=StoreOutSchema)
async def detail_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail='нету такой информации', status_code=400)
    return store_db


@store_router.put('/{store_id}/', response_model=dict)
async def update_store(store_id: int, store: StoreInputSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail='мындай категору жок', status_code=400)

    for key, value in store.dict().items():
        setattr(store_db, key, value)

    db.commit()
    db.refresh(store_db)
    return {'message': 'store озгорулду'}


@store_router.delete('/{store_id}/', response_model=dict)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail='мындай store жок', status_code=400)

    db.delete(store_db)
    db.commit()
    return {'message': 'store удалит этилди'}
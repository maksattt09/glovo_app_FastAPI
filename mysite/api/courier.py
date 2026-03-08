from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Courier
from mysite.database.schema import CourierInputSchema, CourierOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

courier_router = APIRouter(prefix='/courier', tags=['Courier'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@courier_router.post('/', response_model=CourierOutSchema)
async def create_courier(courier: CourierInputSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.get('/', response_model=List[CourierOutSchema])
async def list_courier(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/{courier_id}/', response_model=CourierOutSchema)
async def detail_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='нету такой информации', status_code=400)
    return courier_db


@courier_router.put('/{courier_id}/', response_model=dict)
async def update_courier(courier_id: int, courier: CourierInputSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='мындай категору жок', status_code=400)

    for key, value in courier.dict().items():
        setattr(courier_db, key, value)

    db.commit()
    db.refresh(courier_db)
    return {'message': 'courier озгорулду'}


@courier_router.delete('/{courier_id}/', response_model=dict)
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail='мындай courier жок', status_code=400)

    db.delete(courier_db)
    db.commit()
    return {'message': 'courier удалит этилди'}
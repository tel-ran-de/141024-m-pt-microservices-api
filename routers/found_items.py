import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db


router = APIRouter()


@router.post("/", response_model=schemas.FoundItem)
async def create_found_item(item: schemas.FoundItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.FoundItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.FoundItem])
async def read_found_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FoundItem))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.FoundItem)
async def read_found_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(models.FoundItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.FoundItem)
async def update_found_item(item_id: int, item: schemas.FoundItemUpdate, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.FoundItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_found_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.FoundItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted"}

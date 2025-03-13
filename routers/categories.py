from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
import models
import schemas


router = APIRouter()


@router.post("/", response_model=schemas.CategoryRead)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.get("/{category_id}", response_model=schemas.CategoryRead)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.execute(select(models.Category).where(models.Category.id == category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=schemas.CategoryRead)
async def update_category(category_id: int, category_update: schemas.CategoryUpdate,
                          db: AsyncSession = Depends(get_db)):
    category = await db.execute(select(models.Category).where(models.Category.id == category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_update.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.execute(select(models.Category).where(models.Category.id == category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category)
    await db.commit()
    return {"message": "Category deleted"}
import schemas
import models
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from database import get_db


router = APIRouter()


@router.post("/", response_model=schemas.FoundItem)
async def create_found_item(
    item: schemas.FoundItemCreate,
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли категория
    category = await db.execute(
        select(models.Category).where(models.Category.id == item.category_id)
    )
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Создаём новую запись FoundItem
    db_item = models.FoundItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.FoundItem])
async def read_found_items(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(10, gt=0, description="Сколько записей вернуть"),
    category_id: Optional[int] = Query(None, description="Фильтрация по категории"),
    location: Optional[str] = Query(None, description="Фильтрация по локации (фрагмент)"),
    order_by: Optional[str] = Query(None, description="Поле для сортировки, например 'found_date'"),
    sort_desc: bool = Query(False, description="Сортировать по убыванию, если True")
):
    """
    Возвращает список найденных вещей (FoundItem) с поддержкой:
    - Пагинации (skip, limit)
    - Фильтрации (category_id, location)
    - Сортировки (order_by, sort_desc)
    """

    # Главная разница: добавляем options(selectinload)
    query = (
        select(models.FoundItem)
        .options(selectinload(models.FoundItem.tags))
    )

    # Фильтрация по category_id, если указано
    if category_id is not None:
        query = query.where(models.FoundItem.category_id == category_id)

    # Фильтрация по location (текстовое вхождение), если указано
    if location:
        query = query.where(models.FoundItem.location.ilike(f"%{location}%"))

    # Сортировка
    if order_by:
        # Проверяем, есть ли такое поле у FoundItem
        column_attr = getattr(models.FoundItem, order_by, None)
        if column_attr is not None:
            if sort_desc:
                query = query.order_by(column_attr.desc())
            else:
                query = query.order_by(column_attr.asc())

    # Пагинация
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()
    return items


# -----------------------------------------------------------------------------
# Метод "привязать тег" (POST /found_items/{found_item_id}/tags?tag_id=...)
# -----------------------------------------------------------------------------
@router.post("/{found_item_id}/tags", response_model=schemas.FoundItem)
async def attach_tag_to_found_item(
    found_item_id: int,
    tag_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):

    # Вместо db.get(...):
    # 1) Выполним явный SELECT с .options(selectinload(...))
    found_item_query = (
        select(models.FoundItem)
        .where(models.FoundItem.id == found_item_id)
        .options(selectinload(models.FoundItem.tags))  # <- тут принудительная загрузка
    )
    found_item_result = await db.execute(found_item_query)
    found_item = found_item_result.scalar_one_or_none()
    if not found_item:
        raise HTTPException(status_code=404, detail="FoundItem not found")

    # Получаем тег
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Теперь found_item.tags уже загружено в этом же контексте,
    # и при обращении к found_item.tags не будет ленивой (lazy) загрузки.
    if tag not in found_item.tags:
        found_item.tags.append(tag)
        await db.commit()
        await db.refresh(found_item)

    return found_item


@router.delete("/{found_item_id}/tags/{tag_id}")
async def detach_tag_from_found_item(
    found_item_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Удаляет связь между FoundItem и Tag.
    Если связь не существует, ничего не меняется.
    Возвращаем простое подтверждение,
    либо можно вернуть полный объект FoundItem.
    """

    # Вместо db.get(...):
    # Делаем явный SELECT + selectinload(FoundItem.tags)
    found_item_query = (
        select(models.FoundItem)
        .where(models.FoundItem.id == found_item_id)
        .options(selectinload(models.FoundItem.tags))  # важный момент!
    )
    found_item_result = await db.execute(found_item_query)
    found_item = found_item_result.scalar_one_or_none()
    if not found_item:
        raise HTTPException(status_code=404, detail="FoundItem not found")

    # Тут можно db.get(...) для тега, это ОК, т. к. тег не требует eager loading
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Теперь found_item.tags уже загружено
    if tag in found_item.tags:
        found_item.tags.remove(tag)
        await db.commit()

    return {"detail": "Tag detached from FoundItem"}


@router.get("/{item_id}", response_model=schemas.FoundItem)
async def read_found_item(
        item_id: int,
        db: AsyncSession = Depends(get_db)
):
    item = await db.get(models.FoundItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.FoundItem)
async def update_found_item(
        item_id: int,
        item: schemas.FoundItemUpdate,
        db: AsyncSession = Depends(get_db)
):
    db_item = await db.get(models.FoundItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_found_item(
        item_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_item = await db.get(models.FoundItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted"}

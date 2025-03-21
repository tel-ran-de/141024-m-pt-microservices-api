import schemas
import models
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload  # <-- добавили
from typing import Optional
from database import get_db
from utils.security import get_token_data
from utils.chatgpt import chatgpt_similarity
import schemas

router = APIRouter()


@router.post("/", response_model=schemas.LostItem)
async def create_lost_item(
        item: schemas.LostItemCreate,
        db: AsyncSession = Depends(get_db),
        token_data: schemas.TokenData = Depends(get_token_data)
):
    # Проверка существования категории
    category = await db.execute(
        select(models.Category).where(models.Category.id == item.category_id)
    )
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_item = models.LostItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    # Явно загружаем связь tags через selectinload
    result = await db.execute(
        select(models.LostItem)
        .options(selectinload(models.LostItem.tags))
        .where(models.LostItem.id == db_item.id)
    )
    db_item = result.scalar_one_or_none()
    return db_item


@router.get("/", response_model=list[schemas.LostItem])
async def read_lost_items(
        db: AsyncSession = Depends(get_db),
        skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
        limit: int = Query(10, gt=0, description="Сколько записей вернуть"),
        category_id: Optional[int] = Query(None, description="Фильтрация по категории"),
        location: Optional[str] = Query(None, description="Фильтрация по локации (фрагмент)"),
        order_by: Optional[str] = Query(None, description="Поле для сортировки, например 'lost_date'"),
        sort_desc: bool = Query(False, description="Сортировать по убыванию, если True"),
        # token_data: schemas.TokenData = Depends(get_token_data),
):
    """
    Возвращает список потерянных вещей (LostItem) с поддержкой:
    - Пагинации (skip, limit)
    - Фильтрации (category_id, location)
    - Сортировки (order_by, sort_desc)
    """

    # Главная разница: добавляем options(selectinload)
    query = (
        select(models.LostItem)
        .options(selectinload(models.LostItem.tags))
    )

    # Фильтрация по category_id
    if category_id is not None:
        query = query.where(models.LostItem.category_id == category_id)

    # Фильтрация по location (текстовое вхождение)
    if location:
        query = query.where(models.LostItem.location.ilike(f"%{location}%"))

    # Сортировка
    if order_by:
        # Проверяем, действительно ли такое поле есть у модели LostItem
        column_attr = getattr(models.LostItem, order_by, None)
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
# Метод "привязать тег" (POST /lost_items/{lost_item_id}/tags?tag_id=...)
# -----------------------------------------------------------------------------
@router.post("/{lost_item_id}/tags", response_model=schemas.LostItem)
async def attach_tag_to_lost_item(
        lost_item_id: int,
        tag_id: int = Query(...),
        db: AsyncSession = Depends(get_db),
        token_data: schemas.TokenData = Depends(get_token_data)
):
    # Вместо db.get(...):
    # 1) Выполним явный SELECT с .options(selectinload(...))
    lost_item_query = (
        select(models.LostItem)
        .where(models.LostItem.id == lost_item_id)
        .options(selectinload(models.LostItem.tags))  # <- тут принудительная загрузка
    )
    lost_item_result = await db.execute(lost_item_query)
    lost_item = lost_item_result.scalar_one_or_none()
    if not lost_item:
        raise HTTPException(status_code=404, detail="LostItem not found")

    # Получаем тег
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Теперь lost_item.tags уже загружено в этом же контексте,
    # и при обращении к lost_item.tags не будет ленивой (lazy) загрузки.
    if tag not in lost_item.tags:
        lost_item.tags.append(tag)
        await db.commit()
        await db.refresh(lost_item)

    return lost_item


@router.delete("/{lost_item_id}/tags/{tag_id}")
async def detach_tag_from_lost_item(
        lost_item_id: int,
        tag_id: int,
        db: AsyncSession = Depends(get_db),
        token_data: schemas.TokenData = Depends(get_token_data)
):
    """
    Удаляет связь между LostItem и Tag.
    Если связь не существует, ничего не меняется.
    Возвращаем простое подтверждение,
    либо можно вернуть полный объект LostItem.
    """

    # Вместо db.get(...):
    # Делаем явный SELECT + selectinload(LostItem.tags)
    lost_item_query = (
        select(models.LostItem)
        .where(models.LostItem.id == lost_item_id)
        .options(selectinload(models.LostItem.tags))  # важный момент!
    )
    lost_item_result = await db.execute(lost_item_query)
    lost_item = lost_item_result.scalar_one_or_none()
    if not lost_item:
        raise HTTPException(status_code=404, detail="LostItem not found")

    # Тут можно db.get(...) для тега, это ОК, т. к. тег не требует eager loading
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Теперь lost_item.tags уже загружено
    if tag in lost_item.tags:
        lost_item.tags.remove(tag)
        await db.commit()

    return {"detail": "Tag detached from LostItem"}


@router.get("/{item_id}", response_model=schemas.LostItem)
async def read_lost_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        # token_data: schemas.TokenData = Depends(get_token_data)
):
    result = await db.execute(
        select(models.LostItem)
        .options(selectinload(models.LostItem.tags))
        .where(models.LostItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.LostItem)
async def update_lost_item(
        item_id: int,
        item: schemas.LostItemUpdate,
        db: AsyncSession = Depends(get_db),
        token_data: schemas.TokenData = Depends(get_token_data)
):
    db_item = await db.get(models.LostItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)

    await db.commit()
    await db.refresh(db_item)

    # Выполняем повторный запрос с eager loading для поля tags
    result = await db.execute(
        select(models.FoundItem)
        .options(selectinload(models.FoundItem.tags))
        .where(models.FoundItem.id == item_id)
    )
    db_item = result.scalar_one_or_none()
    return db_item


@router.delete("/{item_id}")
async def delete_lost_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        token_data: schemas.TokenData = Depends(get_token_data)
):
    db_item = await db.get(models.LostItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted"}


@router.get("/{lost_item_id}/similar_found_items")
async def get_similar_found_items(
    lost_item_id: int,
    db: AsyncSession = Depends(get_db),
    top_k: int = Query(5, description="Сколько максимально похожих вернуть"),
    # token_data: schemas.TokenData = Depends(get_token_data)  # если нужна авторизация
):
    """
    Для данного LostItem вызываем ChatGPT (модель ChatCompletion)
    и сравниваем его с каждым FoundItem.
    Возвращаем top_k найденных предметов с наибольшим 'процентом совпадения'.
    (На каждый FoundItem уходит отдельный запрос к ChatGPT!)
    """

    # 1) Ищем LostItem
    result = await db.execute(
        select(models.LostItem)
        .options(
            selectinload(models.LostItem.tags),
            selectinload(models.LostItem.category)
        )
        .where(models.LostItem.id == lost_item_id)
    )
    lost_item = result.scalar_one_or_none()
    if not lost_item:
        raise HTTPException(status_code=404, detail="LostItem not found")

    # 2) Формируем текст LostItem
    lost_parts = [
        f"Название: {lost_item.name}",
        f"Описание: {lost_item.description or ''}"
    ]
    if lost_item.category:
        lost_parts.append(f"Категория: {lost_item.category.name}")
    if lost_item.tags:
        tag_names = ", ".join(tag.name for tag in lost_item.tags)
        lost_parts.append(f"Теги: {tag_names}")
    lost_text = "\n".join(lost_parts)

    # 3) Берём все FoundItem (можете сделать фильтры, если нужно)
    found_result = await db.execute(
        select(models.FoundItem)
        .options(
            selectinload(models.FoundItem.tags),
            selectinload(models.FoundItem.category)
        )
    )
    found_items = found_result.scalars().all()
    if not found_items:
        return []

    # 4) Для каждого FoundItem формируем prompt и вызываем ChatGPT
    scored_items = []
    for f_item in found_items:
        found_parts = [
            f"Название: {f_item.name}",
            f"Описание: {f_item.description or ''}"
        ]
        if f_item.category:
            found_parts.append(f"Категория: {f_item.category.name}")
        if f_item.tags:
            ftags = ", ".join(tag.name for tag in f_item.tags)
            found_parts.append(f"Теги: {ftags}")
        found_text = "\n".join(found_parts)

        # Вызываем ChatGPT, получаем число 0..100
        similarity_score = chatgpt_similarity(lost_text, found_text)

        scored_items.append((f_item, similarity_score))

    # 5) Сортируем по убыванию
    scored_items.sort(key=lambda x: x[1], reverse=True)

    # 6) Формируем ответ (берём первые top_k)
    results = []
    for item, score in scored_items[:top_k]:
        # Конвертируем FoundItem в pydantic-модель (schemas.FoundItem)
        item_data = schemas.FoundItem(
            id=item.id,
            category_id=item.category_id,
            name=item.name,
            description=item.description,
            found_date=item.found_date,
            location=item.location,
            tags=[schemas.TagRead(id=t.id, name=t.name) for t in item.tags]
        )
        results.append({
            "found_item": item_data,
            "similarity_percent": round(score, 2)
        })

    return results

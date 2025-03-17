from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_db
import models
import schemas


router = APIRouter()


@router.post("/", response_model=schemas.TagRead)
async def create_tag(
    tag_in: schemas.TagCreate,
    db: AsyncSession = Depends(get_db),
    # token: str = Depends(oauth2_scheme),  # 👈 явно используем схему OAuth2 из main
    # user: models.User = Depends(get_current_user),  # 👈 защита через JWT
):
    """
    Создаём новый тег.
    Если в базе уже есть такой же name, выбрасываем ошибку (400).
    """
    # Проверяем, есть ли тег с таким же именем
    result = await db.execute(
        select(models.Tag).where(models.Tag.name == tag_in.name)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")

    new_tag = models.Tag(name=tag_in.name)
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag


@router.get("/", response_model=List[schemas.TagRead])
async def read_tags(
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращаем список всех тегов в базе.
    """
    result = await db.execute(select(models.Tag))
    tags = result.scalars().all()
    return tags


@router.get("/{tag_id}", response_model=schemas.TagRead)
async def read_tag_by_id(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    # token: str = Depends(oauth2_scheme),  # 👈 явно используем схему OAuth2 из main
    # user: models.User = Depends(get_current_user),  # 👈 защита через JWT
):
    """
    Ищем тег по ID.
    """
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=schemas.TagRead)
async def update_tag(
    tag_id: int,
    tag_in: schemas.TagCreate,  # или отдельная схема для update
    db: AsyncSession = Depends(get_db),
    # token: str = Depends(oauth2_scheme),  # 👈 явно используем схему OAuth2 из main
    # user: models.User = Depends(get_current_user),  # 👈 защита через JWT
):
    """
    Обновляем name тега.
    Если пытаются установить имя, которое уже занято — ошибка 400.
    """
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Если имя изменилось
    if tag_in.name != tag.name:
        # Проверяем, нет ли в базе другого тега с таким именем
        result = await db.execute(
            select(models.Tag).where(models.Tag.name == tag_in.name)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Another tag with this name already exists")

    tag.name = tag_in.name
    await db.commit()
    await db.refresh(tag)
    return tag


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    # token: str = Depends(oauth2_scheme),  # 👈 явно используем схему OAuth2 из main
    # user: models.User = Depends(get_current_user),  # 👈 защита через JWT
):
    """
    Удаляем тег из базы по ID.
    Если у тега есть связи, SQLAlchemy очистит записи из промежуточных таблиц
    (например, lostitem_tag), но связанные LostItem или FoundItem не удалятся.
    """
    tag = await db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    await db.delete(tag)
    await db.commit()
    return {"detail": "Tag deleted"}

import os

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_, or_
import models, schemas
import aiohttp
from database import AsyncSession, get_db

router = APIRouter()

LOST_ITEMS_SERVICE_URL = os.getenv("LOST_ITEMS_SERVICE_URL", "http://lostfound_service:8000/api/lost_items/")

@router.post("/", response_model=schemas.Auction)
async def create_auction(auction: schemas.AuctionCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового аукциона."""

    # Отправляем запрос в lost_found_service для проверки предмета с указанным id
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{LOST_ITEMS_SERVICE_URL}{auction.lost_item_external_id}") as response:
            if response.status == 404:
                raise HTTPException(status_code=400, detail="Предмет с указанным ID не найден")
            elif response.status != 200:
                raise HTTPException(status_code=500, detail="Ошибка при проверке существования предмета")
    db_auction = models.Auction(**auction.model_dump())
    db.add(db_auction)
    await db.commit()
    await db.refresh(db_auction)
    return db_auction


@router.get("/", response_model=list[schemas.Auction])
async def get_auctions(
        status: str | None = Query(None),
        is_active: bool | None = Query(None),
        db: AsyncSession = Depends(get_db)
):
    """Получение списка аукционов с возможностью фильтрации."""
    query = select(models.Auction)
    conditions = []

    if status:
        conditions.append(models.Auction.status == status)
    if is_active is not None:
        conditions.append(models.Auction.is_active == is_active)

    if conditions:
        query = query.where(and_(*conditions))

    results = await db.execute(query)
    auctions = results.scalars().all()
    return auctions

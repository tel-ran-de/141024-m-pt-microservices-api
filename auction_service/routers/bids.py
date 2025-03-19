from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_, or_
import models, schemas
import aiohttp
from database import AsyncSession, get_db

router = APIRouter()

AUTH_SERVICE_URL = "http://127.0.0.1:8003/users/"  # Замените на URL вашего сервиса аутентификации


@router.post("/auctions/{auction_id}/bids/", response_model=schemas.Bid)
async def create_bid(auction_id: int, bid: schemas.BidCreate, db: AsyncSession = Depends(get_db)):
    """Добавление ставки на аукцион."""

    # Проверяем, существует ли аукцион
    auction = await db.get(models.Auction, auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Аукцион не найден")

    # Проверяем, активен ли аукцион
    if not auction.is_active:
        raise HTTPException(status_code=400, detail="Аукцион не активен")

    # Проверяем, что ставка больше текущей цены
    if bid.amount <= auction.current_price:
        raise HTTPException(status_code=400, detail="Ставка должна быть больше текущей цены")

    # TODO: Добавив авторизацию, измените логику работы,
    #  чтобы user_external_id извлекалось не из запроса, а из данных токена авторизации(token_data)

    db_bid = models.Bid(auction_id=auction_id, **bid.model_dump())
    db.add(db_bid)
    auction.current_price = bid.amount  # Обновляем текущую цену аукциона
    await db.commit()
    await db.refresh(db_bid)
    return db_bid


@router.get("/auctions/{auction_id}/bids/", response_model=list[schemas.Bid])
async def get_bids(auction_id: int, db: AsyncSession = Depends(get_db)):
    """Получение списка ставок для аукциона."""
    # Проверяем, существует ли аукцион
    auction = await db.get(models.Auction, auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Аукцион не найден")

    query = select(models.Bid).where(models.Bid.auction_id == auction_id)
    results = await db.execute(query)
    bids = results.scalars().all()
    return bids

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Auctions - аукционы
class AuctionBase(BaseModel):
    lost_item_external_id: str
    start_price: float
    current_price: float
    # start_time: datetime = None
    # end_time: datetime = None


class AuctionCreate(AuctionBase):
    pass


class Auction(AuctionBase):
    id: int
    current_price: float
    status: str
    winner_external_id: str
    is_active: bool
    start_time: datetime
    end_time: datetime


# Bids - ставки
class BidBase(BaseModel):
    user_external_id: str
    amount: float


class BidCreate(BidBase):
    pass


class Bid(BidBase):
    id: int
    timestamp: datetime

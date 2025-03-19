from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, func, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from datetime import timedelta

Base = declarative_base()


class Auction(Base):
    __tablename__ = "auctions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lost_item_external_id: Mapped[str] = mapped_column(String)  # ID из lost_found_service
    start_price: Mapped[float] = mapped_column(Float)
    current_price: Mapped[float] = mapped_column(Float)
    start_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    end_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now() + timedelta(hours=4))
    status: Mapped[str] = mapped_column(String, default="scheduled")
    winner_external_id: Mapped[str] = mapped_column(String, default='')  # ID из auth_service
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    bids = relationship("Bid", back_populates="auction")


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    auction_id: Mapped[int] = mapped_column(Integer, ForeignKey("auctions.id"))
    user_external_id: Mapped[str] = mapped_column(String)  # ID из auth_service
    amount: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    auction = relationship("Auction", back_populates="bids")

from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class LostItem(Base):
    __tablename__ = "lost_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)


class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
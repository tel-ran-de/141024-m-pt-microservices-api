"""
Демонстрация пагинации, фильтрации и сортировки одним запуском,
с подробными комментариями и разбиением на пункты.
"""

import asyncio
from sqlalchemy import select
from sqlalchemy import asc, desc
import datetime

# Импортируем вашу асинхронную "фабрику" сессий и модели:
from database import AsyncSessionLocal
import models


async def main():
    """
    Внутри этой функции последовательно показываем
    1) Пагинацию,
    2) Фильтрацию,
    3) Сортировку.
    Используем один вызов asyncio.run(main()) для избежания
    проблем с закрытием event loop.
    """

    # -------------------------
    # Открываем единую сессию
    # -------------------------
    session = AsyncSessionLocal()

    # =========================================
    # Пункт 2: Пагинация
    # =========================================
    print("=== Пункт 2: Пагинация ===\n")

    # Для чего нужна пагинация:
    # Когда в таблице очень много записей, выводить их все за раз неэффективно.
    # Поэтому разбиваем данные на страницы: выбираем, скажем, по 5 записей.

    # Пример: берём "первую страницу" (skip=0, limit=5)
    query_page1 = select(models.LostItem).offset(0).limit(5)
    result_page1 = await session.execute(query_page1)
    page1_items = result_page1.scalars().all()

    print("Первая страница (5 записей):")
    for item in page1_items:
        print(item.id, item.name, item.location)

    # Пример: берём "вторую страницу" (skip=5, limit=5)
    query_page2 = select(models.LostItem).offset(5).limit(5)
    result_page2 = await session.execute(query_page2)
    page2_items = result_page2.scalars().all()

    print("\nВторая страница (следующие 5 записей):")
    for item in page2_items:
        print(item.id, item.name, item.location)

    # =========================================
    # Пункт 3: Фильтрация
    # =========================================
    print("\n=== Пункт 3: Фильтрация ===\n")

    # Для чего нужна фильтрация:
    # Часто нужно отбирать только те записи, которые соответствуют определённым критериям:
    # по категории, по локации, по текстовому совпадению и т.д.
    # Это позволяет сразу получать нужную часть данных, не загружая лишнего.

    # 1) Фильтр: у LostItem category_id == 2
    query_cat2 = select(models.LostItem).where(models.LostItem.category_id == 2)
    result_cat2 = await session.execute(query_cat2)
    items_cat2 = result_cat2.scalars().all()
    print("LostItem, category_id=2 (Техника):")
    for item in items_cat2:
        print(item.id, item.name, item.category_id, item.location)

    # 2) Фильтр: FoundItem, у кого в location есть 'СПб' (регистронезависимо, ILIKE)
    query_spb = select(models.FoundItem).where(models.FoundItem.location.ilike("%СПб%"))
    result_spb = await session.execute(query_spb)
    spb_found_items = result_spb.scalars().all()
    print("\nFoundItem, где в локации упоминается 'СПб':")
    for item in spb_found_items:
        print(item.id, item.name, item.location)

    # 3) Фильтр: LostItem, потерянные за последние 7 дней (lost_date >= now() - 7)
    week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    query_recent = select(models.LostItem).where(models.LostItem.lost_date >= week_ago)
    result_recent = await session.execute(query_recent)
    recent_items = result_recent.scalars().all()
    print("\nLostItem за последние 7 дней:")
    for item in recent_items:
        print(item.id, item.name, item.lost_date)

    # =========================================
    # Пункт 4: Сортировка
    # =========================================
    print("\n=== Пункт 4: Сортировка ===\n")

    # Для чего нужна сортировка:
    # При большом количестве записей пользователю может быть важно
    # видеть их в определённом порядке: по дате, по алфавиту, по убыванию и т. д.

    # 1) Сортируем LostItem по дате убывания (сначала самые свежие)
    query_desc_date = select(models.LostItem).order_by(models.LostItem.lost_date.desc())
    result_desc_date = await session.execute(query_desc_date)
    lost_desc_date = result_desc_date.scalars().all()
    print("LostItem (самые свежие сначала):")
    for item in lost_desc_date[:5]:
        print(item.id, item.name, item.lost_date)

    # 2) Сортируем FoundItem по алфавиту (name.asc())
    query_asc_name = select(models.FoundItem).order_by(models.FoundItem.name.asc())
    result_asc_name = await session.execute(query_asc_name)
    found_asc_name = result_asc_name.scalars().all()
    print("\nFoundItem (по имени A->Z):")
    for item in found_asc_name:
        print(item.id, item.name)

    # 3) Комбинированная сортировка:
    #    - сначала по category_id (asc)
    #    - затем по name (desc)
    query_combo = select(models.LostItem).order_by(
        asc(models.LostItem.category_id),
        desc(models.LostItem.name)
    )
    result_combo = await session.execute(query_combo)
    lost_combo = result_combo.scalars().all()
    print("\nLostItem, сначала category_id asc, потом name desc:")
    for item in lost_combo:
        print(item.category_id, item.name)

    # Закрываем сессию
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())

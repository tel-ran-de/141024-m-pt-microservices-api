"""
test_db_tasks.py

В этом файле демонстрируется решение 9 заданий:
- 3 задания по пагинации,
- 3 задания по фильтрации,
- 3 задания по сортировке.

Все действия выполняются в одной асинхронной функции `main()`, которую
мы запускаем через `asyncio.run(main())`. Это позволяет избежать
проблем с повторным использованием event loop в интерактивной среде.

Порядок заданий:
1) Пагинация (5.1):
   1.1 LostItem, по 3 штуки на страницу — вывести первую и вторую страницу
   1.2 FoundItem, по 2 штуки на страницу — вывести вторую страницу
   1.3 LostItem, по 4 штуки на страницу — вывести последнюю страницу

2) Фильтрация (5.2):
   2.1 LostItem, у которых в локации встречается "Москва"
   2.2 FoundItem, только для категорий "Документы"(id=1) и "Украшения"(id=4)
   2.3 LostItem, потерянные за последние 10 дней

3) Сортировка (5.3):
   3.1 LostItem: сортировка по name (asc)
   3.2 FoundItem: сортировка по found_date (desc)
   3.3 LostItem: сортировка сначала по category_id (asc), потом lost_date (desc)

После каждого задания выводятся результаты, чтобы проверить, что всё работает правильно.
"""

import asyncio
import datetime
from sqlalchemy import select, func
from sqlalchemy import asc, desc

# Импортируем вашу фабрику сессий и модели:
from database import AsyncSessionLocal
import models


async def main():
    """
    Внутри одной корутины решаем все 9 заданий (по 3 для пагинации, фильтрации, сортировки).
    В конце закрываем сессию. Запуск: python test_db_tasks.py
    """

    # Создаём одну асинхронную сессию
    session = AsyncSessionLocal()

    # -------------------------
    # 5.1 ПАГИНАЦИЯ
    # -------------------------
    print("=== 5.1 ПАГИНАЦИЯ ===")

    # ЗАДАНИЕ 1:
    # LostItem: хотим по 3 штуки на страницу. Нужно вывести
    #   - первую страницу (skip=0, limit=3)
    #   - вторую страницу (skip=3, limit=3)
    print("\nЗАДАНИЕ 1) LostItem, по 3 штуки на страницу. Первая и вторая страница.")

    # Первая страница (skip=0, limit=3)
    q_lost_p1 = select(models.LostItem).offset(0).limit(3)
    r_lost_p1 = await session.execute(q_lost_p1)
    page1_lost = r_lost_p1.scalars().all()
    print("\nПервая страница (3 записи):")
    for item in page1_lost:
        print(item.id, item.name)

    # Вторая страница (skip=3, limit=3)
    q_lost_p2 = select(models.LostItem).offset(3).limit(3)
    r_lost_p2 = await session.execute(q_lost_p2)
    page2_lost = r_lost_p2.scalars().all()
    print("\nВторая страница (следующие 3 записи):")
    for item in page2_lost:
        print(item.id, item.name)

    # ЗАДАНИЕ 2:
    # FoundItem: по 2 штуки на страницу, нужно вывести вторую страницу
    # То есть skip=2, limit=2 (пропускаем первые 2, берём следующие 2).
    print("\nЗАДАНИЕ 2) FoundItem, по 2 штуки на страницу. Вывести вторую страницу.")

    q_found_page2 = select(models.FoundItem).offset(2).limit(2)
    r_found_page2 = await session.execute(q_found_page2)
    page2_found = r_found_page2.scalars().all()
    print("\nFoundItem, страница 2 (2 штуки):")
    for item in page2_found:
        print(item.id, item.name)

    # ЗАДАНИЕ 3:
    # LostItem: по 4 штуки на страницу, нужно вывести последнюю страницу.
    # Для этого:
    # - Считаем общее количество LostItem
    # - Находим общее число страниц
    # - Делаем skip для последней страницы
    print("\nЗАДАНИЕ 3) LostItem, по 4 штуки на страницу, вывести последнюю страницу.")

    q_count_lost = select(func.count(models.LostItem.id))
    r_count_lost = await session.execute(q_count_lost)
    total_lost = r_count_lost.scalar()  # всего записей в lost_items
    page_size = 4

    total_pages = (total_lost + page_size - 1) // page_size  # округляем вверх
    print(f"Всего LostItem: {total_lost}, при page_size={page_size} будет {total_pages} страниц.")

    last_page_skip = (total_pages - 1) * page_size
    q_last_page = select(models.LostItem).offset(last_page_skip).limit(page_size)
    r_last_page = await session.execute(q_last_page)
    last_page_items = r_last_page.scalars().all()

    print(f"\nПоследняя страница (skip={last_page_skip}, limit={page_size}):")
    for item in last_page_items:
        print(item.id, item.name)

    # -------------------------
    # 5.2 ФИЛЬТРАЦИЯ
    # -------------------------
    print("\n=== 5.2 ФИЛЬТРАЦИЯ ===")

    # ЗАДАНИЕ 1:
    # LostItem, у которых в location встречается "Москва" (регистронезависимо)
    # Используем ilike('%Москва%')
    print("\nЗАДАНИЕ 1) LostItem, location ILIKE '%Москва%'")

    q_lost_moscow = select(models.LostItem).where(models.LostItem.location.ilike("%Москва%"))
    r_lost_moscow = await session.execute(q_lost_moscow)
    lost_moscow = r_lost_moscow.scalars().all()
    for item in lost_moscow:
        print(item.id, item.name, item.location)

    # ЗАДАНИЕ 2:
    # FoundItem, категория — только "Документы" и "Украшения".
    # Предположим, у них category_id=1 и category_id=4 (у вас может быть другое, проверяйте в БД).
    print("\nЗАДАНИЕ 2) FoundItem, category_id IN [1, 4]")

    q_found_in_cat = select(models.FoundItem).where(models.FoundItem.category_id.in_([1, 4]))
    r_found_in_cat = await session.execute(q_found_in_cat)
    found_docs_jewelry = r_found_in_cat.scalars().all()
    for item in found_docs_jewelry:
        print(item.id, item.name, f"cat={item.category_id}")

    # ЗАДАНИЕ 3:
    # LostItem, потерянные за последние 10 дней
    # То есть lost_date >= now() - 10
    print("\nЗАДАНИЕ 3) LostItem, потерянные за 10 дней (lost_date >= now()-10)")

    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    q_lost_10d = select(models.LostItem).where(models.LostItem.lost_date >= ten_days_ago)
    r_lost_10d = await session.execute(q_lost_10d)
    recent_10d = r_lost_10d.scalars().all()
    for item in recent_10d:
        print(item.id, item.name, item.lost_date)

    # -------------------------
    # 5.3 СОРТИРОВКА
    # -------------------------
    print("\n=== 5.3 СОРТИРОВКА ===")

    # ЗАДАНИЕ 1:
    # LostItem: сортировка по name (asc)
    # Вывести хотя бы первые 5
    print("\nЗАДАНИЕ 1) LostItem, сортировка name ASC (первые 5).")

    q_lost_name_asc = select(models.LostItem).order_by(models.LostItem.name.asc())
    r_lost_name_asc = await session.execute(q_lost_name_asc)
    sorted_lost_name_asc = r_lost_name_asc.scalars().all()
    for item in sorted_lost_name_asc[:5]:
        print(item.id, item.name)

    # ЗАДАНИЕ 2:
    # FoundItem: сортировка по found_date (desc),
    # чтобы самые последние/свежие были в начале.
    print("\nЗАДАНИЕ 2) FoundItem, сортировка по found_date DESC (первые 5).")

    q_found_date_desc = select(models.FoundItem).order_by(models.FoundItem.found_date.desc())
    r_found_date_desc = await session.execute(q_found_date_desc)
    sorted_found_date_desc = r_found_date_desc.scalars().all()
    for item in sorted_found_date_desc[:5]:
        print(item.id, item.name, item.found_date)

    # ЗАДАНИЕ 3:
    # LostItem: комбинированная сортировка:
    #   - сначала по category_id (asc)
    #   - затем по lost_date (desc)
    print("\nЗАДАНИЕ 3) LostItem, сначала category_id ASC, потом lost_date DESC.")

    q_lost_combo_sort = select(models.LostItem).order_by(
        asc(models.LostItem.category_id),
        desc(models.LostItem.lost_date)
    )
    r_lost_combo_sort = await session.execute(q_lost_combo_sort)
    combo_lost = r_lost_combo_sort.scalars().all()

    for item in combo_lost[:10]:
        print(f"cat={item.category_id}", item.name, item.lost_date)

    # -------------------------
    # Закрываем сессию в самом конце
    # -------------------------
    await session.close()


if __name__ == "__main__":
    # Запускаем единожды: python test_db_tasks.py
    asyncio.run(main())

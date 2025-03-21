import os
import openai
import math


# Подключаем API ключ (по-хорошему через os.getenv или другой способ)
openai.api_key = None


def chatgpt_similarity(lost_text: str, found_text: str) -> float:
    """
    Вызывает OpenAI Chat Completion (gpt-3.5-turbo)
    и просит вернуть число (0..100), показывающее,
    насколько LostItem и FoundItem описывают один и тот же предмет.
    """
    # Собираем "prompt" (точнее, это messages для ChatCompletion)
    system_message = {
        "role": "system",
        "content": (
            "Ты – помощник, который оценивает, совпадают ли два описания предметов. "
            "Возвращай только одно число от 0 до 100 (целое или десятичное), "
            "которое показывает вероятность, что это один и тот же предмет."
        )
    }
    user_message = {
        "role": "user",
        "content": (
            f"Описание потерянного предмета:\n{lost_text}\n\n"
            f"Описание найденного предмета:\n{found_text}\n\n"
            "Насколько они похожи? Верни число от 0 до 100."
        )
    }
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # или "gpt-4", если у вас есть доступ
        messages=[system_message, user_message],
        max_tokens=10,  # просим очень короткий ответ
        temperature=0.0,  # чтобы ChatGPT отвечал более детерминированно
    )
    # Парсим ответ
    reply_text = response["choices"][0]["message"]["content"].strip()

    # Попробуем извлечь число. Может быть "90", "85.5", "  78% " и т.п.
    # На всякий случай уберём % при парсинге.
    reply_text = reply_text.replace("%", "").strip()

    try:
        score = float(reply_text)
    except ValueError:
        # Если ChatGPT не вернул число, считаем схожесть 0
        score = 0.0

    # Ограничим диапазон [0..100]
    score = max(0.0, min(100.0, score))
    return score
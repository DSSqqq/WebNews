from django import template

register = template.Library()

CENSORED_WORDS = {"редиски", "дурак", "идиот"}  # Список нежелательных слов


@register.filter(name="censor")
def censor(value):
    if not isinstance(value, str):
        return value

    words = value.split()
    censored_text = []

    for word in words:
        lower_word = word.lower()  # Приводим к нижнему регистру для сравнения
        clean_word = word  # Исходное слово

        for bad_word in CENSORED_WORDS:
            if bad_word in lower_word:  # Проверяем, есть ли запрещённое слово
                clean_word = word[0] + "*" * (len(word) - 1)  # Заменяем всё, кроме первой буквы

        censored_text.append(clean_word)

    return " ".join(censored_text)
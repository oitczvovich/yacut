import random
from string import ascii_letters, digits

from .models import URLMap

SYMBOLS_CHOICE = list(ascii_letters + digits)


def get_unique_short_id():
    """
    Генератор случайных буквенночисловых значений.
    от A-Za-z0-9, ограничение в 6 символов.
    """
    combined_list = SYMBOLS_CHOICE
    return "".join(random.sample(combined_list, 6))


def check_unique_short_url(custom_id):
    """
    Проверка наличия в БД короткой ссылки.
    """
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None


def check_symbols(custom_id):
    """
    Валидация символов в короткой ссылке.
    """
    for elem in custom_id:
        if elem not in SYMBOLS_CHOICE:
            return False
    return True

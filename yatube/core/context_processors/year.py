import datetime
from typing import Dict

from django.http import HttpRequest


def year(unused: HttpRequest) -> Dict[str, int]:
    """Добавляет переменную с текущим годом.

    Args:
        unused: Объект запроса.

    Returns:
        Текущий год на все страницы в переменную {{ year }}.
    """
    del unused
    return {
        'year': datetime.datetime.now().year,
    }

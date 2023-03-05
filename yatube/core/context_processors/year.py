import datetime as dt
from typing import Dict

from django.http import HttpRequest


def year(request: HttpRequest) -> Dict[str, int]:
    """Добавляет переменную с текущим годом.

    Args:
        request: Объект запроса.

    Returns:
        Текущий год на все страницы в переменную {{ year }}.
    """
    del request
    return {
        'year': dt.datetime.now().year,
    }

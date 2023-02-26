from django.conf import settings
from django.core.paginator import Page, Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest


def paginate(
    request: HttpRequest,
    queryset: QuerySet,
    per_page: int = settings.NUM_OBJECTS,
) -> Page:
    """Список материалов сайта разбивает постранично.

    Args:
        request: Объект запроса.
        queryset: QuerySet, который необходимо разбить на страницы.
        per_page: Максимальное количество элементов для включения на страницу.

    Returns:
        Объект Page.
    """
    return Paginator(queryset, per_page).get_page(request.GET.get('page'))


def cut_string(field: str, cut_out: int = settings.CUT_OUTPUT) -> str:
    """Обрезает строку, если оно больше заданной длины.

    Args:
        field: Текст строки.
        cut_out: Длина строки.

    Returns:
        Текст строки с добавлением многоточия, если оно больше заданной длины.
    """
    return field[:cut_out] + '…' if len(field) > cut_out else field

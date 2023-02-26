from django import forms, template
from django.utils.safestring import SafeText

register = template.Library()


@register.filter
def addclass(field: forms.BoundField, css: str) -> SafeText:
    """Добавляет CSS-класс к тегу шаблона.

    Args:
        field: Поле формы, к которому необходимо добавить атрибут.
        css: Название атрибута, который необходимо добавить к тегу.

    Returns:
        Атрибут CSS-класс.
    """
    return field.as_widget(attrs={'class': css})

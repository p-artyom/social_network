from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def image(name: str = 'small.gif') -> SimpleUploadedFile:
    """Генерирует изображение для тестов.

    Args:
        name: Название генерируемого изображения.

    Returns:
        Простое представление файла, которое имеет только содержимое,
        размер и имя.
    """
    content = BytesIO()
    img = Image.new('RGBA', size=(1, 1), color=(155, 0, 0))
    img.save(content, 'gif')
    content.seek(0)
    return SimpleUploadedFile(
        name=name,
        content=content.getvalue(),
        content_type='image/gif',
    )

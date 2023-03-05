from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def image(name: str = 'small.gif') -> SimpleUploadedFile:
    """Генерирует изображение для тестов."""
    content = BytesIO()
    img = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    img.save(content, 'png')
    content.seek(0)
    return SimpleUploadedFile(
        name=name,
        content=content.getvalue(),
        content_type='image/gif',
    )

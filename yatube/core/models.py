from behaviors.behaviors import Timestamped
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DefaultModel(models.Model):
    text = models.TextField('текст', help_text='Введите текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )

    class Meta:
        abstract = True


class TimestampedModel(DefaultModel, Timestamped):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('created').verbose_name = 'дата публикации'

    class Meta:
        abstract = True
        ordering = ('-created',)

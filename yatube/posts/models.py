from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel
from core.utils import cut_string

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'имя',
        max_length=200,
        help_text='Введите имя группы',
    )
    slug = models.SlugField(
        'адрес',
        unique=True,
        help_text='Введите адрес группы',
    )
    description = models.TextField(
        'описание',
        help_text='Введите описание группы',
    )

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self) -> str:
        return cut_string(self.title)


class Post(CreatedModel):
    text = models.TextField('текст', help_text='Введите текст поста')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name='сообщество',
        blank=True,
        null=True,
        help_text='Группа, к которой будет относиться пост',
    )
    image = models.ImageField('картинка', upload_to='posts/', blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        default_related_name = 'posts'

    def __str__(self) -> str:
        return cut_string(self.text)


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    text = models.TextField('текст', help_text='Введите комментарий')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'

    def __str__(self) -> str:
        return cut_string(self.text)

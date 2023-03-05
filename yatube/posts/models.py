from django.contrib.auth import get_user_model
from django.db import models

from core.models import TimestampedModel
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


class Post(TimestampedModel):
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name='сообщество',
        blank=True,
        null=True,
        help_text='Группа, к которой будет относиться пост',
    )
    image = models.ImageField('картинка', upload_to='posts/', blank=True)

    class Meta(TimestampedModel.Meta):
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        default_related_name = 'posts'

    def __str__(self) -> str:
        return cut_string(self.text)


class Comment(TimestampedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='пост',
    )

    class Meta(TimestampedModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'

    def __str__(self) -> str:
        return cut_string(self.text)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self) -> str:
        return f'`{self.user}` подписался на `{self.author}`'

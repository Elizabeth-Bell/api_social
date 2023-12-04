from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(verbose_name='Дата создания',
                                   auto_now_add=True)

    class Meta:
        abstract = True


class Group(models.Model):
    """Модель группы."""
    title = models.CharField(verbose_name='Заголовок',
                             max_length=200)
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True)
    description = models.TextField(verbose_name='Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(CreatedModel):
    """Модель поста."""
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Введите текст поста')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,
        verbose_name='Картинка')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True,
                              verbose_name='Группа',
                              help_text='Группа, '
                                        'к которой будет относиться пост'
                              )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    """Модель комментария."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Кто подписывается')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following',
                                  verbose_name='На кого вы подписываетесь')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} {self.following}'

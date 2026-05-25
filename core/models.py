from django.db import models


class FeedbackMessage(models.Model):
    """Сообщения через форму обратной связи на странице контактов."""

    name = models.CharField('Имя', max_length=80)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    subject = models.CharField('Тема', max_length=150)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Сообщение от пользователя'
        verbose_name_plural = 'Сообщения от пользователей'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.subject} от {self.name}'


class SiteReview(models.Model):
    """Отзыв о сервисе DjanCar (на главной странице)."""

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             related_name='site_reviews', verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    text = models.TextField('Текст отзыва')
    is_published = models.BooleanField('Опубликован', default=True,
                                       help_text='Снимите галочку, чтобы скрыть отзыв с главной')
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв о сервисе'
        verbose_name_plural = 'Отзывы о сервисе (главная)'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Отзыв {self.user} ({self.rating}★)'

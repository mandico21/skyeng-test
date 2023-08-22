from datetime import datetime

from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import UserABC


class TimedBaseModel(models.Model):
    """Основная модель с датой"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата последнего обновления',
        auto_now=True
    )


def rename_file(instance: 'FileUpload', filename: str) -> str:
    today = datetime.now()
    return (f'documents/{today.year}-{today.month}/{today.day}/'
            f'{today.hour}{today.minute}{today.second}_'
            f'{instance.user.username}__{filename}')


class FileUpload(TimedBaseModel):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    class StatusChoice(models.TextChoices):
        NEW = 'new', 'Новый'
        OVERWRITTEN = 'overwritten', 'Перезаписан'
        VERIFIED = 'verified', 'Проверен'
        DELETED = 'del', 'Удален'

    user = models.ForeignKey(
        UserABC,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='users',
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=rename_file,
        validators=[FileExtensionValidator(['py'])],
        help_text='Поддерживаемый формат: .py'
    )
    filename = models.CharField(
        verbose_name='Название файла',
        max_length=64,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=15,
        choices=StatusChoice.choices,
        default=StatusChoice.NEW,
    )
    is_deleted = models.BooleanField(
        verbose_name='Удален',
        default=False,
    )
    uploaded_at = models.DateTimeField(
        verbose_name='Дата загрузки',
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f'{self.user} - {self.filename}'


class FileReport(TimedBaseModel):
    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    file = models.ForeignKey(
        FileUpload,
        verbose_name='Файл',
        on_delete=models.PROTECT,
        related_name='file_reports',
    )
    result = models.JSONField(
        verbose_name='Результат проверки',
    )
    verification_at = models.DateTimeField(
        verbose_name='Дата проверки',
        auto_now_add=True,
    )
    is_notified = models.BooleanField(
        verbose_name='Письмо отправлено пользователю',
        default=False,
    )

    def __str__(self) -> str:
        return f'{self.file} - {self.is_notified}'

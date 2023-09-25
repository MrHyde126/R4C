from django.db import models


class Robot(models.Model):
    serial = models.CharField(
        'Серийный номер', max_length=5, blank=False, null=False
    )
    model = models.CharField('Модель', max_length=2, blank=False, null=False)
    version = models.CharField('Версия', max_length=2, blank=False, null=False)
    created = models.DateTimeField(
        'Дата и время создания', blank=False, null=False
    )

    class Meta:
        verbose_name = 'Робот'
        verbose_name_plural = 'Роботы'
        ordering = ('serial',)

    def __str__(self):
        return self.serial

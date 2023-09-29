from django.db import models


class Customer(models.Model):
    email = models.EmailField(
        max_length=255, blank=False, null=False, unique=True
    )

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ('email',)

    def __str__(self):
        return self.email

from django.db import models

from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='Покупатель'
    )
    robot_serial = models.CharField(
        'Серийный номер робота', max_length=5, blank=False, null=False
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('customer',)

    def __str__(self):
        return f'{self.customer.email} заказал {self.robot_serial}'

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot

waiting_emails = {}


def add_to_waiting(serial, email):
    if serial in waiting_emails:
        if email not in waiting_emails[serial]:
            waiting_emails[serial].append(email)
        return
    else:
        waiting_emails[serial] = [email]


@receiver(post_save, sender=Robot)
def notify_customer(instance, **kwargs):
    serial = instance.serial
    model = instance.model
    version = instance.version
    if Robot.objects.filter(serial=serial).exists():
        if serial in waiting_emails:
            for email in waiting_emails[serial]:
                send_mail(
                    'Уведомление о наличии робота',
                    (
                        'Добрый день!\nНедавно вы интересовались нашим роботом'
                        f' модели {model}, версии {version}.\nЭтот робот теперь'
                        ' в наличии. Если вам подходит этот вариант -'
                        ' пожалуйста, свяжитесь с нами'
                    ),
                    'r4c@email.com',
                    [email],
                )
            del waiting_emails[serial]

import re
from http import HTTPStatus

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from customers.models import Customer
from robots.models import Robot
from .models import Order
from .signals import add_to_waiting, notify_customer


@csrf_exempt
def order_robot(request):
    if request.method == 'POST':
        if set(request.POST) < {'email', 'serial'}:
            return HttpResponse(
                'В запросе должны быть ключи "email" и "serial".',
                status=HTTPStatus.BAD_REQUEST,
            )
        email = request.POST['email'].lower()
        serial = request.POST['serial'].upper()
        if not (email and serial):
            return HttpResponse(
                'Поля "email" и "serial" не долны быть пустыми.',
                status=HTTPStatus.BAD_REQUEST,
            )
        customer = Customer.objects.filter(email=email)
        if not customer.exists():
            return HttpResponse(
                (
                    f'Покупатель с электронной почтой `{email}` не'
                    ' зарегистрирован.'
                ),
                status=HTTPStatus.BAD_REQUEST,
            )
        if not Robot.objects.filter(serial=serial).exists():
            pattern = r'^[0-9A-Z]{2}-[0-9A-Z]{1,2}$'
            if not re.match(pattern, serial):
                return HttpResponse(
                    f'`{serial}` не соответствует паттерну `{pattern}`.',
                    status=HTTPStatus.BAD_REQUEST,
                )
            add_to_waiting(serial, email)
            notify_customer(Robot(serial=serial))
            return HttpResponse(
                'Вам придет уведомление на почту, когда робот будет в наличии.'
            )
        Order.objects.create(customer=customer.first(), robot_serial=serial)
        return HttpResponse('Заказ оформлен!', status=HTTPStatus.CREATED)
    return HttpResponse(
        'Этот эндпоинт принимает только POST-запросы.',
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )

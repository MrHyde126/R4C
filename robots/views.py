from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Robot


@csrf_exempt
def produce_robot(request):
    if request.POST:
        if set(request.POST) < {'model', 'version', 'created'}:
            return HttpResponse(
                'В запросе должны быть ключи "model", "version" и "created".'
            )
        model = request.POST['model']
        version = request.POST['version']
        created = request.POST['created']
        if not all({model, version, created}):
            return HttpResponse(
                'Поля "model", "version" и "created" не долны быть пустыми.'
            )
        if not Robot.objects.filter(model=model).exists():
            return HttpResponse('Робота такой модели не существует.')
        try:
            Robot.objects.create(
                model=model,
                version=version,
                created=created,
                serial=f'{model}-{version}',
            )
        except ValidationError as e:
            return HttpResponse(e)
        return HttpResponse('Робот создан!')
    else:
        raise PermissionDenied

from datetime import datetime, timedelta
from http import HTTPStatus

import pandas
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Robot


@csrf_exempt
def produce_robot(request):
    if request.POST:
        if set(request.POST) < {'model', 'version', 'created'}:
            return HttpResponse(
                'В запросе должны быть ключи "model", "version" и "created".',
                status=HTTPStatus.BAD_REQUEST,
            )
        model = request.POST['model'].upper()
        version = request.POST['version'].upper()
        created = request.POST['created']
        if not all({model, version, created}):
            return HttpResponse(
                'Поля "model", "version" и "created" не долны быть пустыми.',
                status=HTTPStatus.BAD_REQUEST,
            )
        if not Robot.objects.filter(model=model, version=version).exists():
            return HttpResponse(
                'Робота такой модели и версии не существует.',
                status=HTTPStatus.BAD_REQUEST,
            )
        try:
            datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
            if created > datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                return HttpResponse(
                    'Дата создания не может быть в будущем.',
                    status=HTTPStatus.BAD_REQUEST,
                )
            Robot.objects.create(
                model=model,
                version=version,
                created=created,
                serial=f'{model}-{version}',
            )
        except (ValidationError, ValueError) as e:
            return HttpResponse(e, status=HTTPStatus.BAD_REQUEST)
        return HttpResponse('Робот создан!', status=HTTPStatus.CREATED)
    return HttpResponse(
        'Этот эндпоинт принимает только POST-запросы.',
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )


@csrf_exempt
def generate_report(request):
    if request.method == 'GET':
        current_time = datetime.now()
        filename = (
            f'./reports/production_report_{datetime.date(current_time)}.xlsx'
        )
        writer = pandas.ExcelWriter(filename, engine='xlsxwriter')
        robot_models = [m[0] for m in set(Robot.objects.values_list('model'))]
        robot_models.sort()
        for model in robot_models:
            robot_versions = [
                v[0]
                for v in set(
                    Robot.objects.filter(model=model).values_list('version'),
                )
            ]
            robot_versions.sort()
            sheet = pandas.DataFrame(
                {
                    'Модель': [model] * len(robot_versions),
                    'Версия': robot_versions,
                    'Количество за неделю': [
                        Robot.objects.filter(
                            model=model,
                            version=version,
                            created__gte=(current_time - timedelta(days=7)),
                        ).count()
                        for version in robot_versions
                    ],
                }
            )
            sheet.to_excel(writer, sheet_name=model, index=False)
        writer.close()
        return FileResponse(open(filename, 'rb'), as_attachment=True)
    return HttpResponse(
        'Этот эндпоинт принимает только GET-запросы.',
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )

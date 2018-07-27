import logging

from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


# Create your views here.


def user_info(request):
    return JsonResponse(dict(
        id=1,
        username='test'
    ), safe=False)


def application_index(request):
    """
    List frontend applications
    :param request:
    :return: JSON list of application infos.
    """
    return JsonResponse([
        dict(id=1, name="Report builder", url="/my-app/"),
        dict(id=2, name="Web scraper", url="/my-app/"),
        dict(id=3, name="Wavemeter", url="/my-app/")
    ], safe=False)


def index(request):
    current_app = apps.get_app_config(app_label=settings.PRESENTATION['ROOT_APP'])
    logger.info('Render shell "index.html" ...')
    print(request)
    return render(
        request=request,
        template_name='hydra_presentation/spa.html',
        context=dict(
            application=current_app.application
        ),
    )


def application(request):
    current_app = apps.get_app_config(app_label=settings.PRESENTATION['ROOT_APP'])
    logger.info('Render application "my-app.html" ...')
    return render(
        request=request,
        template_name='hydra_presentation/application.html',
        context=dict(module=current_app.application),
    )


def page(request, path):
    current_app = apps.get_app_config(app_label=settings.PRESENTATION['ROOT_APP'])
    logger.info('Render page ...')
    return render(
        request=request,
        template_name='hydra_presentation/page.html',
        context=dict(module=current_app.application.get_page(path)),
    )


def form(request):
    logger.info('Render form ...')
    return render(
        request=request,
        template_name='hydra_presentation/form.html'
    )

from django.apps import apps
from django.conf import settings
from django.shortcuts import render


# Create your views here.


def user_info(request):
    return render(
        request=request,
        content_type='application/json',
        context=dict(
            id=1,
            username='test'
        )
    )


def index(request):
    current_app = apps.get_app_config(app_label=settings.PRESENTATION['ROOT_APP'])
    return render(
        request=request,
        template_name='hydra_presentation/spa.html',
        context=dict(application=current_app.application),
    )


def application(request):
    current_app = apps.get_app_config(app_label=settings.PRESENTATION['ROOT_APP'])
    return render(
        request=request,
        template_name='hydra_presentation/application.html',
        context=dict(module=current_app.application),
    )


def page(request):
    return render(
        request=request,
        template_name='hydra_presentation/page.html'
    )


def form(request):
    return render(
        request=request,
        template_name='hydra_presentation/form.html'
    )

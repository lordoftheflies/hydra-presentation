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
    return render(
        request=request,
        template_name='hydra_presentation/spa.html',
        context={
            'main_title': 'Maintitle'
        }
    )


def application(request):
    return render(
        request=request,
        template_name='hydra_presentation/application.html'
    )


def page(request):
    return render(
        request=request,
        template_name='hydra_presentation/page.html'
    )

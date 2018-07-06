"""hydra_presentation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^service-worker.js$', serve, kwargs={
        'path': 'service-worker.js',
        'document_root': settings.STATIC_ROOT
    }, name='service-worker'),

    url(r'^.*$', TemplateView.as_view(template_name="hydra_presentation/spa.html"), name='index'),

    url(r'^src/my-app.html', views.application, name='application'),
    url(r'^src/my-(?P<path>.html)$', views.page, name='page'),

    url(r'^src/(?P<path>/.html)$', serve),

    path('user-info/', views.user_info, name='user_info')
    # path(settings.POLYMER_APPLICATION_ROOT, admin.site.urls),
]

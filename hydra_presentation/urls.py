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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.views.static import serve

from hydra_presentation.views import index

urlpatterns = [
    url(r'^service-worker.js$', serve, kwargs={
        'path': 'service-worker.js'
    }, name='service-worker'),

    url(r'^src/(?P<path>/.html)$', serve),

    url(r'^.*$', TemplateView.as_view(template_name="hydra_presentation/spa.html"), name='index'),



    # path(settings.POLYMER_APPLICATION_ROOT, admin.site.urls),
]

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
from django.views.static import serve

from . import views

urlpatterns = [
    # Static service worker from static files
    url(r'^service-worker.js$', serve, kwargs={
        'path': 'service-worker.js',
        'document_root': settings.STATIC_ROOT
    }, name='service_worker'),
    # Dynamic Polymer application view
    url(r'^src/my-app.html', views.application, name='application'),
    # Dynamic Polymer page view
    path(r'page/my-<str:path>.html', views.page, name='page'),
    # Static Polymer application source files
    url(r'^src/(?P<path>.*)$', serve, kwargs={
        'document_root': settings.STATIC_ROOT + '/src'
    }, name='source'),
    # Dynamic Polymer application shell view
    url(r'^index.html', views.index, name='index'),
    # API: User info
    url(r'^user-info/$', views.user_info, name='user_info'),
    # API: Application entry point list
    url(r'^applications/$', views.application_index, name='application_index'),

    # url(r'^(?P<path>)/(?P<path>.html)$', views.page, name='bower'),
    # path(r'index.html', views.page, name='index'),
    # url(r'my-app/.*$', views.index, name='index'),
    # url(r'', RedirectView.as_view(url='index.html', permanent=True), name='home'),
    # path(settings.POLYMER_APPLICATION_ROOT, admin.site.urls),
]

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view

allauth_schema_view = get_swagger_view(title='Allauth API', url=r'/account/')


urlpatterns = [


    path('admin/', admin.site.urls),

    url(r'^account/', include('allauth.urls')),
    # url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^api/allauth/$', allauth_schema_view),

    path(r'my-app/', include('hydra_presentation.urls')),
    url(r'', RedirectView.as_view(url='my-app/', permanent=True), name='home'),
]

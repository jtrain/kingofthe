"""kingofthe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from main import views as main_views

urlpatterns = [
    url(r'^admin/', TemplateView.as_view(template_name='admin.html'),
        name='admin'),
    url(r'^$', main_views.IndexView.as_view(template_name='index.html'),
        name='index'), 
    url(r'^toggle$', main_views.ToggleCacheView.as_view(), name='toggle'), 
    url(r'^api/checkin$', login_required(main_views.CheckinPingView.as_view()),
        name='checkin'),

    # fake accounts login sets up user account with "GET"
    url(r'^accounts/login/$', main_views.NewAccount.as_view(),
        name="accts_login"),

]

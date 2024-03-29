from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('json', views.json, name='json'),
    path('login', views.login, name='login'),
    path('upload', views.upload, name='upload')
]
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('regisconfirmation', views.regisconfirmation, name='regisconfirmation'),
    path('admin', views.admin, name='admin'),
    path('addpromotion', views.addpromotion, name='addpromotion'),
    path('managemovie', views.managemovie, name='managemovie'),
]
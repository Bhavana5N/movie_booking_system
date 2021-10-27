from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    #path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('regisconfirmation', views.regisconfirmation, name='regisconfirmation'),
    path('admin', views.admin, name='admin'),
    path('addpromotion', views.addpromotion, name='addpromotion'),
    path('managemovie', views.managemovie, name='managemovie'),
    path('checkout', views.checkout, name='checkout'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('home', views.home, name='home'),
    path('moviedetails', views.moviedetails, name='moviedetails'),
    path('seats', views.seats, name='seats'),
    path('fullcalendar', views.fullcalendar, name='fullcalendar'),
    path('orderSummary', views.orderSummary, name='orderSummary'),
    path('orderHistory', views.orderHistory, name='orderHistory'),
    path('orderconfirmation', views.orderconfirmation, name='orderconfirmation'),
    path('summary', views.summary, name='summary'),
    path('logout', views.logout, name='logout'),
]

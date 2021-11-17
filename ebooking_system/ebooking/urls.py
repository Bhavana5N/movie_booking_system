"""ebooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('home.urls')),
    path('', views.index, name="index"),
    path('login/',  views.login_user, name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('forgot-password/', views.forgot_password_view, name='forgot'),
    path('reset-password/', views.forgot_password_validation, name='rget'),
    path('admin', views.admin, name='admin'),
    path('edit_profile', views.edit_profile, name='edit'),
    path('registration', views.registration, name="registration"),
    path('regisconfirmation', views.regisconfirmation, name='regisconfirmation'),
    path('edit_card', views.edit_card, name='editcard'),
    path('changepassword', PasswordChangeView.as_view(
            template_name='change_password.html',success_url="login"),
        name='changepassword'),
    path('orderSummary', views.orderSummary, name="orderSummary"),
    path('addpromotion', views.addpromotion, name='addpromotion'),
    path('addmovie', views.addmovie, name='addmovie'),
    path('checkout', views.checkout, name='checkout'),
    path('moviedetails', views.moviedetails, name='moviedetails'),
    path('seats', views.seats, name='seats'),
    path('fullcalendar', views.fullcalendar, name='fullcalendar'),
    path('orderconfirmation', views.orderconfirmation, name='orderconfirmation'),
    path('summary', views.summary, name='summary'),
    path('searchResults', views.searchResults, name='searchResults'),
    path('categories', views.categories, name='categories'),
    path('schedule', views.schedule, name='schedule'),
    #path('schedulemovie', views.schedulemovie, name='schedulemovie'),
    path('bookmovie/', views.book_movie, name='bookmovie'),
    path('base', views.base, name='base')

]


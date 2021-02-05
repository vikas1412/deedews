from django.urls import path, include
from . import views

urlpatterns = [
    path('user-account/login', views.login, name='login'),
    path('user-account/signup', views.signup, name='signup'),
    path('user-account/profile', views.profile, name='profile'),
    path('user-account/logout', views.logout, name='logout'),
]

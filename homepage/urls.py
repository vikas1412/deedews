from django.urls import path, include
from . import views

urlpatterns = [
path('contact-us', views.contact, name="contact"),
path('about-us', views.about, name="about"),
path('teams', views.teams, name="teams"),
]

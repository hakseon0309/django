from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home1"),
    # pk = primary key
    path("post/<str:pk>/", views.post, name="post"),
]

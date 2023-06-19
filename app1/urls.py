from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # pk = primary key
    path("room/<str:pk>/", views.content, name="contents"),
]

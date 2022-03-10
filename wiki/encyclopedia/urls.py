from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.title, name="by_title"),
]

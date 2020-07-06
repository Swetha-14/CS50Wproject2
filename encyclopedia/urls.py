from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.index, name="index"),
    path("search", views.search, name="search"),
    path("", views.random_page, name="random"),
    path("new_entry", views.create_page, name="create"),
    path("<str:title>", views.edit_page, name="edit"),
    path("wiki/<str:title>", views.load_page, name="load_page")
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("movie/<int:pk>/", views.movie_detail, name="movie-detail"),
    path("films/", views.all_films, name="AllFilms_page"),
    path("films/filter/<str:filter_type>/<str:filter_value>/", views.filtered_films, name="filtered-films"),
    path("serials/", views.all_serials, name="all-serials"),
    path("serial/<int:pk>/", views.serial_detail, name="serial-detail"),
]
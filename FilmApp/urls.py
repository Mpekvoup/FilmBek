from django.urls import path
from . import views
from .views import search_suggestions

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("movie/<int:pk>/", views.movie_detail, name="movie-detail"),
    path("films/", views.all_films, name="AllFilms_page"),
    path(
        "films/filter/<str:filter_type>/<str:filter_value>/",
        views.filtered_films,
        name="filtered-films",
    ),
    path("serials/", views.all_serials, name="AllSerials_page"),
    path("serial/<int:pk>/", views.serial_detail, name="serial-detail"),
    path(
        "serials/filter/<str:filter_type>/<str:filter_value>/",
        views.filtered_serials,
        name="filtered_serials",
    ),
    path("auth/", views.login_page, name="login_page"),
    path("news/", views.news_list, name="news-list"),
    path("news/<int:pk>/", views.news_detail, name="news_detail"),
    path("search/", views.search_films, name="search"),
    path("search-suggestions/", search_suggestions, name="search-suggestions"), 
    path("settings/", views.settings_page, name="settings"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile_page, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("warning/", views.warning_view, name="warning"),
    path("bout_page/", views.bout_page, name="bout" ),
]
from django.shortcuts import get_object_or_404, redirect, render
from .models import Country, Film, Genre, Serial, News
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect

def main_page(request):
    query = request.GET.get("q", " ")

    films = (
        Film.objects.order_by("?")
        .select_related("rating", "age_rating")
        .prefetch_related("genres", "countries")
    ).distinct()

    if query:
        films = films.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(genres__name__icontains=query)
        ).distinct()

    news_list = News.objects.all().order_by("?")

    context = {
        "films": films,
        "news_list": news_list,
        "query": query,
    }
    return render(request, "MainPage.html", context)


def movie_detail(request, pk):
    film = get_object_or_404(
        Film.objects.select_related("rating", "age_rating").prefetch_related(
            "genres", "countries"
        ),
        pk=pk,
    )
    return render(request, "MovieDetail.html", {"film": film})


def all_films(request):
    films = (
        Film.objects.order_by("?")
        .select_related("rating", "age_rating")
        .prefetch_related("genres", "countries")
    )
    return render(request, "AllFilms.html", {"films": films})


def filtered_films(request, filter_type=None, filter_value=None):
    films = (
        Film.objects.all()
        .select_related("rating", "age_rating", "content_type")
        .prefetch_related("genres", "countries")
    )

    if filter_type == "rating":
        if filter_value == "9-10":
            films = films.filter(rating__value__gte=9, rating__value__lt=10.1)
        elif filter_value == "8-9":
            films = films.filter(rating__value__gte=8, rating__value__lt=9)
        elif filter_value == "7-8":
            films = films.filter(rating__value__gte=7, rating__value__lt=8)
        elif filter_value == "6-7":
            films = films.filter(rating__value__gte=6, rating__value__lt=7)
        elif filter_value == "5-6":
            films = films.filter(rating__value__gte=5, rating__value__lt=6)
        elif filter_value == "below-5":
            films = films.filter(rating__value__lt=5)

    elif filter_type == "genre":
        if filter_value and filter_value.lower() != "all":
            films = films.filter(genres__slug__iexact=filter_value)

    elif filter_type == "year":
        if filter_value == "before-1990":
            films = films.filter(year__lt=1990)
        elif filter_value == "1990-2000":
            films = films.filter(year__gte=1990, year__lt=2000)
        elif filter_value == "2000-2010":
            films = films.filter(year__gte=2000, year__lt=2010)
        elif filter_value == "2010-2020":
            films = films.filter(year__gte=2010, year__lt=2020)
        elif filter_value == "2020-2025":
            films = films.filter(year__gte=2020, year__lte=2025)
    elif filter_type == "country":
        if filter_value and filter_value.lower() != "all":
            films = films.filter(countries__slug__iexact=filter_value)
    elif filter_type == "age-rating":
        if filter_value and filter_value.lower() != "all":
            films = films.filter(age_rating__slug__iexact=filter_value)
    elif filter_type == "content-type":
        if filter_value and filter_value.lower() != "all":
            films = films.filter(content_type__slug__iexact=filter_value)
    context = {
        "films": films,
        "picked_filter": filter_value,
        "filter_type": filter_type,
    }
    return render(request, "AllFilms.html", context)


def serial_detail(request, pk):
    serial = get_object_or_404(
        Serial.objects.select_related("rating", "age_rating").prefetch_related(
            "genres", "countries"
        ),
        pk=pk,
    )
    return render(request, "SerialDetail.html", {"serial": serial})


def all_serials(request):
    serials = Serial.objects.order_by("?")
    return render(request, "AllSerial.html", {"serials": serials})


def filtered_serials(request, filter_type=None, filter_value=None):
    serials = (
        Serial.objects.all()
        .select_related("rating", "age_rating", "content_type")
        .prefetch_related("genres", "countries")
    )
    if filter_type == "rating":
        if filter_value == "9-10":
            serials = serials.filter(rating__value__gte=9, rating__value__lt=10.1)
        elif filter_value == "8-9":
            serials = serials.filter(rating__value__gte=8, rating__value__lt=9)
        elif filter_value == "7-8":
            serials = serials.filter(rating__value__gte=7, rating__value__lt=8)
        elif filter_value == "6-7":
            serials = serials.filter(rating__value__gte=6, rating__value__lt=7)
        elif filter_value == "5-6":
            serials = serials.filter(rating__value__gte=5, rating__value__lt=6)
        elif filter_value == "below-5":
            serials = serials.filter(rating__value__lt=5)
    elif filter_type == "genre":
        if filter_value and filter_value.lower() != "all":
            serials = serials.filter(genres__slug__iexact=filter_value)
    elif filter_type == "year":
        if filter_value == "before-1990":
            serials = serials.filter(year__lt=1990)
        elif filter_value == "1990-2000":
            serials = serials.filter(year__gte=1990, year__lt=2000)
        elif filter_value == "2000-2010":
            serials = serials.filter(year__gte=2000, year__lt=2010)
        elif filter_value == "2010-2020":
            serials = serials.filter(year__gte=2010, year__lt=2020)
        elif filter_value == "2020-2025":
            serials = serials.filter(year__gte=2020, year__lte=2025)
    elif filter_type == "country":
        if filter_value and filter_value.lower() != "all":
            serials = serials.filter(countries__slug__iexact=filter_value)
    elif filter_type == "age-rating":
        if filter_value and filter_value.lower() != "all":
            serials = serials.filter(age_rating__slug__iexact=filter_value)
    elif filter_type == "content-type":
        if filter_value and filter_value.lower() != "all":
            serials = serials.filter(content_type__slug__iexact=filter_value)
    context = {
        "serials": serials,
        "picked_filter": filter_value,
        "filter_type": filter_type,
    }
    return render(request, "AllSerial.html", context)


def login_page(request):
    return render(request, "auth.html")


def news_list(request):
    news_list = News.objects.all().order_by("-published_date")
    return render(request, "AllNews.html", {"news_list": news_list})


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)

    next_news = (
        News.objects.filter(published_date__lt=news.published_date)
        .order_by("-published_date")
        .first()
    )

    prev_news = (
        News.objects.filter(published_date__gt=news.published_date)
        .order_by("published_date")
        .first()
    )

    context = {
        "news": news,
        "next_news": next_news,
        "prev_news": prev_news,
    }

    return render(request, "NewsDetail.html", context)


def search_films(request):
    query = request.GET.get("q", "")

    films = (
        Film.objects.all()
        .select_related("rating", "age_rating")
        .prefetch_related("genres", "countries")
    )

    serials = (
        Serial.objects.all()
        .select_related("rating", "age_rating")
        .prefetch_related("genres", "countries")
    )

    if query:
        films = films.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(genres__name__icontains=query)
        ).distinct()

        serials = serials.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(genres__name__icontains=query)
        ).distinct()

    context = {
        "films": films,
        "serials": serials,
        "query": query,
    }
    return render(request, "search_results.html", context)


def search_suggestions(request):
    query = request.GET.get("q", "").strip()
    suggestions = []
    if query:
        films = Film.objects.filter(Q(name__icontains=query))[:3]
        for film in films:
            suggestions.append(
                {
                    "title": film.name,
                    "poster": film.image_url if film.image_url else "",
                    "type": "Фильм",
                    "url": f"/movie/{film.pk}/",
                }
            )

        serials = Serial.objects.filter(Q(name__icontains=query))[:2]
        for serial in serials:
            suggestions.append(
                {
                    "title": serial.name,
                    "poster": serial.image_url if serial.image_url else "",
                    "type": "Сериал",
                    "url": f"/serial/{serial.pk}/",
                }
            )

    return JsonResponse({"suggestions": suggestions})


def settings_page(request):

    return render(request, "settings.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("main_page")
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    return render(request, "auth.html")


def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        pwd1 = request.POST.get("password1", "")
        pwd2 = request.POST.get("password2", "")

        if not all([full_name, username, email, pwd1, pwd2]):
            messages.error(request, "Все поля обязательны к заполнению")
            return render(request, "auth.html")

        if pwd1 != pwd2:
            messages.error(request, "Пароли не совпадают")
            return render(request, "auth.html")

        try:
            new_user = User.objects.create_user(
                username=username, password=pwd1, email=email, first_name=full_name
            )
        except IntegrityError:
            messages.error(request, "Пользователь с таким именем уже существует")
            return render(request, "auth.html")

        auth_login(request, new_user)
        messages.success(request, "Регистрация прошла успешно!")
        return redirect("main_page")

    return render(request, "auth.html")


def get_random_films():
    return (
        Film.objects.order_by("?")
        .select_related("rating")
        .prefetch_related("genres")[:4]
    )


def profile_page(request):
    random_films = get_random_films()
    return render(
        request, "profile.html", {"user": request.user, "random_films": random_films}
    )


def logout_view(request):
    logout(request)
    return redirect("main_page")


def watchlist(request):
    films = (
        Film.objects.order_by("?")
        .select_related("rating", "age_rating")
        .prefetch_related("genres", "countries")
    )

    return render(request, "watchlist.html", {"films": films})


def warning_view(request):
    return render(request, "warning.html")

def bout_page(request):
    return render(request, "bout_me.html")

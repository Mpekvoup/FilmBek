from django.shortcuts import get_object_or_404, render
from .models import Film, Serial

def main_page(request):
    films = Film.objects.all()
    new_films = Film.objects.filter(year__in=["2024", "2025"]) 
    context = {
        'films': films,
        'new_films': new_films,  
    }
    return render(request, "MainPage.html", context)

def movie_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    return render(request, 'MovieDetail.html', {'film': film})

def all_films(request):
    films = Film.objects.order_by('-id')
    return render(request, 'AllFilms.html', {"films": films})

def filtered_films(request, filter_type=None, filter_value=None):
    films = Film.objects.all()
    if filter_type == 'rating':          
        if filter_value == '9-10':
            films = films.filter(rating__value__gte=9, rating__value__lte=10)
        elif filter_value == '8-9':
            films = films.filter(rating__value__gte=8, rating__value__lte=9)
        elif filter_value == '7-8':
            films = films.filter(rating__value__gte=7, rating__value__lte=9)
        elif filter_value == '6-7':
            films = films.filter(rating__value__gte=6, rating__value__lte=7)
        elif filter_value == '5-6':
            films = films.filter(rating__value__gte=5, rating__value__lte=6)
            films = films.filter(rating__name=filter_value)
    if filter_type == 'genre':
        if filter_value in ['Боевик', 'Комедия', 'Драма', 'Фэнтези', 'Ужасы', 'Фантастика']:
            films = films.filter(genre__name=filter_value)
    if filter_type == 'country':
        if filter_value in ['США', 'Россия', 'Япония', 'Великобритания']:
            films = films.filter(country__name=filter_value)
    if filter_type == 'age-rating':
        if filter_value in ['0+', '6+', '12+', '16+','18+']:
            films = films.filter(year__name=filter_value)
    if filter_type == 'content-type':
        if filter_value in ['Фильмы', 'Сериалы', 'Аниме', 'Документальные']:
            films = films.filter(year__name=filter_value)
    context = {
        'films': films,
        'picked_filter': filter_value,
        'filter_type': filter_type,
    }

    return render(request, 'AllFilms.html', context)

    
def all_serials(request):
    serials = Serial.objects.all()
    context = {
        'serials': serials,
    }
    return render(request, "AllSerial.html", context)


def serial_detail(request, pk):
    serial = get_object_or_404(Serial, pk=pk)
    return render(request, "SerialDetail.html", {"serial": serial})
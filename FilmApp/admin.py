from django.contrib import admin
from .models import (
    Film,
    Serial,
    News,
    Genre,
    Country,
    AgeRating,
    ContentType,
    Rating,
    UserRating,
    MediaType
        
)




@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date")
    search_fields = ("title", "content")
    ordering = ("-published_date",)


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("id", "name", "slug")

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "rating_display", "created_at", "status")
    list_filter = ("genres", "countries", "age_rating", "created_at")
    search_fields = ("name", "description", "year")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("genres", "countries")
    raw_id_fields = ("rating", "age_rating")
    ordering = ("-created_at",)

    def rating_display(self, obj):
        return obj.rating.value if obj.rating else "Нет оценки"

    rating_display.short_description = "Оценка"


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "rating_display", "created_at", "status")
    list_filter = ("genres", "countries", "age_rating", "created_at")
    search_fields = ("name", "description", "year")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("genres", "countries")
    raw_id_fields = ("rating", "age_rating")
    ordering = ("-created_at",)

    def rating_display(self, obj):
        return obj.rating.value if obj.rating else "Нет оценки"

    rating_display.short_description = "Оценка"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AgeRating)
class AgeRatingAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("value", "votes")
    list_filter = ("value",)
    search_fields = ("value",)


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "content_name", "value", "created_at")
    list_filter = ("value", "created_at")
    search_fields = ("user__username",)
    raw_id_fields = ("user", "film", "serial")

    def content_name(self, obj):
        return obj.film or obj.serial or "Без привязки"

    content_name.short_description = "Контент"


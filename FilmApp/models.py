from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from pytils.translit import slugify

class Film(models.Model):
    name = models.CharField("Название фильма", max_length=255)
    description = models.TextField("Описание фильма", default="Описание отсутствует")
    status = models.CharField("Статус фильма", default="Нету статуса", max_length=255 )
    image_url = models.URLField("Вставьте изображение", max_length=500, default='', blank=True)
    rating = models.IntegerField("Оценка", default="0")
    genre = models.CharField("Жанр фильма", max_length=255,  default="")
    year = models.CharField("Год выхода фильма", max_length=255, default="")
    com = models.IntegerField("Отзывы", default="0")
    slug = models.SlugField("URL", unique=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Время создания", default=datetime.now)
    age = models.CharField("Возрастной рейтинг фильма", max_length=255, default="")
    content_type = models.CharField("Тип контента", max_length=255, default="")


    class Meta:
        verbose_name = "Список фильма"
        verbose_name_plural = "Список фильмов"

    def __str__(self):
        return f"{self.pk} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Serial(models.Model):
    name = models.CharField("Название сериалов", max_length=255)
    description = models.TextField("Описание сериала", default="Описание отсутствует")
    status = models.CharField("Статус Сериала", default="Нету статуса", max_length=255 )
    image_url = models.URLField("Вставьте изображение", max_length=500, default='', blank=True)
    rating = models.IntegerField("Оценка", default="0")
    genre = models.CharField("Жанр сериала", max_length=255,  default="")
    year = models.CharField("Год выхода сериала", max_length=255, default="")
    com = models.IntegerField("Отзывы", default="0")
    slug = models.SlugField("URL", unique=True, blank=True)  
    created_at = models.DateTimeField(verbose_name="Время создания", default=datetime.now)
    age = models.CharField("Возрастной рейтинг сериала", max_length=255, default="")
    content_type = models.CharField("Тип контента", max_length=255, default="")

    class Meta:
        verbose_name = "Список Сериала"
        verbose_name_plural = "Список Сериалов"

    def __str__(self):
        return f"{self.pk} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


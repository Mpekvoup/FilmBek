from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from pytils.translit import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


def validate_year(value):
    """
    Валидатор для поля year.
    Если нужно поддерживать диапазоны, можно оставить CharField,
    но для корректной фильтрации лучше использовать числовое поле.
    """
    cleaned_value = value.replace(" ", "").replace("–", "")
    if not cleaned_value.isdigit():
        raise ValidationError("Год должен содержать только цифры и символ '–' для диапазона (например, '2008' или '2008 – 2013').")

class BaseNamedModel(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("URL", unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Genre(BaseNamedModel):
     class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Country(BaseNamedModel):
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

class AgeRating(BaseNamedModel):
    name = models.CharField("Возрастной рейтинг", max_length=50, unique=True)

    class Meta:
        verbose_name = "Возрастной рейтинг"
        verbose_name_plural = "Возрастные рейтинги"

class MediaType(BaseNamedModel):
    class Meta:
        verbose_name = "Тип контента"
        verbose_name_plural = "Типы контента"

class Rating(models.Model):
    value = models.DecimalField(
        "Средняя оценка",
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Средняя оценка от 0 до 10"
    )
    votes = models.PositiveIntegerField(
        "Количество голосов",
        default=0,
        help_text="Общее количество голосов"
    )

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return f"{self.value}"

class Media(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", default="Описание отсутствует")
    status = models.CharField("Статус", default="Нет статуса", max_length=255)
    image_url = models.URLField(
        "Изображение",
        max_length=500,
        default='',
        blank=True,
        help_text="URL изображения постера"
    )
    rating = models.ForeignKey(
        Rating,
        verbose_name="Оценка",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_ratings"
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name="Жанры",
        blank=True,
        related_name="%(class)s_genres"
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name="Страны",
        blank=True,
        related_name="%(class)s_countries"
    )
    year = models.PositiveIntegerField(
        "Год выхода",
        validators=[MinValueValidator(1888)],  
        help_text="Укажите год выхода фильма"
    )
    slug = models.SlugField("URL", unique=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    age_rating = models.ForeignKey(
        AgeRating,
        verbose_name="Возрастной рейтинг",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_age_ratings"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk} - {self.name}"
class Film(Media):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="Тип контента",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="films"
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

class Serial(Media):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="Тип контента",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="serials"
    )

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]


class UserRating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="ratings"
    )
    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Фильм",
        related_name="user_ratings"
    )
    serial = models.ForeignKey(
        Serial,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Сериал",
        related_name="user_ratings"
    )
    value = models.PositiveIntegerField(
        "Оценка",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Оценка от 0 до 10"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Оценка пользователя"
        verbose_name_plural = "Оценки пользователей"
        unique_together = [('user', 'film'), ('user', 'serial')]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['film']),
            models.Index(fields=['serial']),
        ]

    def __str__(self):
        content = self.film or self.serial
        return f"Оценка {self.value} от {self.user} для {content}"


class News(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("URL", unique=True, blank=True)
    content = models.TextField("Содержание новости")
    image_url = models.URLField(
        "Изображение новости",
        max_length=500,
        blank=True,
        default='',
        help_text="URL изображения для новости (необязательно)"
    )
    published_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор",
        help_text="Пользователь, опубликовавший новость"
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
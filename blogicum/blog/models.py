from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    MAX_LENGTH_TITLE,
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    DEFAULT_IS_PUBLISHED,
    SLUG_HELP_TEXT,
    PUBLISHED_HELP_TEXT,
    PUB_DATE_HELP_TEXT,
    TITLE_VERBOSE,
    DESCRIPTION_VERBOSE,
    SLUG_VERBOSE,
    IS_PUBLISHED_VERBOSE,
    CREATED_AT_VERBOSE,
    NAME_VERBOSE,
    TEXT_VERBOSE,
    PUB_DATE_VERBOSE,
    AUTHOR_VERBOSE,
    LOCATION_VERBOSE,
    CATEGORY_VERBOSE,
)

User = get_user_model()


class PublishedModel(models.Model):
    """Абстрактная модель с полями для публикации."""

    is_published = models.BooleanField(
        default=DEFAULT_IS_PUBLISHED,
        verbose_name=IS_PUBLISHED_VERBOSE,
        help_text=PUBLISHED_HELP_TEXT,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=CREATED_AT_VERBOSE,
    )

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name=TITLE_VERBOSE,
    )
    description = models.TextField(
        verbose_name=DESCRIPTION_VERBOSE,
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
        verbose_name=SLUG_VERBOSE,
        help_text=SLUG_HELP_TEXT,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name=NAME_VERBOSE,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name=TITLE_VERBOSE,
    )
    text = models.TextField(verbose_name=TEXT_VERBOSE)
    pub_date = models.DateTimeField(
        verbose_name=PUB_DATE_VERBOSE,
        help_text=PUB_DATE_HELP_TEXT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=AUTHOR_VERBOSE,
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=LOCATION_VERBOSE,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=CATEGORY_VERBOSE,
        related_name='posts',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

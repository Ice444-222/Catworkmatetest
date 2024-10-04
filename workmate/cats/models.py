from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .validators import cat_validate_name, cat_validate_birth_date

CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Чёрный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный'),
)

User = get_user_model()


class Breed(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название породы"
    )
    description = models.TextField(
        max_length=254, verbose_name="Описание"
    )

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(
        max_length=100, unique=False, verbose_name="Имя котенка",
        validators=[cat_validate_name]
    )
    color = models.CharField(
        max_length=16, choices=CHOICES, verbose_name="Цвет"
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения (дд-мм-гггг)",
        help_text="Введите дату в формате дд-мм-гггг",
        validators=[cat_validate_birth_date]
    )
    description = models.TextField(
        max_length=254, verbose_name="Описание"
    )
    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, verbose_name="Порода"
    )
    author = models.ForeignKey(
        User, related_name='cats', on_delete=models.CASCADE,
        verbose_name="Создатель")

    class Meta:
        verbose_name = 'котенок'
        verbose_name_plural = 'Котята'

    def __str__(self):
        return self.name

    def calculate_age_in_months(self):
        today = timezone.now().date()
        delta = today - self.birth_date
        return delta.days // 30

    @property
    def age_in_months(self):
        return self.calculate_age_in_months()

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.score for rating in ratings) / ratings.count()
        return 0


class Rating(models.Model):
    cat = models.ForeignKey(
        Cat, related_name='ratings',
        on_delete=models.CASCADE, verbose_name="Кот"
    )
    user = models.ForeignKey(
        User, related_name='ratings',
        on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка", choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cat', 'user')
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

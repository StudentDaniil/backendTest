from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса',
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость',
        null=True,
        blank=True
    )
    lessons_count = models.IntegerField(
        default=0,
        verbose_name='Количество уроков',
    )
    demand_course_percent = models.IntegerField(
        default=0,
        verbose_name='Процент спроса на курс',
    )
    students_count = models.IntegerField(
        default=0,
        verbose_name='Количество студентов',
    )
    groups_filled_percent = models.IntegerField(
        default=0,
        verbose_name='Процент заполненности групп',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='lessons',
        null=True,
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='groups',
        null=True
    )
    students = models.ManyToManyField(
        CustomUser,
        verbose_name='Студенты',
        related_name='students_groups',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

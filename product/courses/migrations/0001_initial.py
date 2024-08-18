# Generated by Django 4.2.10 on 2024-08-17 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=250, verbose_name='Автор')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('start_date', models.DateTimeField(blank=True, verbose_name='Дата и время начала курса')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Стоимость')),
                ('lessons_count', models.IntegerField(default=0, verbose_name='Количество уроков')),
                ('demand_course_percent', models.IntegerField(default=0, verbose_name='Процент спроса на курс')),
                ('students_count', models.IntegerField(default=0, verbose_name='Количество студентов')),
                ('groups_filled_percent', models.IntegerField(default=0, verbose_name='Процент заполненности групп')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('link', models.URLField(max_length=250, verbose_name='Ссылка')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='courses.course', verbose_name='Курс')),
                ('students', models.ManyToManyField(related_name='students_groups', to=settings.AUTH_USER_MODEL, verbose_name='Студенты')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ('-id',),
            },
        ),
    ]

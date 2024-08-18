from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """
    if created:
        course = instance.course
        user = instance.user

        groups = list(course.groups.all())

        max_students_in_group = 0
        if groups:
            max_students_in_group = max(groups, key=lambda g: g.students.count()).students.count()

        if not groups:
            Group.objects.create(course=course, title=f'Группа №1')

        if max_students_in_group >= 30:
            group_count = course.groups.count()
            Group.objects.create(course=course, title=f'Группа №{group_count + 1}')

        groups = list(course.groups.all())

        min_group = min(groups, key=lambda g: g.students.count())

        min_group.students.add(user)

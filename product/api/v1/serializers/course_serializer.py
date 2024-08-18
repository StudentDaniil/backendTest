from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription, CustomUser
from django.utils import timezone

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'course',
        )


class MiniLessonSerializer(LessonSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class AdminCourseSerializer(serializers.ModelSerializer):
    """Список курсов для админа."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return obj.students.count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        return round((obj.students.count()/30) * 100 / 10, 2)

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_subscriptions = Subscription.objects.filter(course=obj).count()
        total_users = CustomUser.objects.filter(is_staff=False).count()

        if total_users == 0:
            return 0

        demand_percent = (total_subscriptions / total_users) * 100
        return round(demand_percent, 2)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons',
            'lessons_count',
            'students',
            'students_count',
            'demand_course_percent',
            'groups_filled_percent',
        )


class FullCourseSerializer(serializers.ModelSerializer):
    """Курсы для подписанных пользователей и администраторов."""
    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = (
            'author',
            'title',
            'start_date',
            'price',
            'lessons',
            'lessons_count'
        )


class PublicCourseSerializer(serializers.ModelSerializer):
    """Курсы для неподписанных пользователей."""
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = (
            'author', 'title', 'price', 'lessons_count'
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        start_date = validated_data.get('start_date', None)
        if start_date is None:
            validated_data['start_date'] = timezone.now()

        return super().create(validated_data)


class MiniCourseSerializer(LessonSerializer):
    """Список названий курсов для списка групп."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели группы."""

    course = MiniCourseSerializer(read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)

    def get_students_count(self, obj):
        """Количество студентов в группе."""
        return obj.students.count()

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'course',
            'students',
            'students_count'
        )

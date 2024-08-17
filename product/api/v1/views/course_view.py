from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        print(f"Creating lesson for course: {course.title}")
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        course = get_object_or_404(Course, pk=pk)
        user = request.user

        try:
            balance = Balance.objects.get(user=user)
        except Balance.DoesNotExist:
            return Response({"error": "У вас нет информации о балансе."},
                            status=status.HTTP_400_BAD_REQUEST)

        if balance.amount < course.price:
            return Response({"error": "Недостаточно бонусов для покупки курса."},
                            status=status.HTTP_400_BAD_REQUEST)

        if Subscription.objects.filter(user=user, course=course).exists():
            return Response({"error": "Вы уже подписаны на этот курс."},
                            status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscription.objects.create(user=user, course=course)

        balance.amount -= course.price
        balance.save()

        data = {
            "subscription": {
                "user": user.email,
                "course": course.title,
                "created_at": subscription.created_at
            }
        }

        return Response(data, status=status.HTTP_201_CREATED)

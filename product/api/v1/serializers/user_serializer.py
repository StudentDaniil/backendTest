from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Balance

from api.v1.serializers.course_serializer import CourseSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'user',
            'course',
            'created_at'
        )


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели баланса пользователя."""

    class Meta:
        model = Balance
        fields = ('id', 'user', 'amount')

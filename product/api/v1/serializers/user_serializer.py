from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from users.models import Subscription, Balance

from api.v1.serializers.course_serializer import FullCourseSerializer

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
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = UserSerializer(read_only=True)
    course = FullCourseSerializer(read_only=True)

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
        fields = (
            'id',
            'user',
            'amount'
        )


class BalanceCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания баланса пользователя."""

    class Meta:
        model = Balance
        fields = (
            'user',
            'amount',
        )

    def create(self, validated_data):
        user = self.context.get('request').user

        balance = Balance.objects.create(user=user, **validated_data)
        return balance

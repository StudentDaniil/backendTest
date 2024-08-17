from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer, BalanceCreateSerializer
from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin, IsStudentReadOnlyOrIsAdmin
from users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class BalanceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsStudentReadOnlyOrIsAdmin,)
    queryset = Balance.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BalanceSerializer
        return BalanceCreateSerializer

from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request):
    # TODO
    pass


class IsSubscribedToCourse(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        course_id = view.kwargs.get('course_id')
        if course_id is None:
            return False

        if request.method in SAFE_METHODS:
            return Subscription.objects.filter(user=request.user, course__id=course_id).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class IsStudentReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # return request.user.is_authenticated and request.user.is_staff or request.method in SAFE_METHODS
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:

            if request.user.is_staff:
                return True

            return obj.user == request.user

        return False


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS

from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsTaskCreatorOrAssignee(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ["PUT", "PATCH"]:
            return obj.created_by == request.user or obj.assignee == request.user

        if request.method == "DELETE":
            return obj.created_by == request.user

        return False

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsCommentOwner(BasePermission):
        
        def has_permission(self, request, view):
            permission_classes = [IsAuthenticated | ReadOnly]
            return request.method in SAFE_METHODS

            def has_object_permission(self , request , view , obj):
                if request.method in SAFE_METHODS:
                    return True

                return obj.author ==request.user



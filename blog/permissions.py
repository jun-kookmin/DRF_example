from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    작성자만 수정/삭제 권한 부여 (나머지는 읽기만 가능)
    """
    def has_object_permission(self, request, view, obj):
        #읽기는 누구나 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #수정/삭제는 작성자만 가능
        return obj.author == request.user
    
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS or request.method in ["PUT", "PATCH"]:
            if request.user == obj.owner:
                return True
            if obj.members.filter(id=request.user.id).exists():
                return True
        
        if request.method == "DELETE":
            if request.user == obj.owner:
                return True
        
        return False

from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from kanban_app.models import Board

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
    

class IsMember(BasePermission):
    def has_permission(self, request, view):

        if request.method == "POST":
            board_id = request.data["board"]
            single_board = get_object_or_404(Board, pk=board_id)
            if request.user in single_board.members.all():
                return True
        return False

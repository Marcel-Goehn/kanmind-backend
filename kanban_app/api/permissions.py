from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from kanban_app.models import Board, Ticket


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


class IsPatchMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            if request.user in obj.board.members.all():
                return True
            
        if request.method == "DELETE":
            if request.user == obj.board.owner:
                return True
            if request.user == obj.creator:
                return True

        return False
    

class IsBoardTaskMember(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "POST":
            ticket = get_object_or_404(Ticket, pk=view.kwargs.get("pk"))
            if ticket.board.members.filter(pk=request.user.pk).exists():
                return True
            return False
        
    
class IsOwnerOfComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user == obj.author
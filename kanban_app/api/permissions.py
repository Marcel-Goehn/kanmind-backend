from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from kanban_app.models import Board, Ticket


class IsOwnerOrMember(BasePermission):
    """
    The custom permission class for the board model.

    It ensures that:
        - if the request method is GET, PUT or PATCH, the members and owner of the board are 
          allowed to read and update it
        - if the request method is DELETE, only the owner of the board is allowed to delete it
    """

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
    """
    This permission class makes sure that:
        - the creator of the task is a member of the board
    """

    def has_permission(self, request, view):

        if request.method == "POST":
            board_id = request.data["board"]
            single_board = get_object_or_404(Board, pk=board_id)
            if request.user in single_board.members.all():
                return True
            return False


class IsPatchMember(BasePermission):
    """
    This permission class makes sure that:
        - if the request method is PUT or PATCH, the authenticated user who wants to update the task,
          has to be a member of the board
        - if the request method is DELETE, the authenticated can only delete it if he is the board
          owner or the creator of the task
    """

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
    """
    This permission class makes sure that:
        - the authenticated user has to be a member of the board to create a comment on the specific ticket
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "POST":
            ticket = get_object_or_404(Ticket, pk=view.kwargs.get("pk"))
            if ticket.board.members.filter(pk=request.user.pk).exists():
                return True
            return False


class IsOwnerOfComment(BasePermission):
    """
    This permission makes sure that:
        - the authenticated user, who wants to delete a comment, has also to be the author of it
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user == obj.author

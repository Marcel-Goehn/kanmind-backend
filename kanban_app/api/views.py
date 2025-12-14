from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from kanban_app.models import Board, Ticket, Comment
from .serializers import (BoardListSerializer, BoardRetrieveSerializer, BoardUpdateSerializer,
                          TaskSerializer, TaskPatchSerializer, CommentSerializer)
from .permissions import (IsOwnerOrMember, IsMember, IsPatchMember, IsBoardTaskMember, 
                          IsOwnerOfComment)


class ListCreateBoardView(generics.ListCreateAPIView):
    """
    - Shows a list of all boards of wich the authenticated user is a member or owner of
    - Creates a new board
    """

    serializer_class = BoardListSerializer

    def get_queryset(self):
        """
        Returns a queryset of the Board model that inclues the following:
            - boards where the authenticated user is the owner of
            - boards where the authenticated user is a member of
            - makes sure with the distinct() method, that there are not duplicates
        """

        return Board.objects.filter(Q(owner=self.request.user) | Q(members__id=self.request.user.id)).distinct()

    def perform_create(self, serializer):
        """
        Adds the authenticated user to the owner field of the Board model before the create() method
        gets executed
        """

        serializer.save(owner=self.request.user)


class RetrieveUpdateDestroyBoardView(generics.RetrieveUpdateDestroyAPIView):
    """
    - Sends a single Board as a response
    - Updates a specific Board
    - Deletes a specific Board
    """

    queryset = Board.objects.all()
    permission_classes = [IsOwnerOrMember]

    def get_serializer_class(self):
        """
        Returns differents serializer based on the request method.

        The reason for it is, that the response data differs for the get method and patch/put method
        """

        if self.request.method == "GET":
            return BoardRetrieveSerializer
        if self.request.method == "PATCH":
            return BoardUpdateSerializer
        if self.request.method == "PUT":
            return BoardUpdateSerializer


class EmailCheckView(APIView):
    """Cheks if Email is already in use."""

    def get(self, req):
        user = get_object_or_404(User, email=req.user.email)
        data = {
            "id": user.pk,
            "email": user.email,
            "fullname": user.username
        }
        return Response(data, status=status.HTTP_200_OK)


class AssignedToMeView(generics.ListAPIView):
    """Returns a list of all Tickets/Tasks that are assigned to the authenticated user."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        return Ticket.objects.filter(assignee=self.request.user)


class ReviewView(generics.ListAPIView):
    """Returns a list of all Tickets/Tasks that the authenticated user has to review."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        return Ticket.objects.filter(reviewer=self.request.user)
    

class CreateTaskView(generics.CreateAPIView):
    """Creates a new Task."""

    queryset = Ticket.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsMember]

    def perform_create(self, serializer):
        """
        Adds the authenticated user to the creator field of the Task model before the create() method
        gets executed
        """

        serializer.save(creator=self.request.user)


class UpdateDeleteTaskView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    This class allows to:
        - updates a task
        - delete a task
    """
    
    queryset = Ticket.objects.all()
    serializer_class = TaskPatchSerializer
    permission_classes = [IsPatchMember]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ListCreateCommentView(generics.ListCreateAPIView):
    """
    This class allows to:
        - return a list of all comments that belong to a specific task
        - create a new comment that belongs to a specific task
    """

    serializer_class = CommentSerializer
    permission_classes = [IsBoardTaskMember]

    def get_queryset(self):
        """
        Returns a queryset of Comments, that only belong to a specific Task
        """

        pk = self.kwargs["pk"]
        return Comment.objects.filter(ticket=pk).order_by("created_at")

    def perform_create(self, serializer):
        """
        - Adds the authenticated user to the author field of the Comment.
        - Adds the specific Ticket instance to the ticket field of the Comment model

        Calls the create() method in the serializer
        """

        ticket = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        serializer.save(author=self.request.user, ticket=ticket)


class DestroyCommentView(generics.DestroyAPIView):
    """Deletes a specific Comment."""

    permission_classes = [IsOwnerOfComment]

    def get_queryset(self):
        """
        Returns a queryset of all the Comments that belong to a specific Task/Ticket
        """

        task_id = self.kwargs["task_id"]
        return Comment.objects.filter(ticket=task_id)


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
from .permissions import IsOwnerOrMember


class ListCreateBoardView(generics.ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        return Board.objects.filter(Q(owner=self.request.user) | Q(members__id=self.request.user.id)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveUpdateDestroyBoardView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsOwnerOrMember]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BoardRetrieveSerializer
        if self.request.method == "PATCH":
            return BoardUpdateSerializer
        if self.request.method == "PUT":
            return BoardUpdateSerializer


class EmailCheckView(APIView):
    def get(self, req):
        user = get_object_or_404(User, email=req.user.email)
        data = {
            "id": user.pk,
            "email": user.email,
            "fullname": user.username
        }
        return Response(data, status=status.HTTP_200_OK)


class AssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Ticket.objects.filter(assignee=self.request.user)


class ReviewView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Ticket.objects.filter(reviewer=self.request.user)
    

class CreateTaskView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TaskSerializer


class UpdateDeleteTaskView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TaskPatchSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ListCreateCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Comment.objects.filter(ticket=pk)

    def perform_create(self, serializer):
        ticket = get_object_or_404(Ticket, pk=self.kwargs["pk"])
        serializer.save(author=self.request.user, ticket=ticket)


class DestroyCommentView(generics.DestroyAPIView):

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        return Comment.objects.filter(ticket=task_id)


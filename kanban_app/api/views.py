from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from kanban_app.models import Board
from .serializers import BoardListSerializer
# from .permissions import IsOwnerOrMember


class ListCreateBoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EmailCheckView(APIView):
    def get(self, req):
        user = get_object_or_404(User, email=req.user.email)
        data = {
            "id": user.pk,
            "email": user.email,
            "fullname": user.username
        }
        return Response(data, status=status.HTTP_200_OK)
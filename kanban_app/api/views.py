from rest_framework import generics
from kanban_app.models import Board
from .serializers import BoardListSerializer
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerOrMember


class ListCreateBoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
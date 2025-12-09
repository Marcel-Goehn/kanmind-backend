from django.urls import path
from .views import ListCreateBoardView

urlpatterns = [
    path("boards/", ListCreateBoardView.as_view(), name="board-list")
]
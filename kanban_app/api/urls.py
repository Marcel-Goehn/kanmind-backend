from django.urls import path
from .views import ListCreateBoardView, EmailCheckView

urlpatterns = [
    path("boards/", ListCreateBoardView.as_view(), name="board-list"),
    path("email-check/", EmailCheckView.as_view(), name="email-check")
]
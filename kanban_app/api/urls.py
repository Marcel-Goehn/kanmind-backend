from django.urls import path
from .views import ListCreateBoardView, RetrieveUpdateDestroyBoardView, EmailCheckView

urlpatterns = [
    path("boards/", ListCreateBoardView.as_view(), name="board-list"),
    path("boards/<int:pk>/", RetrieveUpdateDestroyBoardView.as_view(), name="board-detail"),
    path("email-check/", EmailCheckView.as_view(), name="email-check")
]
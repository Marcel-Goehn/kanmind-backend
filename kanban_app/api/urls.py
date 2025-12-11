from django.urls import path
from .views import (ListCreateBoardView, RetrieveUpdateDestroyBoardView, 
                    EmailCheckView, AssignedToMeView, ReviewView,
                    CreateTaskView, UpdateDeleteTaskView, ListCreateCommentView,
                    DestroyCommentView)

urlpatterns = [
    path("boards/", ListCreateBoardView.as_view(), name="board-list"),
    path("boards/<int:pk>/", RetrieveUpdateDestroyBoardView.as_view(), name="board-detail"),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
    path("tasks/", CreateTaskView.as_view(), name="task"),
    path("tasks/<int:pk>/", UpdateDeleteTaskView.as_view(), name="update-delete-task"),
    path("tasks/<int:pk>/comments/", ListCreateCommentView.as_view(), name="create-comment"),
    path("tasks/<int:task_id>/comments/<int:pk>/", DestroyCommentView.as_view(), name="destroy-comment"),
    path("tasks/assigned-to-me/", AssignedToMeView.as_view(), name="assigned-to-me"),
    path("tasks/reviewing/", ReviewView.as_view(), name="review")
]
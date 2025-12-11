from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="members_board", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_board")

    def __str__(self):
        return self.title
    

class Ticket(models.Model):
    status_choices = [
        ("to-do", "to-do"),
        ("in-progress", "in-progress"),
        ("review", "review"),
        ("done", "done"),
    ]

    priority_choices = [
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high"),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tickets")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=status_choices)
    priority = models.CharField(max_length=15, choices=priority_choices)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket_assignee")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket_reviewer")
    due_date = models.DateField()

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments", default="")


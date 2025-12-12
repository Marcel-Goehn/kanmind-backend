from django.contrib import admin
from .models import Board, Comment, Ticket

# Register your models here.

admin.site.register(Board)
admin.site.register(Ticket)
admin.site.register(Comment)

from rest_framework import serializers
from kanban_app.models import Board


class BoardListSerializer(serializers.ModelSerializer):

    member_count = serializers.SerializerMethodField(read_only=True)
    ticket_count = serializers.SerializerMethodField(read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField(read_only=True)
    tasks_high_prio_count = serializers.SerializerMethodField(read_only=True)
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "members", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "members": { "write_only": True }
        }

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tickets.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tickets.filter(status="to-do").count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tickets.filter(priority="high").count()
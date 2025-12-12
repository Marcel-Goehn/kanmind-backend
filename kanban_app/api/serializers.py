from django.contrib.auth.models import User
from rest_framework import serializers
from kanban_app.models import Board, Ticket, Comment


class BoardListSerializer(serializers.ModelSerializer):

    member_count = serializers.SerializerMethodField(read_only=True)
    ticket_count = serializers.SerializerMethodField(read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField(read_only=True)
    tasks_high_prio_count = serializers.SerializerMethodField(read_only=True)
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "members", "member_count", "ticket_count",
                  "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "members": {"write_only": True}
        }

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tickets.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tickets.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tickets.filter(priority="high").count()


class MemberSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]
        read_only_fields = ["id", "email"]


class HelperTaskSerializer(serializers.ModelSerializer):

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "status",
                  "priority", "assignee", "reviewer", "comments_count"]
        read_only_fields = ["id", "title", "description", "priority"]

    def get_comments_count(self, obj):
        return obj.comments.count()


class BoardRetrieveSerializer(serializers.ModelSerializer):

    owner_id = serializers.IntegerField()
    members = MemberSerializer(many=True, read_only=True)
    tasks = HelperTaskSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardUpdateSerializer(serializers.ModelSerializer):

    owner_data = MemberSerializer(source="owner", read_only=True)
    members_data = MemberSerializer(
        source="members", read_only=True, many=True)

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "members": {"write_only": True}
        }


class TaskSerializer(serializers.ModelSerializer):

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="assignee", required=False)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="reviewer", required=False)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "board", "title", "description", "status", "priority",
                  "assignee_id", "assignee", "reviewer_id", "reviewer", "due_date", "comments_count"]
        read_only_fields = ["id"]

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def validate(self, data):
        board = data.get("board")
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee_id": "Assignee is not a member of the board."})

        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({"reviewer_id": "Reviewer is not a member of the board."})

        return data


class TaskPatchSerializer(serializers.ModelSerializer):

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="assignee")
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="reviewer")

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "status", "priority",
                  "assignee_id", "assignee", "reviewer_id", "reviewer", "due_date"]
        read_only_fields = ["id"]

    def validate(self, data):
        board = self.instance.board
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee_id": "Assignee is not a member of the board."})

        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({"reviewer_id": "Reviewer is not a member of the board."})

        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]
        read_only_fields = ["id", "created_at"]

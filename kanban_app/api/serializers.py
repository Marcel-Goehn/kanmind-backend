from django.contrib.auth.models import User
from rest_framework import serializers
from kanban_app.models import Board, Ticket, Comment


class BoardListSerializer(serializers.ModelSerializer):
    """Serializer for listing all Boards that belong to a specific User."""

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
        """Returns an integer, wich contains the count of all members 
        that are part of the board."""

        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns an integer, wich contains the count of all tickets/tasks 
        that belong to the board."""

        return obj.tickets.count()

    def get_tasks_to_do_count(self, obj):
        """Returns an integer, wich contains the count of all tasks, where the status is 'to-do'."""

        return obj.tickets.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        """Returns an integer, wich contains the count of all tasks, where the priority is 'high'."""

        return obj.tickets.filter(priority="high").count()


class MemberSerializer(serializers.ModelSerializer):
    """
    Helper serializer for representating the nested relationships of members, 
    assignees and reviewers.
    """

    fullname = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]
        read_only_fields = ["id", "email"]


class HelperTaskSerializer(serializers.ModelSerializer):
    """
    Helper serializer for representating the tasks of a board in a nested relationship.
    """

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "status",
                  "priority", "assignee", "reviewer", "due_date", "comments_count"]
        read_only_fields = ["id", "title", "description", "priority"]

    def get_comments_count(self, obj):
        """Returns the amount of comments, that belong to the task."""

        return obj.comments.count()


class BoardRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer that returns a single instance of a board.
    """

    owner_id = serializers.IntegerField()
    members = MemberSerializer(many=True, read_only=True)
    tasks = HelperTaskSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer that updates a specific task and returns the updated instance.
    """

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
    """
    Serializer that returns the tasks that belong to a specific board. 
    It also allows to create new taks.
    """

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
        """Returns the amount of comments, that belong to a specific task."""

        return obj.comments.count()
    
    def validate(self, data):
        """
        This validation method does the following:
            - gets an instance of the board where the task belongs to
            - get the assignee
            - get the reviewer
            - checks if the task has an assignee or reviewer
            - if an assignee is in the request body, it checks if the assignee is a member of the board
            - if a reviewer is in the request body, it checks if the reviewer is a member of the board
        """

        board = data.get("board")
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee_id": "Assignee is not a member of the board."})

        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({"reviewer_id": "Reviewer is not a member of the board."})

        return data


class TaskPatchSerializer(serializers.ModelSerializer):
    """Serializer for PATCH request to update a specific task."""

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
        """
        This validation method does the following:
            - gets an instance of the board where the task belongs to
            - get the assignee
            - get the reviewer
            - checks if the task has an assignee or reviewer
            - if an assignee is in the request body, it checks if the assignee is a member of the board
            - if a reviewer is in the request body, it checks if the reviewer is a member of the board
        """

        board = self.instance.board
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee_id": "Assignee is not a member of the board."})

        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError({"reviewer_id": "Reviewer is not a member of the board."})

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for getting a list of comments or to create a comment."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]
        read_only_fields = ["id", "created_at"]

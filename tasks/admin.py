from django.contrib import admin
from .models import User
from .models import Task
from .models import Team


# displaye the following user fields in the admin page
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "get_tasks",
        "get_teams",
    )


# displays the following task fields in the admin page
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task_name", "description", "assignee", "due_date"]


@admin.register(Team)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "get_members"]

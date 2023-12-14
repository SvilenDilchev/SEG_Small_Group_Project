# Import necessary modules and classes
from django.core.validators import RegexValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django.conf import settings


# Define the User model, extending AbstractUser for authentication
class Task(models.Model):
    # Task name with a maximum character length of 50
    task_name = models.CharField(max_length=50, blank=False)
    # Description with maximum character length of 200 and a validation to ensure the limit
    description = models.TextField(
        max_length=200, blank=False, validators=[MaxLengthValidator(200)]
    )
    due_date = models.DateTimeField(blank=False, null=False)

    # Define a custom username field with regex validators
    assignee = models.CharField(
        max_length=30
    )
    objects = models.Manager()
    maker = models.CharField(max_length=50)

    class Meta:
        """Model options."""

        # Tasks are ordered by due date
        ordering = ["due_date"]

    def get_assignee(self):
        return f"{self.assignee}"

    def __str__(self):
        return f"{self.task_name}, due at {self.due_date}, by {self.assignee}"


# Define the Team model
class Team(models.Model):
    # Define a many-to-many relationship with the User model for team members
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="team_members"
    )

    # Define the members that are invited to the team
    invited_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="team_invited_members"
    )

    # Define a unique name for the team
    name = models.CharField(max_length=55, unique=True, blank=False)

    # Define an optional description for the team
    description = models.TextField(blank=True)

    def get_members(self):
        return "\n , ".join(str(member) for member in self.members.all())

    def get_members_queryset(self):
        return self.members.all()

    def remove_member_from_team(self, user):
        if self.members.filter(id=user.id).exists():
            self.members.remove(user)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    # Define a custom username field with regex validation
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^@\w{3,}$",
                message="Username must consist of @ followed by at least three alphanumericals",
            )
        ],
    )

    # Define first_name and last_name fields with max length
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    # Define an email field with uniqueness constraint
    email = models.EmailField(unique=True, blank=False)

    class Meta:
        """Model options."""

        # Set default ordering for user names
        ordering = ["last_name", "first_name"]

    tasks = models.ManyToManyField(Task, related_name="tasks")
    teams = models.ManyToManyField(Team, related_name="teams")

    def get_username(self):
        return f"{self.username}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Method to return the user's gravatar URL
    def gravatar(self, size=120):
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default="mp")
        return gravatar_url

    # Method to return a miniature version of the user's gravatar URL
    def mini_gravatar(self):
        return self.gravatar(size=60)

    def get_tasks(self):
        return "\n".join([p.tasks for p in self.tasks.all()])

    def get_teams(self):
        return "\n".join(str(team) for team in Team.objects.filter(members=self))

    def __str__(self):
        return self.username


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    action = models.CharField(max_length = 255)
    timestamp = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return f'Activity Log for {self.user.username} - {self.action}'


from django.core.exceptions import ValidationError
from .models import User


# Makes sure that when an assignee is being entered into a TaskFrom the assignees username beings with an @
def starts_with_atSign_validator(value):
    if not User.objects.get(id=value).username.startswith("@"):
        raise ValidationError('Assignee must begin with "@".')


# Checks that a user exists when adding a user to a task.
# If not gives a warning to the user to ensure that the user you are adding exists.
def assignee_exists_validator(value):
    try:
        user = User.objects.get(id=value)
    except User.DoesNotExist:
        raise ValidationError(f"A user with the username '{value}' does not exist.")

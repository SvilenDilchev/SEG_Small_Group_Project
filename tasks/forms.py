"""Forms for the tasks app."""
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Team
from .models import Task
from django import forms
from tasks.widgets import BootstrapDateTimePickerInput
from tasks import taskFormValidators


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ["first_name", "last_name", "username", "email"]


class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$",
                message="Password must contain an uppercase character, a lowercase "
                "character and a number",
            )
        ],
    )
    password_confirmation = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput()
    )

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get("new_password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if new_password != password_confirmation:
            self.add_error(
                "password_confirmation", "Confirmation does not match password."
            )


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label="Current password", widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get("password")
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error("password", "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data["new_password"]
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def save(self):
        """Create a new user."""
        print("BAsdfads")

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get("username"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("new_password"),
        )
        return user


class CreateTeamForm(forms.ModelForm):
    """Form enabling users to create team."""

    class Meta:
        """Form options."""

        model = Team
        fields = ["name", "description"]

    def save(self, user):
        """Create a new user."""
        super().save(commit=False)
        team = Team(
            name=self.cleaned_data.get("name"),
            description=self.cleaned_data.get("description"),
        )

        team.save()

        team.members.add(user)
        user.team = team.name
        team.save()

        return team


class InviteForm(forms.ModelForm):
    """Form enabling users to be invited to a team."""

    invited_user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        label="Select User"
    )
    team = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'), label="Select Team")

    class Meta:
        """Form options."""

        model = Team
        fields = ["team", "invited_user"]

    def save(self):
        """Create a new user."""
        super().save(commit=False)

        team = self.cleaned_data["team"]
        invited_user = self.cleaned_data["invited_user"]

        if invited_user not in team.members.all():
            team.invited_members.add(invited_user)
            team.save()

        return team


# Controls the contents of a Task
class TaskForm(forms.ModelForm):
    # form options
    class Meta:
        model = Task
        fields = ["task_name", "description", "assignee", "due_date", "maker"]

    assignee = forms.ChoiceField(
        validators=[
            taskFormValidators.starts_with_atSign_validator,
            taskFormValidators.assignee_exists_validator,
        ],
        label='Select Team Member'
    )

    # Hides the field called maker. This is the person who makes the task and is automatically filled
    maker = forms.CharField(widget=forms.HiddenInput())

    due_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],
        widget=BootstrapDateTimePickerInput(
            attrs={"placeholder": "Enter a date and time after today"}
        ),
    )

    def save(self):
        task = super().save()
        assignee = self.cleaned_data.get("assignee")
        user = User.objects.get(id=assignee)
        user.tasks.add(task)

    def __init__(self, *args, maker=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["maker"] = maker.username
        self.fields["maker"].label = ""
        teammates = []

        if maker is not None:
            allTeams = Team.objects.all()
            for eachTeam in allTeams:
                teamMembers = eachTeam.get_members_queryset()
                for eachTeammate in teamMembers:
                    teammates.append(eachTeammate)

        if not teammates:
            teammates.append(maker)

        teammates = list(set(teammates))
        self.fields['assignee'].choices = [(choice.pk, choice) for choice in teammates]


# Allows you to edit tasks
class EditTaskForm(forms.ModelForm):
    class Meta:
        # form options
        model = Task
        fields = ["task_name", "description", "assignee", "due_date", "maker"]

    assignee = forms.ChoiceField(
        validators=[
            taskFormValidators.starts_with_atSign_validator,
            taskFormValidators.assignee_exists_validator,
        ],
        label='Select Team Member'
    )


    # Hides the field called maker. This is the person who makes the task and is automatically filled
    maker = forms.CharField(widget=forms.HiddenInput())

    due_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],
        widget=BootstrapDateTimePickerInput(
            attrs={"placeholder": "Enter a valid date and time"}
        ),
    )

    def save(self):
        task = super().save()
        assignee = self.cleaned_data.get("assignee")
        user = User.objects.get(id=assignee)
        user.tasks.add(task)

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["maker"].label = ""

        # Auto fills the following fields which shows what the task looked like before it was edited.
        if instance:
            if instance.task_name:
                self.initial["task_name"] = instance.task_name
            if instance.description:
                self.initial["description"] = instance.description
            if instance.assignee:
                self.initial["assignee"] = instance.assignee
            if instance.maker:
                self.initial["maker"] = instance.maker
                teammates = []
                allTeams = Team.objects.all()
                for eachTeam in allTeams:
                    teamMembers = eachTeam.get_members_queryset()
                    for eachTeammate in teamMembers:
                        teammates.append(eachTeammate)
                # if not teammates:
                #    teammates.append(instance.maker)
                #    teammates.append(User.objects.get(username=instance.maker))

                teammates = list(set(teammates))
                self.fields['assignee'].choices = [(choice.pk, choice) for choice in teammates]

            if instance.due_date:
                self.initial["due_date"] = instance.due_date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateTeamForm, InviteForm, EditTaskForm
from tasks.helpers import login_prohibited
from tasks.models import Team, Task, User, ActivityLog
from tasks.forms import TaskForm
from django.shortcuts import render, get_object_or_404, redirect

def team_accept(request, team_id):
    """handle team invitation acceptance"""
    current_user = request.user
    team = Team.objects.filter(name=team_id)
    if team.exists():
        team = team[0]
        if current_user in team.invited_members.all():
            team.members.add(current_user)
            team.invited_members.remove(current_user)
            current_user.team = team.name

    return redirect("teams")  # Redirect to the teams page or any other page you prefer

def team_reject(request, team_id):
    """handle team invitation rejection."""
    current_user = request.user
    team = Team.objects.filter(name=team_id)
    if team.exists():
        team = team[0]
        if current_user in team.invited_members.all():
            team.invited_members.remove(current_user)

    return redirect("teams")  # Redirect to the teams page or any other page you prefer


def leave_team(request, team_id):
    current_user = request.user
    team = Team.objects.filter(id=team_id)
    teams = Team.objects.filter(members=current_user)
    invited_teams = Team.objects.filter(invited_members=current_user)
    data = Task.objects.all()
    userData = []
    myCreatedTasks = []

    for task in data:
        if str(task.assignee) == str(current_user.id):
            userData.append(task)

        if task.maker == current_user.username:
            myCreatedTasks.append(task)

    for exactTeam in team:
        if exactTeam.members.filter(id=current_user.id):
            exactTeam.members.remove(current_user)
            if exactTeam.members.count() == 0:
                exactTeam.delete()

    return render(
        request,
        "dashboard.html",
        {
            "user": current_user,
            "data": userData,
            "createdTasks": myCreatedTasks,
            "teams": teams,
            "invites": invited_teams
        },
    )

@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    data = Task.objects.all()
    teams = Team.objects.filter(members=current_user)
    invited_teams = Team.objects.filter(invited_members=current_user)
    userData = []
    myCreatedTasks = []

    for task in data:
        if str(task.assignee) == str(current_user.id):
            userData.append(task)

        if task.maker == current_user.username:
            myCreatedTasks.append(task)

    return render(
        request,
        "dashboard.html",
        {
            "user": current_user,
            "data": userData,
            "createdTasks": myCreatedTasks,
            "teams": teams,
            "invites": invited_teams,
        },
    )


@login_required
def teams(request):
    """Display user's teams"""
    current_user = request.user

    teams = Team.objects.filter(members=current_user)

    # Get teams where the user is invited
    invited_teams = Team.objects.filter(invited_members=current_user)

    return render(request, "teams.html", {"teams": teams, "invites": invited_teams})


class CreateTeamView(FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = CreateTeamForm
    template_name = "create_team.html"
    success_url = reverse_lazy("teams")

    def form_valid(self, form):
        user = self.request.user
        form.save(user)
        return super().form_valid(form)


class InviteTeam(FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = InviteForm
    template_name = "invite_user.html"
    success_url = reverse_lazy("teams")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["team"].queryset = Team.objects.filter(members=self.request.user)
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, "home.html")


# Retrives all tasks and renders then in the 'your_tasks.html' template.
def your_tasks(request):
    data = Task.objects.filter(assignee=request.user.id)
    return render(request, "your_tasks.html", {"data": data})


# Creates a new task and renders it with the TaskForm model.
# If the form is valid, the task is saved, and the user is brought to the dashboard.
def tasks(request):
    current_user = request.user

    form = TaskForm(request.POST or None, maker=current_user)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("dashboard"))

    return render(request, "tasks.html", {"user": current_user, "form": form})


# Enables the user to edit existing tasks and renders an EditTaskForm model.
# If the edited form is valid, the task is updates and the user is brought back to the dashboard.
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    form = EditTaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        task.delete()
        return HttpResponseRedirect(reverse("dashboard"))

    return render(request, "edit_task.html", {"form": form, "task": task})


# Allows the user to delete an exisiting task.
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()

    current_user = request.user
    teams = Team.objects.filter(members=current_user)
    invited_teams = Team.objects.filter(invited_members=current_user)
    data = Task.objects.all()
    userData = []
    myCreatedTasks = []

    for task in data:
        if str(task.assignee) == str(current_user.id):
            userData.append(task)

        if task.maker == current_user.username:
            myCreatedTasks.append(task)

    return render(
        request,
        "dashboard.html",
        {
            "user": current_user,
            "data": userData,
            "createdTasks": myCreatedTasks,
            "teams": teams,
            "invites": invited_teams
        },
    )


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ["get", "post"]
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get("next") or ""
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get("next") or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(
            request, messages.ERROR, "The credentials provided were invalid!"
        )
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, "log_in.html", {"form": form, "next": self.next})


def log_out(request):
    """Log out the current user"""
    user = request.user
    logout(request)
    #Logging the user logout to activity log entry,as this is a custom log out, middleware can't detect it
    ActivityLog.objects.create(
        user=user,
        action='Visited /log_out/',
        timestamp=timezone.now()
    )
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = "password.html"
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse("dashboard")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        print("A????")
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

    ############
    # Constraints of the Invitation function
    # Can't invite someone already in the team


@login_required
def activityLogView(request):
    activity_log = ActivityLog.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "activity_log.html", {"activity_log": activity_log})

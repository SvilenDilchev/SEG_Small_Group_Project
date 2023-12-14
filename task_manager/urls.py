"""
URL configuration for task_manager project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("log_in/", views.LogInView.as_view(), name="log_in"),
    path("log_out/", views.log_out, name="log_out"),
    path("password/", views.PasswordView.as_view(), name="password"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),
    path("sign_up/", views.SignUpView.as_view(), name="sign_up"),
    path("tasks/", views.tasks, name="tasks"),
    path("", views.your_tasks),
    path("teams/", views.teams, name="teams"),
    path("create_team", views.CreateTeamView.as_view(), name="create_team"),
    path("invite_user", views.InviteTeam.as_view(), name="invite_user"),
    path("tasks/", views.tasks, name="tasks"),
    path("teams/accept/<str:team_id>/", views.team_accept, name="accept_invite"),
    path("teams/reject/<str:team_id>/", views.team_reject, name="reject_invite"),
    path("edit_task/<int:task_id>/", views.edit_task, name="edit_task"),
    path("dashboard/<int:task_id>/", views.delete_task, name="dashboard_delete"),
    path("activity_log", views.activityLogView, name="activity_log"),
    path("dashboard/leave_team/<int:team_id>", views.leave_team, name="leave_team")
]

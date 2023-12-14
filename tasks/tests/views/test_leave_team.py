from django.test import TestCase
from tasks.models import Team, Task, User
from tasks.views import leave_team
from django.urls import reverse
from django.test import RequestFactory

class LeaveTeamTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='@personA', password='Password123')
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user)
        self.task1 = Task.objects.create(assignee=self.user, maker=self.user.username, due_date="2024-11-10 12:13",)
        self.task2 = Task.objects.create(assignee=self.user, maker=self.user.username, due_date="2024-11-10 12:13",)

    def test_leave_team(self):
        factory = RequestFactory()
        request = factory.get(reverse('dashboard'))
        request.user = self.user
        leave_team(request, self.team.id)
        self.assertFalse(self.team.members.filter(id=self.user.id).exists())
        self.assertFalse(Team.objects.filter(id=self.team.id).exists())

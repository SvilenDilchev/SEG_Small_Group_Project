"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from tasks.forms import CreateTeamForm, InviteForm
from tasks.models import Team, User


class TeamViewTestCase(TestCase):
    """Tests of the team view."""

    fixtures = ["tasks/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse("teams")
        self.team = Team.objects.create(name="Name", description="Description")

    def test_teams_url(self):
        self.assertEqual(self.url, "/teams/")

    # <<<<<<< HEAD
    # #error
    # def test_get_team(self):
    # =======
    # def test_team_accept(self):
    #    self.team.invited_members.add(self.user)
    # >>>>>>> team-model-base
    #    self.client.login(username=self.user.username, password='Password123')
    #    response = self.client.get(reverse('accept_invite', args=[self.team.name]))
    #    self.assertEqual(response.status_code, 302)
    #    updated_team = Team.objects.get(name=self.team.name)
    #    self.assertTrue(self.user in updated_team.members.all())
    #    self.assertFalse(self.user in updated_team.invited_members.all())

    def test_team_reject(self):
        self.team.invited_members.add(self.user)
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse("reject_invite", args=[self.team.name]))
        self.assertEqual(response.status_code, 302)
        updated_team = Team.objects.get(name=self.team.name)
        self.assertFalse(self.user in updated_team.invited_members.all())
        self.assertRedirects(response, reverse("teams"))

    # def test_create_team_view(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'name="form"')
    #     response = self.client.post(self.url, data={'name': 'Test Team', 'description': 'Test Description'})
    #     self.assertEqual(response.status_code, 302)
    #     created_team = User.objects.get(username='@johndoe').teams.first()
    #     self.assertIsNotNone(created_team)
    #     self.assertEqual(created_team.name, 'Test Team')
    #     self.assertTrue(self.user in created_team.members.all())
    #     self.assertRedirects(response, reverse('teams'))

    # def test_get_form(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.context['form'], InviteForm)
    #     form = response.context['form']
    #     self.assertIsNotNone(form.fields["team"].queryset)
    #
    # def test_get_team(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     response = self.client.get(self.url, follow = True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'teams.html')
    #     form = response.context['form']
    #     self.assertTrue(isinstance(form, CreateTeamForm))
    #     self.assertEqual(form.instance, self.user)
    #
    # def test_create_team_url(self):
    #     response = self.client.get(self.url_create_team)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'create_team.html')
    #
    # def test_invite_user_url(self):
    #     response = self.client.get(self.url_invite_user)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'invite_user.html')
    #
    # def test_teams_view_with_authenticated_user(self):
    #     self.client.login(username='@johndoe', password='Password123')
    #     response = self.client.get(self.url_teams)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(self.team, response.context['teams'])
    #     self.assertContains(response, 'Name')
    #     self.assertContains(response, 'Description')
    #     self.assertIn(self.user, response.context['team_members'])

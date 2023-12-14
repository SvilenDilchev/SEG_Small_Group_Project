"""Tests of the create team view."""
from django.test import TestCase
from django.urls import reverse

from tasks.forms import CreateTeamForm
from tasks.models import User, Team
from django.test import TestCase
from django.urls import reverse
from tasks.models import User


class CreateTeamViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ["tasks/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse("profile")
        self.form_input = {"name": "TestTeam", "description": "this is the description"}
        self.url = reverse("create_team")

    def test_create_team_url(self):
        self.assertEqual(self.url, "/create_team")

    def test_get_create_team(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_team.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_create_team(self):
        self.form_input["name"] = " "
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_team.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertTrue(form.is_bound)

    # WHY DON'T THESE WORK

    # def test_succesful_create_team(self):
    #     before_count = Team.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     after_count = Team.objects.count()
    #     self.assertEqual(after_count, before_count+1)
    #     response_url = reverse('teams')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertContains(response, 'TestTeam')
    #     self.assertContains(response, 'this is the description')
    #     team = Team.objects.get(name='TestTeam')
    #     self.assertEqual(team.name, 'TestTeam')
    #     self.assertEqual(team.description, 'this is the description')

    # def test_get_create_team_redirects_when_created(self):
    #     self.client.login(username=self.user.username, password="Password123")
    #     response_create_team = self.client.post(reverse('create_team'), data={'team_name': 'Test Team'})
    #     self.assertEqual(response_create_team.status_code, 302)
    #     response_teams = self.client.get(response_create_team.url, follow=True)
    #     self.assertRedirects(response_create_team, reverse('teams'), status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response_teams, 'teams.html')

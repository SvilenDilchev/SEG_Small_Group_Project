from django.test import TestCase, Client
from tasks.models import Team, User

class TeamAcceptanceTestCase(TestCase):
    def setUp(self):
        self.userA = User.objects.create_user(username='@personA', password='Password123', email="personA@x.com")
        self.team = Team.objects.create(name='testteam')
        self.userB = User.objects.create_user(username='@personB', password='Password123', email="personB@x.com")
        self.team.invited_members.add(self.userB)

    def test_team_accept_success(self):
        self.client.login(username='@personB', password='Password123')
        response = self.client.get(f'/teams/accept/{self.team.name}/')
        self.assertRedirects(response, '/teams/', status_code=302, target_status_code=200)
        self.assertTrue(self.userB in self.team.members.all())
        self.assertFalse(self.userB in self.team.invited_members.all())

    def test_team_accept_invalid_team(self):
        self.client.login(username='@personB', password='Password123')
        response = self.client.get('/teams/accept/nonexistentteam/')
        self.assertRedirects(response, '/teams/', status_code=302, target_status_code=200)
        self.assertFalse(self.userB in self.team.members.all())

    def test_team_accept_uninvited_user(self):
        self.client.login(username='@personA', password='Password123')
        response = self.client.get(f'/teams/accept/{self.team.name}/')
        self.assertRedirects(response, '/teams/', status_code=302, target_status_code=200)
        self.assertFalse(self.userA in self.team.invited_members.all())
        self.assertEqual(list(self.team.members.all()), [])

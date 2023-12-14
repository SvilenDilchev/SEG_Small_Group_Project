# Import necessary modules and classes
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from tasks.models import User, Team


# Define a TestCase for the Team model
class TeamModelTestCase(TestCase):
    """Unit tests for the Team model."""

    # Load fixtures for testing
    fixtures = [
        "tasks/tests/fixtures/default_user.json",
        "tasks/tests/fixtures/other_users.json",
    ]

    # Gravatar URL for reference
    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    # Setup method to initialize common objects for tests
    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team", description="This is a test team."
        )

    # Test method to check if a valid team passes validation
    def test_valid_team(self):
        self._assert_team_is_valid()

    # Test method to check if a team with a blank name is invalid
    def test_name_cannot_be_blank(self):
        self.team.name = ""
        self._assert_team_is_invalid()

    # Test method to check if a team with a blank description is still valid
    def test_description_can_be_blank(self):
        self.team.description = ""
        self._assert_team_is_valid()

    # Test method to check if team names must be unique
    def test_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Team.objects.create(name=self.team.name, description="Another Test Team")

    # Test method to check if members can be added to a team
    def test_members_can_be_added(self):
        new_user = User.objects.create(
            username="@newuser",
            first_name="New",
            last_name="User",
            email="newuser@example.com",
        )
        self.team.members.add(new_user)
        self.assertIn(new_user, self.team.members.all())

    def test_name_can_be_55_characters_long(self):
        self.team.name = "x" * 55
        self._assert_team_is_valid()

    def test_name_cannot_be_over_55_characters_long(self):
        self.team.name = "x" * 56
        self._assert_team_is_invalid()

    def test_name_may_contain_numbers(self):
        self.team.name = "team123"
        self._assert_team_is_valid()

    def _assert_team_is_valid(self):
        try:
            self.team.full_clean()
        except ValidationError:
            self.fail("Test team should be valid")

    def _assert_team_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.team.full_clean()

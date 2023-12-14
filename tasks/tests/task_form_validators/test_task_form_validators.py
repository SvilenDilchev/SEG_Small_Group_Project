from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.taskFormValidators import (
    starts_with_atSign_validator,
    assignee_exists_validator,
)
from tasks.models import User


class TaskFormValidatorsTestCase(TestCase):
    # tests for the task form validators in taskFormValidators.py
    fixtures = [
        "tasks/tests/fixtures/default_user.json",
        "tasks/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.valid_assignee = "@johndoe"
        self.invalid_assignee = "johndoe"

        # Creating a user for assignee_exists_validator test
        self.valid_user = User.objects.create(username="valid_user")

    def test_starts_with_atSign_validator_valid(self):
        try:
            starts_with_atSign_validator(self.valid_assignee)
        except ValidationError:
            self.fail(
                "starts_with_atSign_validator should not raise ValidationError for a valid assignee."
            )

    def test_starts_with_atSign_validator_invalid(self):
        with self.assertRaises(ValidationError):
            starts_with_atSign_validator(self.invalid_assignee)

    def test_assignee_exists_validator_valid(self):
        try:
            assignee_exists_validator(self.valid_assignee)
        except ValidationError:
            self.fail(
                "assignee_exists_validator should not raise ValidationError for an existing user."
            )

    def test_assignee_exists_validator_invalid(self):
        with self.assertRaises(ValidationError):
            assignee_exists_validator(self.invalid_assignee)

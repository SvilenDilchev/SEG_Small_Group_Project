from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import Task


class TaskModelTestCase(TestCase):
    # tests the task class

    def setUp(self):
        self.task = Task.objects.create(
            task_name="TaskModelTestCaseTask",
            description="A good description",
            due_date="2024-11-10 12:13",
            assignee="@admin",
            maker="@admin",
        )

    def test_valid_task(self):
        self._assert_task_is_valid()

    def test_task_name_cannot_be_blank(self):
        self.task.task_name = ""
        self._assert_task_is_invalid()

    def test_task_name_can_be_50_characters_long(self):
        self.task.task_name = "x" * 50
        self._assert_task_is_valid()

    def test_task_name_cannot_be_51_characters_long(self):
        self.task.task_name = "x" * 51
        self._assert_task_is_invalid()

    def test_description_must_not_be_blank(self):
        self.task.description = ""
        self._assert_task_is_invalid()

    def test_description_can_be_200_characters_long(self):
        self.task.description = "x" * 200
        self._assert_task_is_valid()

    def test_description_cant_be_201_characters_long(self):
        self.task.description = "x" * 201
        self._assert_task_is_invalid()

    def test_assignee_has_to_start_with_atsign(self):
        self.task.assignee = "nah"
        self._assert_task_is_invalid()

    def test_due_date_must_not_be_blank(self):
        self.task.due_date = ""
        self._assert_task_is_invalid()

    def test_due_date_has_date(self):
        self.task.due_date = "12:13"
        self._assert_task_is_invalid()

    def test_assignee_can_be_30_characters_long(self):
        self.task.assignee = "@" + "x" * 29
        self._assert_task_is_valid()

    def test_assignee_cannot_be_over_30_characters_long(self):
        self.task.assignee = "@" + "x" * 30
        self._assert_task_is_invalid()

    def test_assignee_must_start_with_at_symbol(self):
        self.task.assignee = "johndoe"
        self._assert_task_is_invalid()

    def test_assignee_must_contain_only_alphanumericals_after_at(self):
        self.task.assignee = "@john!doe"
        self._assert_task_is_invalid()

    def test_assignee_must_contain_at_least_3_alphanumericals_after_at(self):
        self.task.assignee = "@jo"
        self._assert_task_is_invalid()

    def test_assignee_may_contain_numbers(self):
        self.task.assignee = "@j0hndoe2"
        self._assert_task_is_valid()

    def test_assignee_must_contain_only_one_at(self):
        self.task.assignee = "@@johndoe"
        self._assert_task_is_invalid()

    def test_get_assignee_is_assignee(self):
        self.assertEqual(self.task.assignee, self.task.get_assignee())

    def test_str_is_valid(self):
        string = f"{self.task.task_name}, due at {self.task.due_date}, by {self.task.assignee}"
        self.assertEqual(str(self.task), string)

    def _assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except ValidationError:
            self.fail("Test task should be valid")

    def _assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()

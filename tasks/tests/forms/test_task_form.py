from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import Task
from tasks.tests.models.test_task_model import TaskModelTestCase


class TaskFormTestCase(TestCase):
    # tests the task form
    fixtures = ["tasks/tests/fixtures/default_user.json"]

    def setUp(self):
        self.form_input = {
            "task_name": "TestTask",
            "description": "a test description for a test task",
            "assignee": "@johndoe",
            "due_date": "2025-01-15 08:10",
            "maker": "@johndoe",
        }
        # 15/01/2003 08:10

    # doesn't work
    def test_task_accepts_valid_input(self):
        task = TaskForm(data=self.form_input)
        self.assertTrue(task.is_valid())

    def test_task_rejects_blank_assignee(self):
        self.form_input["assignee"] = ""
        task = TaskForm(data=self.form_input)
        self.assertFalse(task.is_valid())

    def test_task_rejects_blank_task_name(self):
        self.form_input["task_name"] = ""
        task = TaskForm(data=self.form_input)
        self.assertFalse(task.is_valid())

    def test_initial_maker_value(self):
        # Test that the 'maker' field is initialized correctly
        form = TaskForm(data=self.form_input)
        self.assertEqual(form["maker"].value(), "@johndoe")

    def test_form_label_for_maker_field(self):
        # Test that the 'maker' field label is empty as expected
        form = TaskForm(data=self.form_input)
        self.assertEqual(form.fields["maker"].label, "")

    def test_task_rejects_blank_description(self):
        self.form_input["description"] = ""
        task = TaskForm(data=self.form_input)
        self.assertFalse(task.is_valid())

    def test_task_rejects_blank_due_dates(self):
        self.form_input["due_date"] = ""
        task = TaskForm(data=self.form_input)
        self.assertFalse(task.is_valid())

    def test_task_accepts_valid_due_date(self):
        self.form_input["due_date"] = "2025-01-15 08:10"
        task = TaskForm(data=self.form_input)
        self.assertTrue(task.is_valid())

    def test_task_accepts_incorrect_assignee(self):
        self.form_input["assignee"] = "da"
        task = TaskForm(data=self.form_input)
        self.assertFalse(task.is_valid())

    def test_task_accepts_incorrect_due_dates(self):
        self.form_input["due_date"] = "123/12/3"
        task = TaskForm(data=self.form_input)
        self.assertFalse(task.is_valid())

    def test_task_form_save_function(self):
        taskForm = TaskForm(data=self.form_input)
        if taskForm.is_valid():
            taskForm.save()
            task = Task.objects.get(task_name="TestTask")
            self._assert_task_is_valid(task)

    def _assert_task_is_valid(self, task):
        try:
            task.full_clean()
        except ValidationError:
            self.fail("Test task should be valid")

    def _assert_task_is_invalid(self, task):
        with self.assertRaises(ValidationError):
            task.full_clean()

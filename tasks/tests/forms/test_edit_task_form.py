from django import forms
from django.test import TestCase
from django.utils.datetime_safe import datetime

from tasks.forms import EditTaskForm
from tasks.widgets import BootstrapDateTimePickerInput
from tasks.models import Task


class EditTaskFormTestCase(TestCase):
    fixtures = ["tasks/tests/fixtures/default_user.json"]

    def setUp(self):
        self.task = Task.objects.create(
            task_name="TaskModelTestCaseTask",
            description="A good description",
            due_date="2024-11-10 12:13",
            assignee="@admin",
            maker="@admin",
        )

        self.form_input = {
            "task_name": "EditTaskName",
            "description": "Edit task description",
            "assignee": "@johndoe",
            "due_date": "2025-11-10 12:13",
            "maker": "@johndoe",
        }

    def test_form_contains_required_fields(self):
        form = EditTaskForm()
        self.assertIn("task_name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("assignee", form.fields)
        self.assertIn("due_date", form.fields)
        self.assertIn("maker", form.fields)
        due_date_field = form.fields["due_date"]
        maker_field = form.fields["maker"]
        self.assertTrue(isinstance(due_date_field.widget, BootstrapDateTimePickerInput))
        self.assertTrue(isinstance(maker_field.widget, forms.HiddenInput))

    def test_form_accepts_valid_input(self):
        form = EditTaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_task_name_cant_be_blank(self):
        self.form_input["task_name"] = ""
        form = EditTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_description_cant_be_blank(self):
        self.form_input["description"] = ""
        form = EditTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_due_date_cant_be_blank(self):
        self.form_input["due_date"] = ""
        form = EditTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_assignee_cant_be_blank(self):
        self.form_input["assignee"] = ""
        form = EditTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_maker_cant_be_blank(self):
        self.form_input["maker"] = ""
        form = EditTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_edit_task_save(self):
        self.task.task_name = "NewTestTaskName"
        self.task.due_date = "2024-11-10 12:13"
        self.form_input["task_name"] = "NewTestTaskName"
        editTaskForm = EditTaskForm(data=self.form_input, instance=self.task)

        if editTaskForm.is_valid():
            editTaskForm.save()
            task = Task.objects.get(task_name="NewTestTaskName")
            self.assertEquals(task.task_name, "NewTestTaskName")
        else:
            self.fail("editTaskForm not valid")

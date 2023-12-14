from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Task


class TasksViewTestCase(TestCase):
    # Tests the tasks in views.py

    fixtures = ["tasks/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("tasks")
        self.user = User.objects.get(username="@johndoe")
        self.task = Task.objects.create(
            task_name="TaskModelTestCaseTask",
            description="A good description",
            due_date="2024-11-10 12:13",
            assignee="@admin",
            maker="@admin",
        )

    def test_tasks_url(self):
        self.assertEqual(self.url, "/tasks/")

    def test_get_tasks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks.html")

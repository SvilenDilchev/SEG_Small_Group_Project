from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Task
from tasks.tests.helpers import reverse_with_next


class DashboardViewTestCase(TestCase):
    # tests that the dashboard redirects to the correct tasks.html

    fixtures = ["tasks/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("dashboard")
        self.user = User.objects.get(username="@johndoe")
        self.task = Task.objects.create(
            task_name="TaskModelTestCaseTask",
            description="A good description",
            due_date="2024-11-10 12:13",
            assignee="@admin",
            maker="@admin",
        )
        self.client.login(username=self.user.username, password="Password123")

    def test_dashboard_url(self):
        self.assertEqual(self.url, "/dashboard/")

    def test_get_dashboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        currentUser = response.context["user"]
        userData = response.context["data"]
        createdTasks = response.context["createdTasks"]
        self.assertTrue(isinstance(currentUser, User))
        self.assertTrue(isinstance(userData, list))
        self.assertTrue(isinstance(createdTasks, list))

    def test_get_dashboard_with_redirects(self):
        destination_url = reverse("tasks")
        self.url = reverse_with_next("dashboard", destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        currentUser = response.context["user"]
        userData = response.context["data"]
        createdTasks = response.context["createdTasks"]
        self.assertTrue(isinstance(currentUser, User))
        self.assertTrue(isinstance(userData, list))
        self.assertTrue(isinstance(createdTasks, list))

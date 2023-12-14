from django.test import TestCase, Client
from tasks.models import User
from django.urls import reverse
from tasks.models import ActivityLog

class ActivityLogViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create some test activity log entries for the user
        ActivityLog.objects.create(user=self.user, action="Visited /dashboard/")
        ActivityLog.objects.create(user=self.user, action="Logged out")

    def test_activity_log_view(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

        # Access the activity log view
        response = self.client.get(reverse("activity_log"))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the rendered template contains the user's activity log entries
        self.assertContains(response, "Visited /dashboard/")
        self.assertContains(response, "Logged out")

        # Check that the context contains the activity_log queryset
        self.assertTrue("activity_log" in response.context)
        activity_log = response.context["activity_log"]
        self.assertEqual(activity_log.count(), 2)

    def test_activity_log_view_not_logged_in(self):
        # Log out the test user (if logged in)
        self.client.logout()

        # Access the activity log view without logging in
        response = self.client.get(reverse("activity_log"))

        # Check that the response status code is 302 (redirect to login)
        self.assertEqual(response.status_code, 302)

        # Check that the user is redirected to the login page
        self.assertRedirects(
            response, reverse("log_in") + "?next=" + reverse("activity_log")
        )

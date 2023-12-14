from django.test import TestCase, Client
from tasks.models import Task, Team, User
from django.urls import reverse
from django.test import RequestFactory


class DeleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='@personA', password='Password123')
        self.client = Client()
        self.client.login(username='@personA', password='Password123')

        self.task_assigned_to_user = Task.objects.create(assignee=self.user, maker='@other_user', due_date="2024-11-10 12:13",)
        self.taskID = self.task_assigned_to_user.id

        self.task_created_by_user = Task.objects.create(assignee='@other_user', maker=self.user.username, due_date="2024-11-10 12:13",)


    def test_delete_task(self):
        initial_task_count = Task.objects.count()
        response = self.client.post(reverse(f'dashboard_delete', args=[self.taskID]))
        self.assertEqual(Task.objects.count(), initial_task_count - 1)

        userData = response.context['data']
        myCreatedTasks = response.context['createdTasks']

        self.assertNotIn(self.task_assigned_to_user, userData)
        self.assertIn(self.task_created_by_user, myCreatedTasks)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.taskID)



    def tearDown(self):
        self.client.logout()

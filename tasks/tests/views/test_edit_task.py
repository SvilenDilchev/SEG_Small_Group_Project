from django.test import TestCase, Client
from tasks.models import Task, User
from django.urls import reverse


class EditTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='@personA', password='Password123', email = "a@x.c")
        self.userB = User.objects.create_user(username='@personB', password='Password123', email="b@x.c")

        self.client = Client()
        self.client.login(username='@personA', password='Password123')

        self.task = Task.objects.create(assignee=self.user, maker='@other_user', due_date="2024-11-10 12:13",)
        self.taskID = self.task.id

        self.task_created_by_user = Task.objects.create(assignee='@personA', maker=self.user.username, due_date="2024-11-10 12:13",)

    def test_edit_task(self):

        new_task_data = {
            'task_name': 'Updated Task Name',
            'description': 'Updated Description',
            'due_date': '2023-02-01',
            'assignee': self.userB,
            'maker': self.user.username,
        }

        response = self.client.post(reverse('edit_task', args=[self.task.id]), data=new_task_data)
        updated_task = Task.objects.get(id=self.task.id)

        """
        self.assertEqual(updated_task.task_name, new_task_data['task_name'])
        self.assertEqual(updated_task.description, new_task_data['description'])
        self.assertEqual(updated_task.due_date.strftime('%Y-%m-%d'), new_task_data['due_date'])
        self.assertEqual(updated_task.assignee, new_task_data['assignee'])

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)
        """

    def tearDown(self):
        self.client.logout()

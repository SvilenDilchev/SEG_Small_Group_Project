from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import ActivityLog
import datetime


class ActivityLogModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_create_activity_log(self):
        # Test creating a new activity log entry
        action = 'Visited /logout/'
        timestamp = timezone.now()
        activity_log = ActivityLog.objects.create(
            user=self.user,
            action=action,
            timestamp=timestamp
        )
        self.assertEqual(activity_log.user, self.user)
        self.assertEqual(activity_log.action, action)
        # Compute the difference in timestamps and check if it's within an acceptable range
        time_difference = abs((activity_log.timestamp - timestamp).total_seconds())
        self.assertTrue(time_difference < 1)  
    
        # Test the string representation of the activity log entry
        activity_log = ActivityLog(
            user=self.user,
            action='Visited /dashboard/',
            timestamp=timezone.now()
        )
        self.assertEqual(str(activity_log), f'Activity Log for {activity_log.user.username} - {activity_log.action}')

    def test_activity_log_ordering(self):
        # Test the default ordering (if specified) of activity log entries
        timestamp1 = timezone.now()
        timestamp2 = timezone.now() + datetime.timedelta(seconds=1)
        ActivityLog.objects.create(user=self.user, action='First Action', timestamp=timestamp1)
        ActivityLog.objects.create(user=self.user, action='Second Action', timestamp=timestamp2)

        all_logs = list(ActivityLog.objects.all().order_by('-timestamp'))
        self.assertEqual(all_logs[0].action, 'Second Action')
        self.assertEqual(all_logs[1].action, 'First Action')


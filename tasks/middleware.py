from django.utils import timezone
from .models import ActivityLog
from django.urls import resolve


class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is authenticated and the path does not end with a static file extension
        if request.user.is_authenticated and not request.path.lower().endswith(('.css', '.js', '.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
            view = resolve(request.path_info).url_name
            view_name = view.replace('_',' ')
            #Log the activity
            activity = ActivityLog(user = request.user, action = f'Visited {view_name}', timestamp = timezone.now())

            activity.save()

        return response

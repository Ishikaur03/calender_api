# calendar_integration/urls.py
from django.urls import path
from calendar_integration.views import GoogleCalendarInitView, GoogleCalendarRedirectView

app_name = 'calendar_integration'

urlpatterns = [
    path('init/', GoogleCalendarInitView.as_view(), name='calendar_init'),
    path('redirect/', GoogleCalendarRedirectView.as_view(), name='calendar_redirect'),
]
# from django.urls import path
# from .views import GoogleCalendarInitView, GoogleCalendarRedirectView

# urlpatterns = [
#     path('rest/v1/calendar/init/',
#          GoogleCalendarInitView.as_view(), name='calendar_init'),
#     path('rest/v1/calendar/redirect/',
#          GoogleCalendarRedirectView.as_view(), name='calendar_redirect'),
   
# ]

#from django.shortcuts import render

# Create your views here.
# calendar_integration/views.py
# calendar_integration/views.py
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'credentials.json'),
            scopes=SCOPES,
            redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        request.session['state'] = state
        return HttpResponseRedirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session.get('state', '')
        flow = Flow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'credentials.json'),
            scopes=SCOPES,
            redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/',
            state=state
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        

        if credentials.refresh_token is None:
            credentials.refresh(Request())

        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        return HttpResponse(events)


# #calendar_integration/views.py
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views import View
# from google.oauth2 import credentials
# from google_auth_oauthlib.flow import Flow
# import googleapiclient.discovery

# # Constants for Google OAuth 2.0
# CLIENT_ID = '373716330603-br5h9t959iohh5v2v0tcuhu694hl1upl.apps.googleusercontent.com'
# CLIENT_SECRET = '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'
# SCOPE = 'https://www.googleapis.com/auth/calendar.readonly'
# REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'
# CREDENTIALS_FILE = 'credentials.json'

# class GoogleCalendarInitView(View):
#     def get(self, request):
#         flow = Flow.from_client_secrets_file(
#             CREDENTIALS_FILE,
#             scopes=[SCOPE],
#             redirect_uri=REDIRECT_URI
#         )
#         authorization_url, _ = flow.authorization_url(prompt='consent')

#         return redirect(authorization_url)

# class GoogleCalendarRedirectView(View):
#     def get(self, request):
#         flow = Flow.from_client_secrets_file(
#             CREDENTIALS_FILE,
#             scopes=[SCOPE],
#             redirect_uri=REDIRECT_URI
#         )
#         flow.fetch_token(
#             authorization_response=request.build_absolute_uri(),
#         )

#         credentials_dict = flow.credentials
#         access_token = credentials_dict.token

#         service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials.Credentials.from_authorized_user_info(credentials_dict))

#         events_result = service.events().list(calendarId='primary', maxResults=10).execute()
#         events = events_result.get('items', [])

#         # Process the fetched events as per your requirement
#         # ...

#         return HttpResponse('Events fetched successfully')
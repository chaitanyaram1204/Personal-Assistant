import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/tasks"]

def add_event(data):
    print(data)
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES) //USE your credentials file
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": data[0],
            "location": data[1],
            "description": "This is a test event",
            "colorId": 1,
            "start": {"dateTime": data[2], "timeZone": "(GMT+5:30)Kolkata"},  # Set the time zone to IST
            "end": {"dateTime": data[3], "timeZone": "(GMT+5:30)Kolkata"},    # Set the time zone to IST
            "attendees": [
                {"email": "ATTENDEES MAIL"},
                {"email": "ATTENDEES MAIL"},
                {"email": "ATTENDEES MAIL"}
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 30},
                    {"method": "email", "minutes": 60}
                ]
            }
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        print("Event created: %s" % (event.get("htmlLink")))

    except HttpError as e:
        print("An error occurred", e)

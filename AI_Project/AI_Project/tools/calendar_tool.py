# AI_Project/tools/calendar_tool.py
import os
from datetime import datetime, timedelta
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except Exception:
    service_account = None
    build = None

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarTool:
    def __init__(self):
        sa_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
        if not sa_file or not os.path.exists(sa_file):
            self.creds = None
            self.service = None
            print('Warning: GOOGLE_SERVICE_ACCOUNT_FILE not found; calendar functions will not work until configured.')
            return
        if not service_account or not build:
            self.creds = None
            self.service = None
            print('Warning: google-api-client not installed or import failed.')
            return
        creds = service_account.Credentials.from_service_account_file(sa_file, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=creds)
        self.calendar_id = os.environ.get('GOOGLE_CALENDAR_ID','primary')

    def list_events(self, time_min=None, time_max=None, max_results=10):
        if not getattr(self, 'service', None):
            return 'Calendar not configured.'
        if time_min is None:
            time_min = datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=time_min,
                                                   maxResults=max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return '\n'.join([f"{e.get('start').get('dateTime','')}: {e.get('summary')}" for e in events])

    def create_event(self, summary, start_iso, length_minutes=60, attendees=None):
        if not getattr(self, 'service', None):
            raise RuntimeError('Calendar not configured. Set GOOGLE_SERVICE_ACCOUNT_FILE')
        # Accept either '2025-09-10 14:00' or ISO format
        if 'T' not in start_iso and ' ' in start_iso:
            start_iso = start_iso.replace(' ', 'T')
        start_dt = datetime.fromisoformat(start_iso)
        end_dt = start_dt + timedelta(minutes=length_minutes)
        event = {
            'summary': summary,
            'start': {'dateTime': start_dt.isoformat()},
            'end': {'dateTime': end_dt.isoformat()},
            'attendees': [{'email': a} for a in (attendees or [])],
        }
        created = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return f"Created event: {created.get('htmlLink')}"

    def run(self, query: str):
        if query.startswith('list upcoming'):
            return self.list_events()
        elif query.startswith('create event'):
            parts = query.split('|')
            if len(parts) < 4:
                return 'create event|Summary|ISO_START|DURATION_MINS|optional_comma_sep_attendees'
            _, summary, start_iso, length = parts[:4]
            attendees = parts[4].split(',') if len(parts) > 4 and parts[4] else []
            return self.create_event(summary, start_iso, int(length), attendees)
        else:
            return 'Calendar tool: unknown command'

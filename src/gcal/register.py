#!/usr/bin/env python
from __future__ import print_function
import datetime
import pickle
from os.path import dirname, exists, realpath
from pprint import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Where our credentials and tokens live
PRIVATE_PATH = "{}/{}".format(dirname(dirname(dirname(realpath(__file__)))), "private")

# OAuth scopes required to do the needful
# Delete private/token.pickle and run this script to re-run the oauth flow
Config = {
    "calendar": {
        "token_file": "{}/{}".format(PRIVATE_PATH, "cal.token.pickle"),
        "creds_file": "{}/{}".format(PRIVATE_PATH, "credentials.json"),
        "scopes": [
            "https://www.googleapis.com/auth/calendar.readonly",
        ]
    },
}


class GCal(object):
    """
    The Google API python client is documented in:
        * API Ref: https://developers.google.com/calendar/
    """

    def __init__(self):
        c = Config["calendar"]
        self.cal_creds = self._get_creds(c["creds_file"], c["scopes"], c["token_file"])
        self.cal_svc = build("calendar", "v3", credentials=self.cal_creds)

    def _get_creds(self, cred_file_path, scopes, token_file_path):
        """
        Run OAuth flow and connect to a calendar

        To register our connected app against a G Suite deployment:
            1. Delete token.pickle
            2. Run this script
            3. Sign into proper G Suite account
            4. Accept perms listed above, auth the app
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if exists(token_file_path):
            with open(token_file_path, "rb") as token:
                creds = pickle.load(token)
    
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cred_file_path, scopes)
                creds = flow.run_local_server(port=0)
        
            # Save the credentials for the next run
            with open(token_file_path, "wb") as token:
                pickle.dump(creds, token)
    
        return creds

    def get_events(self):
        """
        Notes:
            * returns only files from my_drive - which we don't really care about
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        
        print('Getting the upcoming 10 events')
        results = (
            self.cal_svc.events().list(calendarId='primary', timeMin=now,
                                       maxResults=10, singleEvents=True,
                                       orderBy='startTime').execute()
        )
        
        events = results.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        print("===> Raw response data")
        pprint(results)


def main():
    cal = GCal()
    cal.get_events()
    
    # """Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.
    # """
    # creds = None
    # # The file token.pickle stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)
    #
    # service = build('calendar', 'v3', credentials=creds)
    #
    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                       maxResults=10, singleEvents=True,
    #                                       orderBy='startTime').execute()
    # events = events_result.get('items', [])
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


if __name__ == '__main__':
    main()

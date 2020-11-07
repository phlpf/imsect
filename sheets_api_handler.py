# Environment to get tokens
import dotenv as de
import os

# Sheets API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Get tokens
de.load_dotenv()

signing_secret = os.getenv("SIGNING_SECRET")
sheet_id = os.getenv("SHEET_ID")

import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = sheet_id
SAMPLE_RANGE_NAME = 'A2:E2'

class SheetHandler:
    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()
    def write(self, values, range_name):
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()

columns = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def data_to_range(values):
    height = len(values)
    max_width = 0
    for row in values:
        if len(row) > max_width:
            max_width = len(row)
    return "A1:" + columns[max_width] + str(height)

    
if __name__ == '__main__':
    sh = SheetHandler()
    data = [["h", "e", "l", "l", "o",""],
            [",","","","","",""],
            ["w","o","r","l","d","!"]]
    sh.write(data, data_to_range(data))
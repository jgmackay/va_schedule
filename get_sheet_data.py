#!/usr/bin/python3
from __future__ import print_function

import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1bM65IR2kNCIz0u9CR56V_GO4UbFtdmkYPhQvf05PLqI' 
SAMPLE_SPREADSHEET_ID = '1Ve7LHUipFhjDwQzRRK_Qa-jDiBW7lpBKsI9ZAtGiwwA'
SAMPLE_RANGE_NAME = 'Fall \'23!A1:H'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    try:
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        df = pd.DataFrame(values)


        # Write out to HTML
        html_file = open("spreadsheet_data.html", "w")
        html_file.writelines(df.to_html())
        html_file.close()
        print("Successfully wrote output to spreadsheet_data.html")

        # Write out to JSON
        json_file = open("spreadsheet_data.json", "w")
        json_file.writelines(df.to_json())
        json_file.close()
        print("Successfully wrote output to spreadsheet_data.json")

        #if not values:
        #    print('No data found.')
        #    return

        #for row in values:
        #    # Print columns A and E, which correspond to indices 0 and 4.
        #    print('%s, %s' % (row[0], row[1]))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()

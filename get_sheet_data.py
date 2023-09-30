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
#SPREADSHEET_ID = '1bM65IR2kNCIz0u9CR56V_GO4UbFtdmkYPhQvf05PLqI' 
SPREADSHEET_ID = '1Ve7LHUipFhjDwQzRRK_Qa-jDiBW7lpBKsI9ZAtGiwwA'
SHEET_NAMES_AND_RANGE = [ 
        ('Fall \'23', '!A1:H'),
        ('Didactics', '!A1:J'),
        ('Clinic Names', '!A1:X'),
        ('NewPt Clinic', '!A1:M'),
        ('Weds Resdt Amb Talks', '!A1:N'),
        ('Spring \'24', '!A1:J')
                        ]


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    try:
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # Loop over each sheet in the spreadsheet
        for name_and_range in SHEET_NAMES_AND_RANGE:
            name = name_and_range[0]
            rng = name_and_range[1]

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=(name+rng)).execute()
            values = result.get('values', [])
            df = pd.DataFrame(values)


            # Write out to HTML
            filename = name.replace(' ', '_')
            html_file = open(filename+".html", "w")
            html_file.writelines(df.to_html())
            html_file.close()
            print("Successfully wrote output to "+filename+".html")

            # Write out to JSON
            json_file = open(filename+".json", "w")
            json_file.writelines(df.to_json())
            json_file.close()
            print("Successfully wrote output to "+filename+".json")

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

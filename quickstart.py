# imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import sys
import os
from sort import sort

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

subjects = []

# holds id for folders
folder_ids = {}

# initializes creds to None
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Call the Drive v3 API
service = build('drive', 'v3', credentials=creds)

# If folders are already created and stored in requirements.txt,
# read them from requirements.txt and store them in ids.
# If not, create folders and put ids in ids.
def createFolder():
    global subjects
    global folder_ids

    # Subjects (folders)
    subjects = ["Science", "Math", "History", "Language Arts"]

    # Opens requirements.txt
    f = open("requirements.txt", "r+")
    filesize = os.path.getsize("requirements.txt")
    ids = []
    if filesize == 0:
        # If requirements.txt is empty, make folders and get id
        for subject in subjects:
            file_metadata = {
                'name': subject,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            file = service.files().create(body=file_metadata,
                                            fields='id').execute()
            id = file.get('id')
            ids.append(id)
            f.write(id + "\n")
    else:
        # Else, read ids from requirements.txt into ids array
        ids = [id.replace("\n", "") for id in f.readlines()]

    # Fill dict folder_ids with subjects as the keys and the ids as the values
    for i in range(len(subjects)):
        folder_ids[subjects[i]] = ids[i]

# Create shortcut to file from folder
def createShortcut(file_id, folder_id):
    file = service.files().get(fileId=file_id, fields='id, parents, name').execute()
    shortcut_metadata = {
        'Name': file.get('name'),
        'mimeType': 'application/vnd.google-apps.shortcut',
        'shortcutDetails': {
            'targetId': file_id
        }
    }
    shortcut = service.files().create(body=shortcut_metadata,
                                      fields='id,shortcutDetails').execute()
    service.files().update(fileId=shortcut.get('id'),
                           addParents=folder_id,
                           fields='id, parents',).execute()

# Creates folders if not already created
# If folders are already created, get IDs from requirements.txt
createFolder()
page_token = None

# Loops over all files
while True:
    response = service.files().list(q="mimeType='application/vnd.google-apps.document'" or "mimeType='application/vnd.google-apps.drawing'" or "mimeType='application/vnd.google-apps.form'" or "mimeType='application/vnd.google-apps.presentation'" or "mimeType='application/vnd.google-apps.spreadsheet'",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        datecreated_split_temp = service.files().get(fileId=file.get(
            'id'), fields="createdTime").execute()['createdTime'].split('-')
        yearvariable = datecreated_split_temp[0]

        datetime_obj = datetime.datetime.now()

        # Checks if file has been created/last modified within the last year
        if (int(datetime_obj.year)-1) <= (int(yearvariable)):
            # Uses sort function to get the subject for the file based on file name
            folder_name = sort(file.get('name'), subjects)
            # Print the file name and the folder name
            print(f"{file.get('name')} - {folder_name}")
            # Create shortcut to file in folder
            createShortcut(file.get('id'), folder_ids[folder_name])

    # If no more pages, end
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break

print("Task completed! :)")

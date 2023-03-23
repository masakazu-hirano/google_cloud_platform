import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

credential = None
if os.path.exists('token.json'):
  credential = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive.metadata.readonly'])

if not credential or not credential.valid:
  if credential and credential.expired and credential.refresh_token:
    credential.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive.metadata.readonly'])
    credential = flow.run_local_server(port=0)

    with open('token.json', 'w') as token_file:
      token_file.write(credential.to_json())

try:
  items = build('drive', 'v3', credentials=credential).files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute().get('files', [])

  print('Files:')
  for item in items:
    print(u'{0} ({1})'.format(item['name'], item['id']))
except HttpError as error:
  print(f'An error occurred: {error}')

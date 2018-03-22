import os

from apiclient import discovery, errors
from oauth2client import file, client, tools
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from settings import CREDENTIAL_DIR, SCOPES, CLIENT_SECRET_FILE, DRIVE_STORAGE_NAME

class AppDriveApiClient(object):
    def __init__(self):
        # client authorization
        if not os.path.exists(CREDENTIAL_DIR):
            os.makedirs(CREDENTIAL_DIR)

        credential_path = os.path.join(CREDENTIAL_DIR,
                                       'storage.json')
        store = file.Storage(credential_path)
        creds = store.get()  # Gets valid user credentials from storage.
        if not creds or creds.invalid:  # if nothing has been stored,
            #  or if the stored credentials are invalid, ...

            flow = client.flow_from_clientsecrets(
                os.path.join(CREDENTIAL_DIR, CLIENT_SECRET_FILE), SCOPES)
            creds = tools.run_flow(flow, store)  # ... the OAuth2 flow is
            # completed to obtain the new credentials

        # creation service object, takes api name, api version, instance of
        # httplib2.Http or something that acts like it that HTTP
        # requests will be made through.
        self.service = discovery.build('drive', 'v3',
                                       http=creds.authorize(Http()))
        self.storage_id = self._choose_or_create_storage_dir()

    def _choose_or_create_storage_dir(self):
        """
        Choose or Creation folder for storing application data. Return id
        of this folder.
        :return: string with folder id
        """
        try:
            app_folder = self.service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and name='Video Monitoring System Storage'").execute().get(
            'files', [])
        except Exception as e:
            print('Something went wrong on choosing application folder', e)
        if not app_folder:

            file_metadata = {
                'name': 'Video Monitoring System Storage',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            try:
                app_folder = self.service.files().create(body=file_metadata,
                                                     fields='id').execute()
            except Exception as e:
                print('Something went wrong on creation application folder', e)
            print('Application folder was created on the drive')
        storage_id = app_folder[0].get('id')
        return storage_id

    def show_app_files_list(self):
        """
        Showing all files in drive application storage

        """
        files = self.service.files().list(
            spaces='drive').execute().get('files', [])
        if len(files) > 1:
            print('Video Monitoring System Storage content:')
        else:
            print('Video Monitoring System Storage is empty')
        for file in files:
            if not file['mimeType']=='application/vnd.google-apps.folder':
                print(file['name'], file['mimeType'])

    def upload_file_to_drive(self, path_to_file, new_file_name):
        """
        Uploading file from current path in google drive application
        data folder.
        :param path_to_file: string with path;
        new_file_name: string
        """
        file_metadata = {'name': new_file_name, 'parents': [self.storage_id]}
        media = MediaFileUpload(path_to_file)
        self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        print('File %s was uploaded' % new_file_name)

    def upload_files_to_drive(self, path_to_dir):
        """
        Uploading all files from some directory in google drive application
        data folder.
        :param path_to_dir: string with path

        """
        for file in os.listdir(path_to_dir):
            path_to_file = os.path.join(path_to_dir, file)
            file_metadata = {'name': file, 'parents': [self.storage_id]}
            media = MediaFileUpload(path_to_file)
            self.service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    def clean_app_folder(self):
        """
        Removing all files from google drive application folder

        """
        files = self.service.files().list(
            spaces='drive').execute().get('files', [])
        for file in files:
            if not file['mimeType'] == 'application/vnd.google-apps.folder':
                file_id = file['id']
                self.service.files().delete(fileId=file_id).execute()
                print('File %s was removed from Video Monitoring System Storage' % file['name'])

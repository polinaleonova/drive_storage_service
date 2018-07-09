import os

from apiclient import discovery, errors
from oauth2client import file, client, tools
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from settings import CREDENTIAL_DIR, SCOPES, CLIENT_SECRET_FILE, \
    DEFAULT_STORAGE_NAME


class AppDriveApiClient(object):

    def __init__(self, custom_name_folder=None):
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
        self.storage_id = self._choose_or_create_storage(custom_name_folder)

    def _choose_or_create_storage(self, custom_name_folder=None):
        """
        Choose or Creation folder for storing application data. Return id
        of this folder.
        :param custom_name_folder: if None - use default folder
            'Video Monitoring System Storage', else string with your
            custom folder name
        :return: string with folder id
        """
        app_folders = []
        self.name_folder = custom_name_folder or DEFAULT_STORAGE_NAME

        try:
            app_folders = self.service.files().list(
                q="mimeType='application/vnd.google-apps.folder' and name='" + self.name_folder + "'").execute().get(
                'files', [])
        except Exception as e:
            print('Something went wrong on choosing application folder', e)

        if not app_folders:
            file_metadata = {
                'name': self.name_folder,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            try:
                app_folder = self.service.files().create(body=file_metadata,
                                                         fields='id').execute()
                storage_id = app_folder.get('id')
            except Exception as e:
                print('Something went wrong on creation application folder', e)
            print("Application folder '{}' was created on the drive".format(
                self.name_folder))
        else:
            storage_id = app_folders[0].get('id')
        return storage_id

    def show_app_files_list(self):
        """
        Showing all files in drive application storage

        """
        files = self.service.files().list(
            spaces='drive', q="'" + self.storage_id + "' in parents").execute().get('files', [])
        if len(files) > 1:
            print(self.name_folder + ' content:')
            for f in files:
                if not f['mimeType'] == 'application/vnd.google-apps.folder':
                    print(f['name'], f['mimeType'])
        else:
            print(self.name_folder + ' is empty')

    def upload_file_to_drive(self, path_to_file, new_file_name):
        """
        Uploading file from current path to google drive application
        data folder.
        :param path_to_file: string with absolute path to file;
        new_file_name: string
        """
        if not os.path.exists(path_to_file):
            print("File '" + path_to_file + "' not found")
        else:
            file_name = new_file_name or os.path.basename(
                path_to_file.split('.')[0])  # without extension
            file_metadata = {'name': file_name, 'parents': [self.storage_id]}
            media = MediaFileUpload(path_to_file)
            self.service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            print('File %s was uploaded to storage' % file_name)

    def upload_files_to_drive(self, path_to_dir):
        """
        Uploading all files from some directory to google drive application
        data folder.
        :param path_to_dir: string with absolute path to directory

        """
        count = 0
        if not os.path.isdir(path_to_dir):
            print("Directory '" + path_to_dir + "' not found")
        else:
            for f in os.listdir(path_to_dir):
                path_to_file = os.path.join(path_to_dir, f)
                file_metadata = {'name': f, 'parents': [self.storage_id]}
                media = MediaFileUpload(path_to_file)
                self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
                count += 1
            print(str(count) + " files were uploaded to application storage")

    def clean_app_folder(self):
        """
        Removing all files from google drive application folder

        """
        files = self.service.files().list(
            spaces='drive',
            q="'" + self.storage_id + "' in parents").execute().get('files',
            [])
        count = 0
        for f in files:
            if not f['mimeType'] == 'application/vnd.google-apps.folder':
                file_id = f['id']
                file_name = f['name']
                self.service.files().delete(fileId=file_id).execute()
                print(("File {} was removed from " + self.name_folder).format(
                    file_name))
                count += 1
        print(str(count) + " files were removed from application storage")


# demo
if __name__ == "__main__":
    print("Init google drive client...")
    drive_fold_name = input("Type in name of folder in google drive "
                            "for your application data or press Enter "
                            "if you want to use default name\n>>>")
    drive_client = AppDriveApiClient(drive_fold_name)
    drive_client.show_app_files_list()

    filepath = input(
        "Type in absolute path to your local file for uploading\n>>>")

    filename = input(
        "Type in new name (without extension) for uploaded "
        "file or press Enter for using current name\n>>>")
    drive_client.upload_file_to_drive(filepath, filename)

    path_to_dir = input(
        "Type in absolute path to your local directory for "
        "content uploading\n>>>")
    drive_client.upload_files_to_drive(path_to_dir)

    drive_client.show_app_files_list()

    clean_storage = input(
        "Do you want to remove all files from current "
         "application storage? y/n\n>>>")
    if clean_storage == 'y':
        drive_client.clean_app_folder()
For authentication and authorization application you need:

Python 3 or greater.
The pip package management tool.
Access to the internet and a web browser.
A Google account with Google Drive enabled.

Step 1: Turn on the Drive API
Use this wizard - https://console.developers.google.com/start/api?id=drive to create or
select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
On the Add credentials to your project page, click the Cancel button.
At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set,
and click the Save button.
Select the Credentials tab, click the Create credentials button and select OAuth client ID.
Select the application type Other, enter the name "your application name", and click the Create button.
Click OK to dismiss the resulting dialog.
Click the file_download (Download JSON) button to the right of the client ID.
Create directory '.credentials' and add path to this directory in CREDENTIAL_DIR in your settings.py
Move json file to this directory and rename it to client_secret.json.
In your settings.py choose SCOPES value:

a)'https://www.googleapis.com/auth/drive.file'
If you use this scopes you can use for files uploading only folders which was created by your application (not by google drive user)

b)'https://www.googleapis.com/auth/drive'
If you use this scopes you can use for files uploading any folders in google drive,
 but you should know that this google drive client will be read/write access to all drive content

To enable the Drive API, complete these steps:

-Go to the Google API Console.
-Select a project.
-In the sidebar on the left, expand APIs & auth and select APIs.
-In the displayed list of available APIs, click the link for the Google Drive API and click Enable API.

Step 2: Install the Google Client Library
Run the following command to install the library using pip:

pip install --upgrade google-api-python-client

After all this steps, when you run firstly you application:
1. run in console: python3 google_drive_service.py --noauth_local_webserver
You will see in your console output:

Init google drive client...
Type name of folder in google drive
for your application data or press Enter if you want to use default name
>>>

2. Type existing folder name from your google drive or
 new name (new folder will be created on drive) or press Enter for using DEFAULT_STORAGE_NAME from settings.py

first time you get this message in console:
Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?redirect_uri=...

2.Enter verification code:

- You should go to this link in browser and check account (which related with you application)
- than you should choose 'Agree' with proposals to share you data with application "your application name"
- Than you get code, and you should to fill this code in console input 'Enter verification code:'
- You will get:
Authentication successful. You can see new file storage.json in your CREDENTIAL_DIR.

After this your application folder will be selected for uploading files or created in drive.
 And app can work with this folder's data.

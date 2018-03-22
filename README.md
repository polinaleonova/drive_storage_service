For authentication and authorization application you need:

Python 3 or greater.
The pip package management tool.
Access to the internet and a web browser.
A Google account with Google Drive enabled.

Step 1: Turn on the Drive API
Use this wizard - https://console.developers.google.com/start/api?id=drive to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
On the Add credentials to your project page, click the Cancel button.
At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
Select the Credentials tab, click the Create credentials button and select OAuth client ID.
Select the application type Other, enter the name "Drive API Quickstart", and click the Create button.
Click OK to dismiss the resulting dialog.
Click the file_download (Download JSON) button to the right of the client ID.
Create directory '.credentials' and add path to this directory in CREDENTIAL_DIR
Move json file to this directory and rename it client_secret.json.

Step 2: Install the Google Client Library
Run the following command to install the library using pip:

pip install --upgrade google-api-python-client


After all this steps, when you run firstly you application:
1. run in console: python3 google_drive_service.py --noauth_local_webserver
first time you get this in console:
Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?redirect_uri=...

Enter verification code:


2. You should go to this link in browser and check account (which related with you application)
3. than you should choose 'Agree' with proposals to share you data with application "Video Monitoring Storage"
4. Than you get code, and you should to fill this code in console input 'Enter verification code:'
5. You will get:
Authentication successful.

After this your application folder will be created in drive. And app can work with this folder's data.

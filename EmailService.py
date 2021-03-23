from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
# Ref: https://developers.google.com/gmail/api/auth/scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class EmailService:
    def __init__(self):
        self.service = self.get_service()
        self.message = None

    def get_service(self):
        """Build the API service

        Returns:
          A service instance
        """
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
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def create_message_with_attachment(self, sender, to, subject, message_text, file):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
          file: The path to the file to be attached.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        # return {'raw': base64.urlsafe_b64encode(message.as_string())}
        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode()
        body = {'raw': b64_string}
        return body

    def send_message(self):
        """Send an email message.

        Returns:
          The Sending result with a return message.
        """
        try:
            message = (self.service.users().messages().send(userId="me", body=self.message).execute())
            # print('Message Id: %s' % message['id'])
            return True, message

        except errors.HttpError as error:
            # print('An error occurred: %s' % error)
            return False, error

    def send_image(self, to, subject, text, image):
        """Send an email message with an image attachment.

        Args:
          to: Email address of the receiver.
          subject: The subject of the email message.
          text: The text of the email message.
          image: The path to the image to be attached.

        Returns:
          The Sending result with a return message.
        """
        profile = self.service.users().getProfile(userId='me').execute()
        self.message = self.create_message_with_attachment(profile.get('emailAddress'), to, subject, text, image)
        return self.send_message()


if __name__ == '__main__':
    # main()
    service = EmailService()
    is_successful, message = service.send_image('', 'subject', 'hello', 'icon.png')

    if is_successful:
        print('sent')
    else:
        print('fail: ', message)

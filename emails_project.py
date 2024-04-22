import imaplib
import email
import re
from time import sleep
from twilio.rest import Client

#setting up imap server
imap_server = 'imap.gmail.com'
email_address = '[YOUR_EMAIL_ADDRESS]'
password = '[YOUR_PASSWORD]'

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)
important_addresses = ['[ENTER_DESIRED_ADDRESSES]']

#pick out the email address from the data
def acquire_address(a):
    match = re.search(r'<(.*?)>', a)
    sender_email = match.group(1)
    return sender_email

#check the email addresses against the list
def crossref_emails(sender_email, subject, date):
    for item in important_addresses:
        if sender_email == item:
            print(f'You have an email from {sender_email}')
            text_phone(sender_email, subject, date)

#send text function
def text_phone(sender_email, subject, date):
    twilio_account_sid = '[YOUR_TWILIO_SID]'
    twilio_auth_token = '[YOUR_TWILIO_AUTH]'

    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        to = '[YOUR_PHONE_NUMBER]',
        from_ = '[YOUR_TWILIO_NUMBER]',
        body = f'You have received an email from {sender_email}\nSubject: {subject}\nDate: {date}'
        )


#scan the email inbox
def scan_emails():

    while True:
        print("Scanning...")
        imap.select("Inbox")
        _, msgnums = imap.search(None, 'UNSEEN')

        for msgnum in msgnums[0].split():

            try:
                _, data = imap.fetch(msgnum, "(RFC822)")
                #_, data = imap.uid('FETCH', msgnum, "(RFC822)")

                message = email.message_from_bytes(data[0][1])
                sender = message.get('From')
                sender_email = acquire_address(sender).lower()
                subject = message.get('Subject')
                date = message.get('Date')
            
                crossref_emails(sender_email, subject, date)

            except:
                pass
        sleep(60)


scan_emails()
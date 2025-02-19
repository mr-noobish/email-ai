import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *


def connect_imap():
    
    connected = False
    while not connected:
        try:
            imap = imaplib.IMAP4_SSL(IMAP_SERVER)
            imap.login(EMAIL_ADDRESS, PASSWORD)
            connected = True
        except Exception as e:
            print(e)
            print("reconnecting")
    return imap

def reconnect_imap():
    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap.login(EMAIL_ADDRESS, PASSWORD)
        connected = True
    except Exception as e:
        print(e)
        print("reconnecting")

def receive_email(imap):
    try:
        imap.select("Inbox")
        _, msgnums = imap.search(None, "UNSEEN")
        if not msgnums[0]:
            return [], [], []
        
        user_email_list = []
        subject_list = []
        prompt_list = []

        for msgnum in msgnums[0].split():
            _, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_bytes(data[0][1])
            user_email_list.append(message.get('From'))
            subject_list.append(message.get('Subject'))
            prompt = ""
            for part in message.walk():
                if part.get_content_type() == "text/plain" and not part.is_multipart():
                    charset = part.get_content_charset() or "utf-8"
                    prompt += part.get_payload(decode=True).decode(charset, errors="ignore")
            prompt_list.append(prompt)
        return user_email_list, subject_list, prompt_list
    except Exception as e:
        print(f"Error in receive_email: {e}")
        return [], [], []

def send_email(from_addr, to_addr, message, subject):

    smtp = smtplib.SMTP_SSL(SMTP_SERVER)
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, PASSWORD)
    print("connected")
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    smtp.sendmail(from_addr, to_addr, text)
    smtp.quit()
    print("disconnected")
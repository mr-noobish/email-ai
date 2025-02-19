import json

with open("info.json", 'r') as f:
    info = json.load(f)
    EMAIL_ADDRESS = info['email']
    PASSWORD = info['pass']
    MODEL = info['model']
SMTP_SERVER = "smtp.gmail.com"
IMAP_SERVER = "imap.gmail.com"
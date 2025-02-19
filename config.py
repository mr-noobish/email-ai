import json

with open("account.json", 'r') as f:
    info = json.load(f)
    EMAIL_ADDRESS = info['email']
    PASSWORD = info['pass']
SMTP_SERVER = "smtp.gmail.com"
IMAP_SERVER = "imap.gmail.com"
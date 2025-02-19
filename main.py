import imaplib
import threading
import handle
import mail
from sql import User, session

def thread_func():
    while True:
        command = input(">>>")
        handle.handle_repl(command)


imap = mail.connect_imap()


def is_imap_connected(imap):
    try:
        imap.noop()
        return True
    except imaplib.IMAP4.error as e:
        print(f"IMAP connection lost: {e}")
        return False


thread = threading.Thread(target=thread_func)
thread.start()

while True:
    if not is_imap_connected(imap):
        imap = mail.connect_imap()
    user_list, subject_list, message_list = mail.receive_email(imap)
    if not user_list:
        continue
    for user_email, subject, message in zip(user_list, subject_list, message_list):
        try:
            results = session.query(User).filter(User.email_addr == user_email).all()
        except:
            results = []
        if len(results) > 1:
            raise Exception("Multiple users found with the same email address.")
        result = results[0] if results else None
        if subject == "help:":
            handle.handle_subject(subject, user_email, message)
        elif not result:
            handle.maybe_new_user(user_email, subject, False)
        else:
            handle.handle_subject(subject, user_email, message)

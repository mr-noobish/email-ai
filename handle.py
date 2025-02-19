from mail import send_email
from config import *
from sql import session, User, Conversation
from ai import chain


def new_chat(name, owner):
    chat = Conversation("", owner, name)
    session.add(chat)
    session.commit()
    send_email(EMAIL_ADDRESS, owner, f"""
    Chat "{name}" has been created. To chat in "{name}",
    type "chat: {name}" in the subject of an email.
    """, "Chat Creation")

def suggest_new_user(email_addr):
    send_email(EMAIL_ADDRESS, email_addr, """
    It looks like you are not a registered user.
    To sign up, type "new user:" in the subject of an email
    """, "Unregistered User")

def new_user(email_addr):
    results = session.query(User).filter(User.email_addr == email_addr).all()
    if len(results) > 1:
        raise Exception("heh")
    if len(results) == 1:
        send_email(EMAIL_ADDRESS, email_addr, """
    It seems that you are already a registered user.
    """, "Registered User")
    if len(results) == 0:
        user = User(email_addr, False)
        session.add(user)
        session.commit()
        send_email(EMAIL_ADDRESS, email_addr, """
        You are now a registered user.
        If you did not mean to do this then type "del user:" in the subject of an email
        """, "Registration Confirmation")
    
def maybe_new_user(email_addr, subject, result):
    if not result and subject == "new user:":
        new_user(email_addr)
    else:
        suggest_new_user(email_addr)

def del_user(email_addr):
    results = session.query(User).filter(User.email_addr == email_addr).all()
    result = results[0] if results else None
    try:
        session.delete(result)
    except:
        return
    results = session.query(Conversation).filter(Conversation.owner == email_addr).all()
    result = results[0] if results else None
    try:
        session.delete(result)
    except:
        return
    session.commit()
    send_email(EMAIL_ADDRESS, email_addr, """
    You have been deregistered.
    To reregister type "new user:" in the subject of an email.
    """, "User Deletion")
    

def handle_repl(input):
    command = ""
    arg = ""
    for letter in input:
        command += letter
        if letter != ":":
            continue
        break
    for letter in input[len(command) + 1:]:
        if letter != ":":
            arg += letter
        else:
            break
    if command == "/list users:":
        user_list = ""
        results = session.query(User).all()
        for result in results:
            user_list = user_list + result.email_addr + " - admin="
            user_list += str(result.admin)
            user_list += "\n"
        print(user_list)
    elif command == "/del user:":
        if arg:
            results = session.query(User).filter(User.email_addr == arg).all()
            result = results[0] if results else None
            try:
                session.delete(result)
            except:
                return
            results = session.query(Conversation).filter(Conversation.owner == arg).all()
            result = results[0] if results else None
            try:
                session.delete(result)
            except:
                return
            session.commit()
    elif command == "/reset chat:":
        if arg:
            results = session.query(Conversation).filter(Conversation.name == arg).all()
            result = results[0] if results else None
            try:
                result.context = ""
            except:
                return
            session.commit()
    elif command == "/admin:":
        if arg:
            results = session.query(User).filter(User.email_addr == arg).all()
            result = results[0] if results else None
            try:
                result.admin = True
            except:
                return
            session.commit()
    elif command == "/de-admin:":
        if arg:
            results = session.query(User).filter(User.email_addr == arg).all()
            result = results[0] if results else None
            try:
                result.admin = False
            except:
                return
            session.commit()
    else:
        print("not a command")

def handle_subject(subject, email_addr, message):
    results = session.query(Conversation).filter(Conversation.owner == email_addr)
    print("handling subject")
    command = ""
    arg = ""
    for letter in subject:
        command += letter
        if letter != (":"):
            continue
        break
    for letter in subject[len(command) + 1:]:
        if letter != (":"):
            arg += letter
        else:
            break
    if command == "del user:":
        del_user(email_addr)
    elif command == "new user:":
        new_user(email_addr)
    elif command == "new chat:":
        if arg:
            new_chat(arg, email_addr)
    elif command == "chat:":
        if arg:
            chat = results.filter(Conversation.name == arg).all()[0]
            chat.chat(email_addr, message)
    elif command == "reset chat:":
        if arg:
            chat = results.filter(Conversation.name == arg).all()[0]
            chat.reset_chat(email_addr)
    elif command == "undo:":
        if arg:
            chat = results.filter(Conversation.name == arg).all()[0]
            chat.undo(email_addr)
    elif command.startswith("/") and session.query(User).filter(User.email_addr == email_addr).all()[0].admin == True:
        if command == "/del user:":
            if arg:
                del_user(arg)
        elif command == "/list users:":
            user_list = ""
            results = session.query(User).all()
            for result in results:
                user_list = user_list + result.email_addr + " - admin="
                user_list += str(result.admin)
                user_list += "\n"
            send_email(EMAIL_ADDRESS, email_addr, user_list, "List of Users")
        

    else:
        send_email(EMAIL_ADDRESS, email_addr, """
    Commands:
        "new user:" - registers a user
        "del user:" - deregisters a user
        "chat: chat_name" - chat with bot
        "reset chat: chat_name" - reset chat history
        "undo: chat_name" - undo previous message
        "help:" - displays this message
        """, "Ollama Help")
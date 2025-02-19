from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.mutable import MutableDict
from mail import send_email
from config import *
from ai import chain


Base = declarative_base()





class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    email_addr = Column("email_addr", String)
    admin = Column("admin", Boolean)

    def __init__(self, email_addr, admin):
        self.email_addr = email_addr
        self.admin = admin
    
    def __repr__(self):
        return f"({self.email_addr}), admin={self.admin}"

class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column("name", String)
    context = Column("Context", String)
    owner = Column(String, ForeignKey(User.email_addr))
    #config = Column("config", MutableDict.as_mutable(JSON))

    def __init__(self, context, owner, name):
        self.context = context
        self.owner = owner
        self.name = name

    def __repr__(self):
        return f"(context=({self.context}), owner=({self.owner}))"
    
    def reset_chat(self, email_addr):
        self.context = ""
        session.commit()
        send_email(EMAIL_ADDRESS, email_addr, f"""
        Chat "{self.name}" history reset.
        """, "Reset")

    def chat(self, user_email, message):
        print("chatting")
        response = chain.invoke({"context": self.context, "question": message})
        send_email(EMAIL_ADDRESS, user_email, response, self.name)
        self.context += f"\nUser: {message}\nAI: {response}\t"
        session.commit()
        print("done chatting")

    def stich(self, chat_list):
            msg = '\t'.join(chat_list)
            msg += '\t'
            return msg
    
    def undo(self, user_email):
        split_chat = self.context.split("\t")
        split_chat.pop()
        last = split_chat[-1]
        send_email(EMAIL_ADDRESS, user_email, f"Removed previous message and response from chat '{self.name}'." + "\n\n\n" + last, "Message undone.")
        split_chat.pop()
        conv = self.stich(split_chat)
        self.context = conv
        session.commit()

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
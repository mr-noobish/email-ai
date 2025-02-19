from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from config import *

model = OllamaLLM(model=MODEL)
template = """
You are an AI chatbot. Your objective is to help the user with whatever they need and answer any question they have.

Here is the conversation history: {context}

User prompt: {question}

AI response:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
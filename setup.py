import json

email = input("Email: ")
password = input("App Password: ")
model = input("Model: ")
info = {"email": email, "pass": password, "model": model}
with open("info.json", 'w')as f:
    json.dump(info, f)
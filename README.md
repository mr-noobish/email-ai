# Email AI

Email AI is a tool that lets you interact with an ollama LLM through an email.

## How To Run

First clone the repository.
```bash
git clone https://github.com/mr-noobish/email-ai.git
cd email-ai
```
### Virtual Environment (optional)
At this point you may want to make a virtual enviornment
to avoid version conflicts.
```bash
python3 -m venv .venv
```
On linux use.
```bash
source .venv/bin/activate
```
On windows.
```powershell
.\.venv\Scripts\Activate.ps1
```
### Dependencies
Next, you'll need to install the dependencies.
```bash
pip install sqlalchemy langchain-ollama
```
You'll also need to be running ollama locally.
You can install ollama [here](https://ollama.com/).  
After installing ollama, you need to download an LLM. For example,
```bash
ollama pull llama3.1:8b
```
but you can use any LLM you want.
### Setup
You'll need an email to act as the AI. 
If you haven't made one already, you should do so.

If You're using a Gmail account, you need to make an app password so the program can log into the account.

After that, run
```bash
python3 setup.py
```
and fill in the information.

Now that you're all set, just run
```bash
python3 main.py
```
and you're good to go.

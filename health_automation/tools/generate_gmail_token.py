import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Caminho do arquivo JSON com credenciais
CREDENTIALS_FILE = os.path.join("certs","email.json")
TOKEN_FILE = os.path.join("certs","gmail_token.pickle")

def generate_token():
    """Autentica e gera um token OAuth2 para envio de e-mails via Gmail."""
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            flow.redirect_uri = "http://localhost:5000/"  # Força a URI correta
            creds = flow.run_local_server(port=5000)  # 🚀 Garante que sempre use a mesma porta

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    print("✅ Token OAuth2 gerado com sucesso!")

if __name__ == "__main__":
    generate_token()
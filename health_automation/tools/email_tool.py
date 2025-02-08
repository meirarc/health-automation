from crewai.tools import tool  # Importação correta
import os
import pickle
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Caminho do token OAuth2
TOKEN_FILE = os.path.join("certs", "gmail_token.pickle")

def get_gmail_service():
    """Carrega o token OAuth2 e retorna o serviço Gmail API autenticado."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("⚠️ Token inválido. Rode 'generate_gmail_token.py' novamente.")

    return build("gmail", "v1", credentials=creds)

@tool("send_health_report")  # Apenas o nome da ferramenta, sem `return_direct`
def send_health_report_tool(subject: str, body: str, recipient: str) -> str:
    """Envia um e-mail formatado usando Gmail API e OAuth2."""
    try:
        service = get_gmail_service()

        # Criando a mensagem de e-mail
        message = MIMEMultipart()
        message["to"] = recipient
        message["subject"] = subject
        message.attach(MIMEText(body, "html"))

        # Converte a mensagem para base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Envia o e-mail via Gmail API
        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        
        return "✅ E-mail enviado com sucesso via OAuth2!"
    except Exception as e:
        return f"❌ Erro ao enviar e-mail: {str(e)}"

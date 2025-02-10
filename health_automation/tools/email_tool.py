import os
import markdown2
from crewai.tools import tool
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import pickle
import base64
import json
from health_automation.tools.notion_tool import fetch_notion_user_data
from health_automation.tools.generate_gmail_token import generate_token

TOKEN_FILE = "certs/gmail_token.pickle"

def get_gmail_service():
    """Carrega o token OAuth2 e retorna o serviço Gmail API autenticado."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        print("⚠️ Token inválido ou expirado. Gerando um novo...")

        generate_token()  # 🔹 Gera um novo token automaticamente

        # 🔹 Recarrega o novo token gerado
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
                print("✅ Novo token carregado com sucesso!")
        else:
            raise Exception("❌ Erro: O token não foi gerado corretamente!")

    return build("gmail", "v1", credentials=creds)


@tool("send_email_tool")
def send_email_tool(subject: str, body_markdown: str) -> str:
    """
    Envia um e-mail formatado usando Gmail API e OAuth2. Converte Markdown para HTML antes do envio.
    O destinatário do e-mail é obtido automaticamente do Notion.

    Parâmetros:
    - subject (str): Assunto do email.
    - body_markdown (str): Conteúdo do email em Markdown.

    Retorna:
    - Mensagem de sucesso ou erro.
    """
    try:
        service = get_gmail_service()

        # 🔹 Obtém o email do usuário do Notion
        user_data = fetch_notion_user_data.run()
        user_info = json.loads(user_data)
        recipient = user_info.get("Email", "")

        if not recipient or "@" not in recipient:
            return "❌ Erro: Email do usuário não encontrado no Notion."

        # 🔹 Converte Markdown para HTML com suporte a títulos
        body_html = markdown2.markdown(
            body_markdown, extras=["tables", "fenced-code-blocks"]
        )

        # 🔹 Garantir compatibilidade do Gmail (headers e estilos básicos)
        full_html = f"""
        <html>
        <head>
            <style>
                h1 {{ font-size: 22px; color: #333; }}
                h2 {{ font-size: 20px; color: #555; }}
                h3 {{ font-size: 18px; color: #777; }}
                p  {{ font-size: 16px; color: #000; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {body_html}
        </body>
        </html>
        """

        # 🔹 Criando a mensagem de e-mail
        message = MIMEMultipart()
        message["to"] = recipient
        message["subject"] = subject
        message.attach(MIMEText(full_html, "html"))

        # 🔹 Converte a mensagem para base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # 🔹 Envia o e-mail via Gmail API
        service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()

        return f"✅ E-mail enviado com sucesso para {recipient}!"

    except Exception as e:
        return f"❌ Erro ao enviar e-mail: {str(e)}"

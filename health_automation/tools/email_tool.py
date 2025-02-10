import os
import markdown2
from crewai.tools import tool
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import pickle
import base64

TOKEN_FILE = os.path.join("certs", "gmail_token.pickle")

def get_gmail_service():
    """Carrega o token OAuth2 e retorna o serviço Gmail API autenticado."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        raise Exception("⚠️ Token inválido. Rode 'generate_gmail_token.py' novamente.")

    return build("gmail", "v1", credentials=creds)

def read_agent_output(file_path):
    """Lê o conteúdo do arquivo salvo de um agente."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "🔹 Nenhum dado encontrado."

@tool("send_health_report_tool")
def send_health_report_tool(subject: str, recipient: str) -> str:
    """
    Envia um e-mail formatado usando Gmail API e OAuth2. Converte Markdown para HTML antes do envio.
    """
    try:
        service = get_gmail_service()

        # 🔹 Lendo os arquivos salvos dos agentes
        nutrition_analysis = read_agent_output("data/analyze_nutrition.txt")
        research_summary = read_agent_output("data/research_supplements.txt")

        # 🔹 Criando o corpo do relatório
        body_markdown = f"""
        # 🏥 Relatório de Saúde e Suplementação

        ## 🍏 Análise Nutricional
        {nutrition_analysis}

        ## 📖 Artigos Científicos
        {research_summary}
        """

        # 🔹 Converte Markdown para HTML
        body_html = markdown2.markdown(body_markdown)

        # 🔹 Criando a mensagem de e-mail
        message = MIMEMultipart()
        message["to"] = recipient
        message["subject"] = subject
        message.attach(MIMEText(body_html, "html"))

        # 🔹 Converte a mensagem para base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # 🔹 Envia o e-mail via Gmail API
        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

        return "✅ E-mail enviado com sucesso via OAuth2!"

    except Exception as e:
        return f"❌ Erro ao enviar e-mail: {str(e)}"

import os
import json
import requests
from crewai.tools import tool

# 🔹 Carrega credenciais do Notion
def load_notion_credentials():
    certs_path = os.path.join("certs", "notion.json")
    with open(certs_path, "r") as file:
        return json.load(file)

notion_creds = load_notion_credentials()

NOTION_API_KEY = notion_creds["NOTION_API_KEY"]
NOTION_DATABASE_ID = notion_creds["NOTION_DATABASE_ID"]
NOTION_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

@tool("fetch_notion_supplements_tool")
def fetch_notion_supplements() -> str:
    """Busca TODOS os suplementos no Notion e retorna apenas Nome e Dosagem."""
    try:
        response = requests.post(NOTION_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        supplements = []
        for result in data.get("results", []):  # 🔹 Retorna TODOS os suplementos
            properties = result.get("properties", {})

            def get_text_value(prop, field_type):
                """Função auxiliar para evitar erros ao acessar campos do Notion."""
                return prop.get(field_type, [{}])[0].get("text", {}).get("content", "Não informado") if prop.get(field_type) else "Não informado"

            nome = get_text_value(properties.get("Name", {}), "title")
            dosagem = get_text_value(properties.get("recommendation", {}), "rich_text")

            supplements.append(f"{nome} - {dosagem}")

        return "\n".join(supplements) if supplements else "Nenhum suplemento encontrado."
    
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar o Notion API: {str(e)}"

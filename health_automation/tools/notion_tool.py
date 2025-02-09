import os
import json
import requests
from crewai.tools import tool

# Carrega credenciais do Notion
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
    """Busca a lista de suplementos e medicamentos registrados no Notion."""
    try:
        response = requests.post(NOTION_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        supplements = []
        for result in data["results"]:
            properties = result.get("properties", {})

            def get_text_value(prop, field_type):
                """Função auxiliar para evitar erros ao acessar campos do Notion."""
                return prop.get(field_type, [{}])[0].get("text", {}).get("content", "Não informado") if prop.get(field_type) else "Não informado"

            def get_select_value(prop):
                """Função auxiliar para campos de seleção."""
                return prop.get("select", {}).get("name", "Não informado") if prop.get("select") else "Não informado"

            nome = get_text_value(properties.get("Name", {}), "title")
            dosagem = get_text_value(properties.get("recommendation", {}), "rich_text")
            beneficios = get_text_value(properties.get("benefits", {}), "rich_text")
            responsavel = get_select_value(properties.get("person", {}))
            periodo = get_select_value(properties.get("time", {}))
            preco = properties.get("avg. cost", {}).get("number", "Não informado")
            quantidade_embalagem = properties.get("pack", {}).get("number", "Não informado")
            marca = get_text_value(properties.get("brand", {}), "rich_text")
            proximo_reabastecimento = properties.get("next shop", {}).get("date", {}).get("start", "Não informado")

            supplements.append(
                f"{nome} ({dosagem}) - {beneficios}\n"
                f"Tomado por: {responsavel} - Período: {periodo}\n"
                f"Marca: {marca} - Embalagem: {quantidade_embalagem} unidades\n"
                f"Preço médio: ${preco} - Próximo reabastecimento: {proximo_reabastecimento}\n"
                "--------------------------"
            )

        return "\n".join(supplements) if supplements else "Nenhum suplemento encontrado no Notion."
    
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar o Notion API: {str(e)}"

import json
import requests
from crewai.tools import tool
from health_automation.tools.config_loader import load_credentials
import os


notion_creds = load_credentials(os.path.join("certs","notion.json"))

NOTION_API_KEY = notion_creds["NOTION_API_KEY"]
NOTION_DATABASE_ID = notion_creds["NOTION_DATABASE_ID"]
NOTION_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

@tool("fetch_notion_supplements")
def fetch_notion_supplements() -> str:
    """Busca TODOS os suplementos no Notion e retorna um JSON estruturado com todos os campos necessários."""
    try:
        response = requests.post(NOTION_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        supplements = []
        for result in data.get("results", []):
            properties = result.get("properties", {})

            def get_text_value(prop):
                """Função auxiliar para evitar erros ao acessar campos do Notion."""
                if not prop:
                    return "Não informado"
                if "title" in prop:
                    return prop["title"][0]["text"]["content"] if prop["title"] else "Não informado"
                if "rich_text" in prop:
                    return prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else "Não informado"
                if "select" in prop:
                    return prop["select"]["name"] if prop["select"] else "Não informado"
                return "Não informado"
            
            # 🔹 Captura todos os campos corretamente
            nome = get_text_value(properties.get("Name", {}))
            recomendacao = get_text_value(properties.get("Recommendation", {}))
            beneficios = get_text_value(properties.get("Benefits", {}))
            horario = get_text_value(properties.get("Time", {}))
            multivitaminico = get_text_value(properties.get("Multivitamin", {}))
            marca = get_text_value(properties.get("Brand", {}))

            supplements.append({
                "name": nome,
                "recommendation": recomendacao,
                "benefits": beneficios,
                "time": horario,
                "multivitaminic": multivitaminico,
                "brand": marca
            })

        return json.dumps(supplements, indent=2, ensure_ascii=False) if supplements else json.dumps({"error": "Nenhum suplemento encontrado."})
    
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Erro ao acessar o Notion API: {str(e)}"})


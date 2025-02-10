import json
import requests
from crewai.tools import tool
from health_automation.tools.config_loader import load_credentials
import os


notion_creds = load_credentials(os.path.join("certs","notion.json"))

NOTION_API_KEY = notion_creds["NOTION_API_KEY"]
NOTION_DATABASE_ID = notion_creds["NOTION_DATABASE_ID"]
NOTION_PAGE_ID = notion_creds["NOTION_PAGE_ID"]

NOTION_DATABASE_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
NOTION_PAGE_URL = f"https://api.notion.com/v1/pages/{NOTION_PAGE_ID}"
NOTION_BLOCKS_URL = f"https://api.notion.com/v1/blocks/{NOTION_PAGE_ID}/children"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

@tool("fetch_notion_supplements")
def fetch_notion_supplements() -> str:
    """Busca TODOS os suplementos no Notion e retorna um JSON estruturado com todos os campos necessários."""
    try:
        response = requests.post(NOTION_DATABASE_URL, headers=HEADERS)
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
    
@tool("fetch_notion_user_data")
def fetch_notion_user_data() -> str:
    """Extrai informações do usuário de uma página do Notion, incluindo email e o corpo da página."""
    try:
        # 1️⃣ Captura as propriedades da página (como o email)
        response_page = requests.get(NOTION_PAGE_URL, headers=HEADERS)
        response_page.raise_for_status()
        page_data = response_page.json()
        
        properties = page_data.get("properties", {})
        email = properties.get("Email", {}).get("email", "Não encontrado")

        # 2️⃣ Captura o corpo da página (blocos de texto)
        response_blocks = requests.get(NOTION_BLOCKS_URL, headers=HEADERS)
        response_blocks.raise_for_status()
        blocks_data = response_blocks.json()

        body_text = []
        for block in blocks_data.get("results", []):
            block_type = block.get("type", "")
            rich_text = block.get(block_type, {}).get("rich_text", [])

            # Captura títulos, listas e parágrafos
            block_content = "".join([text.get("text", {}).get("content", "") for text in rich_text])
            if block_type == "heading_1":
                block_content = f"\n# {block_content}\n"
            elif block_type == "heading_2":
                block_content = f"\n## {block_content}\n"
            elif block_type == "heading_3":
                block_content = f"\n### {block_content}\n"
            elif block_type == "bulleted_list_item" or block_type == "numbered_list_item":
                block_content = f"- {block_content}"

            if block_content:
                body_text.append(block_content)

        body_content = "\n".join(body_text) if body_text else "Sem conteúdo disponível."

        # 3️⃣ Retorna os dados estruturados
        user_info = {
            "Email": email,
            "Conteúdo da Página": body_content
        }

        return json.dumps(user_info, indent=2, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Erro ao acessar o Notion API: {str(e)}"})


import requests
import json
from crewai.tools import tool

AMAZON_API_URL = "https://api.amazon-es.com/search"
IHERB_API_URL = "https://api.iherb.com/search"

@tool("search_supplement_products")
def search_supplement_products(supplement_name: str, max_results: int = 5) -> str:
    """
    Busca suplementos diretamente na Amazon Espanha e iHerb.

    Parâmetros:
    - supplement_name (str): Nome do suplemento.
    - max_results (int): Número máximo de resultados (padrão = 5).

    Retorna:
    - JSON com lista de produtos e links de compra.
    """
    try:
        # 🔹 Busca na Amazon Espanha
        amazon_response = requests.get(AMAZON_API_URL, params={"query": supplement_name, "limit": max_results})
        amazon_response.raise_for_status()
        amazon_results = amazon_response.json().get("products", [])

        # 🔹 Busca no iHerb
        iherb_response = requests.get(IHERB_API_URL, params={"query": supplement_name, "limit": max_results})
        iherb_response.raise_for_status()
        iherb_results = iherb_response.json().get("products", [])

        results = []
        for product in amazon_results:
            results.append({
                "Nome": product.get("name", "Nome não disponível"),
                "Preço": product.get("price", "Preço não disponível"),
                "Link": product.get("url", "Sem link"),
                "Fonte": "Amazon Espanha"
            })

        for product in iherb_results:
            results.append({
                "Nome": product.get("name", "Nome não disponível"),
                "Preço": product.get("price", "Preço não disponível"),
                "Link": product.get("url", "Sem link"),
                "Fonte": "iHerb"
            })

        return json.dumps(results[:max_results], indent=2, ensure_ascii=False) if results else json.dumps({"error": "Nenhum produto encontrado."})

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Erro ao buscar suplementos: {str(e)}"})

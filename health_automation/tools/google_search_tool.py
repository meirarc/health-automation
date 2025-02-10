import os
import json
from crewai_tools import SerperDevTool
from health_automation.tools.config_loader import load_credentials
from crewai.tools import tool

serper_creds = load_credentials(os.path.join("certs", "serper.json"))
os.environ["SERPER_API_KEY"] = serper_creds["SERPER_API_KEY"]

# 🔹 Criamos a ferramenta de busca corretamente
search_best_supplements = SerperDevTool()

@tool("search_supplements_in_spain")
def search_supplements_in_spain(query: str, max_results: int = 5) -> str:
    """
    Busca suplementos na internet, priorizando resultados da Espanha.

    Parâmetros:
    - query: Nome do suplemento (ex: "Vitamina D 5000 IU")
    - max_results: Número máximo de resultados a retornar (padrão = 5)

    Retorna:
    - JSON com os produtos encontrados, incluindo título, link e descrição.
    """
    try:
        search_query = f"{query} suplemento OR vitaminas site:amazon.es OR site:iherb.com"

        # 🔹 Executa a busca
        raw_results = search_best_supplements.run(query=search_query, gl="es", num=max_results)

        # 🔹 Debug: Mostrar a resposta completa do Serper
        print(f"🔍 Resposta do Serper para '{query}': {json.dumps(raw_results, indent=2, ensure_ascii=False)}")

        # 🔹 Verifica se a resposta é uma string JSON válida
        try:
            results = json.loads(raw_results) if isinstance(raw_results, str) else raw_results
        except json.JSONDecodeError:
            return json.dumps({"error": "Erro ao decodificar resposta da API Serper."}, ensure_ascii=False)

        # 🔹 Verifica se há uma chave 'organic' com resultados
        if not isinstance(results, dict) or "organic" not in results or not isinstance(results["organic"], list) or not results["organic"]:
            return json.dumps({"error": f"Nenhum produto encontrado para '{query}'. Tente buscar por outro nome ou verificar disponibilidade."}, ensure_ascii=False)

        # 🔹 Extrai os produtos encontrados
        supplements = [
            {
                "title": item.get("title", "Título não disponível"),
                "link": item.get("link", "Link não disponível"),
                "description": item.get("snippet", "Descrição não disponível")
            }
            for item in results["organic"] if isinstance(item, dict)
        ]

        return json.dumps(supplements[:max_results], indent=2, ensure_ascii=False) if supplements else \
            json.dumps({"error": f"Nenhum produto encontrado para '{query}'."}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"Erro ao buscar suplementos: {str(e)}"}, ensure_ascii=False)

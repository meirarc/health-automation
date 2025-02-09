from crewai.tools import tool
import requests

# URLs da API do PubMed
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

@tool("search_pubmed")
def search_pubmed(query: str) -> str:
    """Busca estudos científicos sobre suplementação no PubMed (retorno simplificado)."""
    try:
        # 🔹 Passo 1: Buscar IDs dos artigos relacionados ao termo de pesquisa
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 2  # 🔹 Retorna apenas 2 artigos para economizar tokens
        }
        search_response = requests.get(PUBMED_SEARCH_URL, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        article_ids = search_data.get("esearchresult", {}).get("idlist", [])
        if not article_ids:
            return f"Nenhum estudo encontrado para '{query}'."

        # 🔹 Passo 2: Buscar detalhes dos artigos (Título + Link)
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(article_ids),
            "retmode": "json"
        }
        fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
        fetch_response.raise_for_status()
        fetch_data = fetch_response.json()

        article_summaries = fetch_data.get("result", {})
        results = []

        for article_id in article_ids:
            article = article_summaries.get(article_id, {})
            title = article.get("title", "Título não disponível")
            results.append(f"{title} (ID: {article_id})\nLink: https://pubmed.ncbi.nlm.nih.gov/{article_id}/")

        return "\n\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API do PubMed: {str(e)}"

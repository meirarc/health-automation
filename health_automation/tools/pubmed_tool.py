from crewai.tools import tool
import requests

# URLs corretas da API do PubMed
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

@tool("search_pubmed")
def search_pubmed(query: str) -> str:
    """Busca estudos científicos sobre suplementação no PubMed."""
    try:
        # Passo 1: Buscar IDs dos artigos relacionados ao termo de pesquisa
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 3  # Limita a 3 artigos para evitar excesso de informação
        }
        search_response = requests.get(PUBMED_SEARCH_URL, params=search_params)
        search_response.raise_for_status()  # Lança erro se a requisição falhar
        search_data = search_response.json()

        article_ids = search_data.get("esearchresult", {}).get("idlist", [])
        if not article_ids:
            return f"Nenhum artigo encontrado para '{query}'."

        # Passo 2: Buscar detalhes dos artigos pelos IDs
        article_details = []
        for article_id in article_ids:
            fetch_params = {
                "db": "pubmed",
                "id": article_id,
                "retmode": "text",
                "rettype": "abstract"
            }
            fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
            fetch_response.raise_for_status()
            
            article_details.append(
                f"🔹 **ID:** {article_id}\n"
                f"📄 Resumo:\n{fetch_response.text.strip()}\n"
                f"🔗 [Link para o estudo](https://pubmed.ncbi.nlm.nih.gov/{article_id}/)\n"
                "--------------------------"
            )

        return "\n\n".join(article_details)

    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API do PubMed: {str(e)}"

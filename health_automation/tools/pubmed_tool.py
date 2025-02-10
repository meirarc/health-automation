from crewai.tools import tool
import requests
import json

# URLs da API do PubMed
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


@tool("search_pubmed")
def search_pubmed(query: str, max_results: int = 3) -> str:
    """
    Busca estudos científicos sobre suplementação no PubMed e retorna um JSON com título, resumo curto e link.

    Parâmetros:
    - query: Termo de busca (ex: "Vitamin C supplementation")
    - max_results: Número máximo de artigos a buscar (padrão = 3)
    """
    try:
        # 🔹 Passo 1: Buscar IDs dos artigos relacionados ao termo de pesquisa
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results,  # 🔹 Limita a busca para evitar excesso de tokens
        }
        search_response = requests.get(PUBMED_SEARCH_URL, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        article_ids = search_data.get("esearchresult", {}).get("idlist", [])
        if not article_ids:
            return json.dumps(
                {"error": f"Nenhum estudo encontrado para '{query}'."},
                ensure_ascii=False,
            )

        # 🔹 Passo 2: Buscar detalhes dos artigos (Título + Link)
        fetch_params = {"db": "pubmed", "id": ",".join(article_ids), "retmode": "json"}
        fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
        fetch_response.raise_for_status()
        fetch_data = fetch_response.json()

        article_summaries = fetch_data.get("result", {})
        results = []

        for article_id in article_ids:
            article = article_summaries.get(article_id, {})
            title = article.get("title", "Título não disponível")
            link = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"

            # 🔹 Passo 3: Buscar o resumo do artigo (abstract)
            abstract_params = {
                "db": "pubmed",
                "id": article_id,
                "retmode": "text",
                "rettype": "abstract",
            }
            abstract_response = requests.get(PUBMED_DETAILS_URL, params=abstract_params)

            # 🔹 Pega apenas os primeiros 500 caracteres para evitar excesso de tokens
            abstract_text = (
                abstract_response.text.strip()[:500]
                if abstract_response.status_code == 200
                else "Resumo não disponível"
            )

            results.append({"title": title, "abstract": abstract_text, "link": link})

        return json.dumps(results, indent=2, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        return json.dumps(
            {"error": f"Erro ao acessar a API do PubMed: {str(e)}"}, ensure_ascii=False
        )


@tool("summarize_pubmed_results")
def summarize_pubmed_results(response: str) -> str:
    """
    Resuma os artigos científicos antes de enviá-los ao LLM.
    - Limita o abstract a 300 caracteres.
    - Remove informações irrelevantes.
    """
    try:
        articles = json.loads(response)
        summarized_articles = []

        for article in articles[:3]:  # 🔹 Garante que usamos no máximo 3 artigos
            title = article.get("title", "Título não disponível")
            abstract = article.get("abstract", "Resumo não disponível")[
                :300
            ]  # 🔹 Corta para 300 caracteres
            link = article.get("link", "")

            summarized_articles.append(
                f"📌 **{title}**\nResumo: {abstract}...\n🔗 [Leia mais]({link})\n"
            )

        return "\n".join(summarized_articles)

    except Exception as e:
        return f"Erro ao processar resposta do PubMed: {str(e)}"

import pytest
from health_automation.tools.pubmed_tool import search_pubmed

@pytest.mark.pubmed
def test_search_pubmed():
    """Testa a ferramenta de busca no PubMed."""
    print("🚀 Testando busca no PubMed...")

    resultado = search_pubmed.run("Vitamin D supplementation")
    print(resultado)

    assert "Erro" not in resultado, "A busca no PubMed falhou!"

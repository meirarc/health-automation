import pytest
from health_automation.tools.google_search_tool import search_best_supplements

@pytest.mark.google
def test_google_search_supplements():
    """Testa a ferramenta de busca no Google."""
    print("🚀 Testando busca no Google...")

    # Correção: Usamos .run() corretamente
    resultado = search_best_supplements.run(search_query="Melhores suplementos de Ômega-3")
    print(resultado)

    assert "Erro" not in resultado, "A busca no Google falhou!"

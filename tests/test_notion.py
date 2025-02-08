import sys
import os
import pytest
from health_automation.tools.notion_tool import fetch_notion_supplements

@pytest.mark.notion
def test_fetch_notion_supplements():
    """Testa a integração com a API do Notion para buscar suplementos."""
    print("🚀 Testando busca de suplementos no Notion...")

    resultado = fetch_notion_supplements.run()
    print(resultado)

    assert "Erro" not in resultado, "A busca no Notion falhou!"

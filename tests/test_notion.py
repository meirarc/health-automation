import sys
import os
import pytest
from health_automation.tools.notion_tool import fetch_notion_supplements, fetch_notion_user_data

@pytest.mark.notion
def test_fetch_notion_supplements():
    """Testa a integração com a API do Notion para buscar suplementos."""
    print("🚀 Testando busca de suplementos no Notion...")

    resultado = fetch_notion_supplements.run()
    print(resultado)

    assert "Erro" not in resultado, "A busca no Notion falhou!"

@pytest.mark.notion
def test_fetch_notion_user_data():
    """Testa a extração de dados do usuário da página do Notion."""
    print("🚀 Testando extração de dados do usuário no Notion...")

    resultado = fetch_notion_user_data.run()
    print(resultado)

    assert isinstance(resultado, str), "O retorno deve ser uma string JSON!"
    assert "Erro" not in resultado, "A extração da página do Notion falhou!"
    assert "Email" in resultado, "O JSON retornado não contém o campo 'Email'!"
    assert "Conteúdo da Página" in resultado, "O JSON não contém o corpo da página!"
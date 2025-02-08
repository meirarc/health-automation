import sys
import os
import pytest

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from health_automation.tools.email_tool import send_health_report_tool

@pytest.mark.email
def test_send_health_report():
    """Testa se o envio de e-mail via CrewAI Tools funciona corretamente."""
    print("🚀 Testando envio de e-mail...")

    resultado = send_health_report_tool.run(
        subject="🚀 Teste CrewAI - Suplementação",
        body="<h1>Seu relatório de suplementos</h1><p>Isso é um teste de envio de e-mail via CrewAI!</p>",
        recipient="meirarc@gmail.com"
    )

    print(resultado)

    # O teste passa se a resposta conter a confirmação de envio bem-sucedido
    assert "✅ E-mail enviado com sucesso" in resultado, "O envio de e-mail falhou!"

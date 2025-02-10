import pytest
from health_automation.tools.email_tool import send_email_tool


@pytest.mark.email
def test_send_email_tool():
    """Testa a ferramenta de envio de email via CrewAI Tools."""
    print("🚀 Testando envio de e-mail...")

    resultado = send_email_tool.run(
        subject="🚀 Teste CrewAI - Email Markdown",
        body_markdown="# Teste de Envio\n\nIsso é um **teste** de envio de e-mail via CrewAI!\n\n- Item 1\n- Item 2",
    )

    print(resultado)

    # O teste passa se a resposta conter a confirmação de envio bem-sucedido
    assert "✅ E-mail enviado com sucesso" in resultado, "O envio de e-mail falhou!"

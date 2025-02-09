from crewai import Task

from health_automation.tools.notion_tool import fetch_notion_supplements
from health_automation.tools.pubmed_tool import search_pubmed
from health_automation.tools.google_search_tool import search_best_supplements
from health_automation.tools.email_tool import send_health_report_tool

from health_automation.config.agents import analysis_agent, research_agent, email_agent  # Importa os agentes

from health_automation.llm_setup.checkpoint_manager import get_checkpoint, save_checkpoint


def create_task(name, description, expected_output, agent, tools=[]):
    if get_checkpoint(name):  # 🔹 Se já foi concluída, pula
        print(f"✅ [CHECKPOINT] Tarefa '{name}' já concluída. Pulando...")
        return None
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        tools=tools
    )

# 🔹 Tarefa: Analisar Suplementação
analyze_supplementation = create_task("analyze_supplementation",
    description=(
        "Analise a tabela de suplementação do Notion e verifique:\n"
        "- Se há interações negativas entre suplementos e medicamentos.\n"
        "- Se a ingestão está alinhada com recomendações científicas.\n"
        "- Se há sugestões para melhorar a rotina de suplementação."
    ),
    expected_output=(
        "Um relatório estruturado com:\n"
        "- Lista de suplementos e medicamentos analisados.\n"
        "- Possíveis interações negativas.\n"
        "- Sugestões de ajustes na rotina de consumo.\n"
        "- Reforço sobre quais suplementos são essenciais."
    ),
    tools=[fetch_notion_supplements],
    agent=analysis_agent
)

# 🔹 Tarefa: Pesquisar Melhores Suplementos
research_best_supplements = create_task(
    "research_best_supplements",
    description=(
        "Pesquise por suplementos de melhor qualidade e custo-benefício, considerando:\n"
        "- Opções que combinem múltiplas vitaminas em um só produto.\n"
        "- Redução na quantidade de cápsulas ingeridas.\n"
        "- Comparação de preços e marcas confiáveis."
    ),
    expected_output=(
        "Uma lista estruturada com:\n"
        "- Suplementos recomendados com base em qualidade e custo.\n"
        "- Opções que reduzem a quantidade de cápsulas.\n"
        "- Links para compra dos produtos recomendados."
    ),
    tools=[search_pubmed, search_best_supplements],
    agent=research_agent
)

# 🔹 Tarefa: Enviar Relatório de Suplementação
send_supplementation_report = create_task(
    "send_supplementation_report",
    description=(
        "Envie um e-mail com um relatório estruturado contendo:\n"
        "- A análise do `Analysis Agent` sobre a suplementação.\n"
        "- A pesquisa do `Research Agent` sobre melhores suplementos e preços.\n"
        "- Sugestões de ajustes na rotina de ingestão.\n"
        "- Opções de compra e links para os suplementos recomendados."
    ),
    expected_output=(
        "Um e-mail bem formatado, contendo:\n"
        "- A análise detalhada da combinação de suplementos.\n"
        "- Recomendações de suplementos mais eficientes e econômicos.\n"
        "- Links confiáveis para compra dos produtos."
    ),
    tools=[send_health_report_tool],
    agent=email_agent
)

# 🔹 Lista de Tarefas para Importação Fácil
tasks = [task for task in [analyze_supplementation, research_best_supplements, send_supplementation_report] if task]

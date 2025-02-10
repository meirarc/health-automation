from crewai import Task
from health_automation.config.agents import notion_manager, health_researcher, shopping_assistant

def create_task(name, description, expected_output, agent):
    """Cria uma tarefa reutilizável com parâmetros padronizados."""
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        output_file=f"data/{name}.txt",
    )

# 🔹 Tarefa 1: Extração de Dados do Usuário no Notion
extract_user_data = create_task(
    name="extract_user_data",
    description="Ler os dados do usuário no Notion e armazená-los para referência futura.",
    expected_output="Arquivo com informações do usuário incluindo email, rotina e condições de saúde.",
    agent=notion_manager
)

# 🔹 Tarefa 2: Extração de Suplementos do Notion
extract_supplements = create_task(
    name="extract_supplements",
    description="Extrair a tabela de suplementos do Notion e armazená-la para análise.",
    expected_output="Arquivo contendo os suplementos do usuário, incluindo nome, dosagem e horário de consumo.",
    agent=notion_manager
)

# 🔹 Tarefa 3: Pesquisa Acadêmica sobre Suplementos
research_articles = create_task(
    name="research_articles",
    description="Buscar artigos acadêmicos para cada suplemento e enviar um email com os resultados.",
    expected_output="Emails enviados com links e resumos dos artigos científicos para cada suplemento.",
    agent=health_researcher
)

# 🔹 Tarefa 4: Buscar Suplementos na Internet
find_products = create_task(
    name="find_products",
    description="Buscar suplementos recomendados na internet e enviar um email com as opções de compra.",
    expected_output="Emails enviados com links para comprar os suplementos recomendados.",
    agent=shopping_assistant
)

# 🔹 Lista de Tarefas sem `find_recommended_dosages`
tasks = [extract_user_data, extract_supplements, research_articles, find_products]

from crewai import Task
import json
from health_automation.config.agents import notion_manager, health_researcher, shopping_assistant, dosage_specialist

def create_task(name, description, expected_output, agent):
    """Cria uma tarefa reutilizável com parâmetros padronizados."""
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        output_file=f"data/{name}.txt"
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

analyze_user_health = create_task(
    name="analyze_user_health",
    description=(
        "Com base nos dados de saúde do usuário extraídos do Notion, identifique possíveis conflitos "
        "entre os suplementos consumidos e as condições médicas do usuário. "
        "Sugira suplementos adicionais se necessário."
    ),
    expected_output="Lista de suplementos que podem ser problemáticos e sugestões de substituições.",
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


def process_each_supplement():
    """Carrega a lista de suplementos e cria uma task para cada um."""
    try:
        with open("data/extract_supplements.txt", "r", encoding="utf-8") as file:
            supplements = json.load(file)
        
        tasks = []
        for supplement in supplements:
            supplement_name = supplement["name"]

            task = create_task(
                name=f"research_articles_{supplement_name}",
                description=f"Pesquisar artigos acadêmicos sobre {supplement_name} e gerar um resumo.",
                expected_output=f"Resumo acadêmico salvo em data/research_articles_{supplement_name}.txt",
                agent=health_researcher
            )
            tasks.append(task)

        return tasks

    except FileNotFoundError:
        print("❌ Arquivo de suplementos não encontrado.")
        return []
    
def process_dosage_recommendations():
    """Carrega os dados do usuário e suplementos para gerar recomendações personalizadas."""
    try:
        with open("data/extract_user_data.txt", "r", encoding="utf-8") as user_file:
            user_data = json.load(user_file)
        
        with open("data/extract_supplements.txt", "r", encoding="utf-8") as supplements_file:
            supplements = json.load(supplements_file)

        tasks = []
        for supplement in supplements:
            supplement_name = supplement["name"]
            health_condition = user_data.get("Saúde", "Condição de saúde não especificada")

            task = create_task(
                name=f"dosage_recommendation_{supplement_name}",
                description=f"Buscar a dosagem recomendada de {supplement_name} para um usuário com {health_condition} e enviar por email.",
                expected_output=f"Email enviado para o usuário com a dosagem recomendada de {supplement_name}.",
                agent=dosage_specialist
            )
            tasks.append(task)

        return tasks

    except FileNotFoundError:
        print("❌ Arquivo de dados do usuário ou suplementos não encontrado.")
        return []

tasks = [extract_user_data, extract_supplements,analyze_user_health, research_articles, find_products]
tasks.extend(process_each_supplement())
tasks.extend(process_dosage_recommendations())


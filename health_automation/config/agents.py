from crewai import Agent

from health_automation.tools.notion_tool import fetch_notion_user_data, fetch_notion_supplements
from health_automation.tools.pubmed_tool import search_pubmed, summarize_pubmed_results
from health_automation.tools.email_tool import send_email_tool
from health_automation.tools.google_search_tool import search_supplements_in_spain, fetch_recommended_dosages
from health_automation.tools.shopping_tool import search_supplement_products

from health_automation.llm_setup.groq_setup import groq_setup

llm=groq_setup()

def create_agent(role="", goal="", backstory="", tools=[], function_call=None, max_rpm=3):
    """
    Cria um agente com os parâmetros fornecidos.
    """
    print(f"⚡ Criando agente: {role}...")  # 🔹 Log para depuração
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        llm=llm, 
        function_call=function_call,
        verbose=True,
        max_rpm=max_rpm

    )

notion_manager = create_agent(
    role="Gerenciador de Notion",
    goal="Extrair e organizar os dados do usuário no Notion",
    backstory="Você é um assistente especializado em coletar e organizar dados do Notion para análise de saúde.",
    tools=[fetch_notion_user_data, fetch_notion_supplements]
)

# 🔹 Agente Pesquisador Científico
health_researcher = create_agent(
    role="Pesquisador de Saúde",
    goal="Buscar artigos científicos sobre os suplementos e gerar um resumo.",
    backstory="Você é um pesquisador que analisa estudos científicos para determinar a eficácia e segurança dos suplementos.",
    tools=[search_pubmed, summarize_pubmed_results, send_email_tool]
)

# 🔹 Agente Assistente de Compras
shopping_assistant = create_agent(
    role="Assistente de Compras",
    goal="Encontrar os melhores suplementos na internet para o usuário",
    backstory="Você é um assistente especializado em encontrar suplementos confiáveis e recomendados para compra.",
    tools=[search_supplement_products, search_supplements_in_spain, send_email_tool]  # 🔹 Agora tem as duas ferramentas!
)

# 🔹 Novo Agente: Especialista em Dosagem
dosage_specialist = create_agent(
    role="Especialista em Dosagem",
    goal="Determinar a dosagem ideal de suplementos com base na condição de saúde do usuário.",
    backstory=(
        "Você é um especialista em suplementação e recomendações personalizadas. "
        "Seu objetivo é garantir que o usuário tome os suplementos na dosagem correta para seu perfil de saúde."
    ),
    tools=[fetch_recommended_dosages, send_email_tool]  # 🔹 Ferramentas para busca e envio
)

# 🔹 Lista de Agentes
agents = [notion_manager, health_researcher, shopping_assistant, dosage_specialist]

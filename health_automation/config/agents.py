from crewai import Agent, LLM

from health_automation.tools.notion_tool import fetch_notion_supplements
from health_automation.tools.pubmed_tool import search_pubmed, summarize_pubmed_results
from health_automation.tools.google_search_tool import search_supplements_in_spain
from health_automation.tools.email_tool import send_health_report_tool


# 🔹 Criamos um único LLM compartilhado entre todos os agentes
def create_llm():
    return LLM(
        model="groq/gemma2-9b-it",
        max_tokens=2500,  # 🔹 Permitimos mais tokens, já que agora temos controle melhorado
        temperature=0.3,
        timeout=120,
        frequency_penalty=0.6
    )



def create_agent(role="", goal="", backstory="", tools=[], function_call=None):
    """
    Cria um agente com os parâmetros fornecidos.
    """
    print(f"⚡ Criando agente: {role}...")  # 🔹 Log para depuração
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        llm=create_llm(),  # 🔹 Usa o modelo limitado
        verbose=True,
        max_rpm=4,
        function_call=function_call
    )

# 🔹 Agente de Análise de Suplementação
extractor_agent = create_agent(
    role="Especialista em Extração de Dados",
    goal="Coletar informações detalhadas sobre os suplementos no Notion e validar as recomendações diárias.",
    backstory="Você é um especialista em organização e coleta de dados estruturados.",
    tools=[fetch_notion_supplements, search_supplements_in_spain],
    function_call=lambda supplement: search_supplements_in_spain(supplement["name"])
)

nutrition_agent = create_agent(
    role="Nutricionista Especialista em Suplementação",
    goal="Analisar a combinação e horários dos suplementos para garantir eficácia, utilizando o mínimo de palavras possíveis.",
    backstory="Você é um nutricionista especializado em suplementação e otimização da saúde.",
)


# 🔹 Agente Pesquisador de Suplementos
research_agent = create_agent(
    role="Pesquisador Científico",
    goal="Buscar evidências científicas atualizadas sobre suplementação e gerar um resumo curto.",
    backstory="Você é um cientista dedicado a encontrar as melhores evidências científicas sobre suplementação.",
    tools=[search_pubmed],
    function_call=lambda response: summarize_pubmed_results(response) 
)

# 🔹 Agente de Comunicação por E-mail
report_agent = create_agent(
    role="Gerador de Relatórios",
    goal="Compilar todas as informações e enviar um relatório bem formatado.",
    backstory="Você é um especialista em relatórios e comunicação clara. Seu objetivo é entregar informações bem estruturadas.",
    tools=[send_health_report_tool]
)

# 🔹 Lista de Agentes para Importação Fácil
agents = [extractor_agent,nutrition_agent, research_agent, report_agent]

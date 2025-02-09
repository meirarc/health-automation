from crewai import Agent, LLM

from health_automation.tools.notion_tool import fetch_notion_supplements
from health_automation.tools.pubmed_tool import search_pubmed
from health_automation.tools.google_search_tool import search_best_supplements
from health_automation.tools.email_tool import send_health_report_tool

from health_automation.config.rate_limiter import rate_limiter

def rate_limited_llm(model="groq/mixtral-8x7b-32768", max_tokens=1000, temperature=0.1, timeout=120, frequency_penalty=0.1):
    rate_limiter.wait_for_tokens(max_tokens)  # 🔹 Wait before making the API call
    return LLM(model=model, max_tokens=max_tokens, temperature=temperature, timeout=timeout, frequency_penalty=frequency_penalty)



# 🔹 Agente de Análise de Suplementação
analysis_agent = Agent(
    role="Especialista em análise de suplementação",
    goal="Verificar se a combinação de suplementos e medicamentos está adequada.",
    backstory=(
        "Você é um especialista em saúde e suplementação, focado em ajudar as pessoas "
        "a otimizar sua ingestão de vitaminas e minerais para melhorar a saúde."
    ),
    tools=[fetch_notion_supplements],
    llm=rate_limited_llm(),
    max_iter=3,
    verbose=True
)

# 🔹 Agente Pesquisador de Suplementos
research_agent = Agent(
    role="Pesquisador de suplementos e estudos científicos",
    goal="Buscar evidências científicas sobre suplementação e encontrar produtos de melhor qualidade e custo-benefício.",
    backstory=(
        "Você é um pesquisador especializado em suplementação, com acesso a bases científicas "
        "e ferramentas de busca para encontrar as melhores opções de vitaminas e minerais."
    ),
    tools=[search_pubmed, search_best_supplements],
    llm=rate_limited_llm(),
    max_iter=3,
    verbose=True
)

# 🔹 Agente de Comunicação por E-mail
email_agent = Agent(
    role="Assistente de comunicação por e-mail",
    goal="Enviar relatórios bem estruturados com análises e recomendações sobre suplementação.",
    backstory=(
        "Você é um assistente responsável por comunicar as análises e recomendações da equipe, "
        "garantindo que o usuário tenha um resumo claro e acionável."
    ),
    tools=[send_health_report_tool],
    llm=rate_limited_llm(),
    max_iter=3,
    verbose=True
)

# 🔹 Lista de Agentes para Importação Fácil
agents = [analysis_agent, research_agent, email_agent]

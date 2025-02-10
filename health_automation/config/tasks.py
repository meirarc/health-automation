from crewai import Task

from health_automation.config.agents import extractor_agent,nutrition_agent, research_agent, report_agent


def create_task(name, description, expected_output, agent, tools=[]):
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        tools=tools,
        output_file=f"data/{name}.txt",
    )


extract_data_task = create_task(
    name="extract_data",
    description="Extraia os dados do Notion e valide as recomendações diárias.",
    expected_output="JSON com informações dos suplementos e possíveis ajustes.",
    agent=extractor_agent,
)

# 🔹 Tarefa 2: Análise Nutricional
analyze_nutrition_task = create_task(
    name="analyze_nutrition",
    description="Analise horários e combinações dos suplementos e sugira ajustes.",
    expected_output="Sugestões de ajustes nos horários e combinações dos suplementos.",
    agent=nutrition_agent,
)

# 🔹 Tarefa 3: Pesquisa Científica
research_supplements_task = create_task(
    name="research_supplements",
    description="Pesquise artigos científicos sobre os suplementos e forneça resumos.",
    expected_output="Lista de artigos científicos com resumos e links.",
    agent=research_agent,
)

# 🔹 Tarefa 4: Gerar e Enviar Relatório
generate_report_task = create_task(
    name="generate_report",
    description="Consolide todas as informações e envie um relatório formatado.",
    expected_output="Relatório final enviado via email.",
    agent=report_agent,
)


tasks = [extract_data_task, analyze_nutrition_task, research_supplements_task, generate_report_task]

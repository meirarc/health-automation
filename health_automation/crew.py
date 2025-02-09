from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from health_automation.tools.notion_tool import fetch_notion_supplements
from health_automation.tools.pubmed_tool import search_pubmed
from health_automation.tools.google_search_tool import search_best_supplements
from health_automation.tools.email_tool import send_health_report_tool

@CrewBase
class HealthAutomationCrew:
    """Configuração da CrewAI para automação da suplementação."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Criando Agentes (nomes iguais ao exemplo)
    @agent
    def analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["analysis_agent"],
            verbose=True,
            #tools=[fetch_notion_supplements]  # ⬅️ Adicionando a ferramenta diretamente no agente
        )

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            verbose=True,
            tools=[search_pubmed, search_best_supplements]  # ⬅️ Garantindo ferramentas registradas corretamente
        )

    @agent
    def report_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_agent"],
            verbose=True,
            tools=[send_health_report_tool]  # ⬅️ Registrando ferramenta corretamente
        )

    # Criando Tarefas (nomes iguais ao exemplo)
    @task
    def analyze_supplements_task(self):
        return {
            "config": self.tasks_config["analyze_supplementation"],
            "agent": self.analysis_agent(),
            #"tools": [fetch_notion_supplements]  # ⬅️ Garantindo que a ferramenta é passada para a task
        }

    @task
    def research_supplements_task(self):
        return {
            "config": self.tasks_config["research_best_supplements"],
            "agent": self.research_agent(),
            "tools": [search_pubmed, search_best_supplements]  # ⬅️ Garantindo ferramentas registradas
        }

    @task
    def generate_health_report_task(self):
        return {
            "config": self.tasks_config["send_supplementation_report"],
            "agent": self.report_agent(),
            "tools": [send_health_report_tool]  # ⬅️ Garantindo ferramenta para envio de relatório
        }

    # Criando a Crew
    @crew
    def health_crew(self) -> Crew:
        return Crew(
            agents=[self.analysis_agent(), self.research_agent(), self.report_agent()],
            tasks=[
                self.analyze_supplements_task(),
                self.research_supplements_task(),
                self.generate_health_report_task()
            ],
            process=Process.sequential  # Executa os agentes em sequência
        )

# Executar a Crew
if __name__ == "__main__":
    crew_instance = HealthAutomationCrew()
    result = crew_instance.health_crew().kickoff()
    print(result)

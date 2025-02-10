from crewai import Crew, Process
from health_automation.config.agents import agents
from health_automation.config.tasks import tasks
from health_automation.llm_setup import groq_setup


def create_crew():
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential
    )

if __name__ == "__main__":
    print("🚀 Starting CrewAI process...\n")
    crew = create_crew()
    result = crew.kickoff()
    print("\n✅ Final Result:\n", result)
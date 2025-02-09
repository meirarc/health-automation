import time

from health_automation.config import groq_setup
from crewai import Crew, Process
from health_automation.config.agents import agents
from health_automation.config.tasks import tasks
from health_automation.checkpoint_manager import save_checkpoint

import os

CHECKPOINT_FILE = "task_checkpoints.json"

# 🔹 Apaga o arquivo JSON para recomeçar do zero
if os.path.exists(CHECKPOINT_FILE):
    os.remove(CHECKPOINT_FILE)
    print("🗑️ Checkpoints resetados. Rodando do zero!")

def create_crew():
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential
    )

if __name__ == "__main__":
    print("🚀 Starting CrewAI process...\n")
    crew = create_crew()

    retry_attempts = 5  # 🔹 Tentativas antes de falhar completamente

    for attempt in range(retry_attempts):
        try:
            for task in tasks:
                print(f"⚡ Executando tarefa: {task.description[:30]}...")  # Exibir início da descrição
                
                result = task.execute_sync()  # 🔹 Executa a tarefa diretamente
                save_checkpoint(task.description, result)  # 🔹 Salva progresso corretamente
                
                print(f"✅ Tarefa '{task.description[:30]}...' concluída!\n")
            
            print("\n🎉 Todas as tarefas foram concluídas com sucesso!")
            break  # Sai do loop se tudo der certo
        except Exception as e:
            if "rate_limit_exceeded" in str(e):
                wait_time = 10 + (attempt * 5)  # 🔹 Espera crescente (10s → 15s → 20s...)
                print(f"⚠️ Rate limit atingido. Esperando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
            else:
                print("❌ Erro inesperado:", e)
                break  # Sai se não for erro de limite de taxa
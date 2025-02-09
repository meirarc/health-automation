import json
import os

CHECKPOINT_FILE = "data/task_checkpoints.json"

def load_checkpoints():
    """Carrega checkpoints e evita erro se o JSON estiver vazio ou inválido."""
    if not os.path.exists(CHECKPOINT_FILE):
        return {}

    try:
        with open(CHECKPOINT_FILE, "r") as file:
            data = file.read().strip()  # 🔹 Remove espaços extras
            return json.loads(data) if data else {}  # 🔹 Se vazio, retorna {}
    except json.JSONDecodeError:
        print("⚠️ Erro ao carregar task_checkpoints.json. Resetando arquivo...")
        return {}

def save_checkpoint(task_name, result):
    """Salva o progresso da tarefa convertendo o resultado para string."""
    checkpoints = load_checkpoints()
    checkpoints[task_name] = str(result)  # 🔹 Converte `TaskOutput` para string

    with open(CHECKPOINT_FILE, "w") as file:
        json.dump(checkpoints, file, ensure_ascii=False, indent=4)  # 🔹 JSON formatado

def get_checkpoint(task_name):
    """Retorna o progresso salvo da tarefa, se existir."""
    return load_checkpoints().get(task_name, None)
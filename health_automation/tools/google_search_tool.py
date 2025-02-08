import os
import json
from crewai_tools import SerperDevTool

# Carrega credenciais do Serper.dev
def load_serper_credentials():
    certs_path = os.path.join("certs", "serper.json")
    with open(certs_path, "r") as file:
        return json.load(file)

serper_creds = load_serper_credentials()
os.environ["SERPER_API_KEY"] = serper_creds["SERPER_API_KEY"]  # Define a chave no ambiente

# Criamos a ferramenta corretamente
search_best_supplements = SerperDevTool()

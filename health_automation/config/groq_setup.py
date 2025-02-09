import os
import json

# Carregar credenciais do Groq
def load_groq_credentials():
    certs_path = os.path.join("certs", "groq.json")
    with open(certs_path, "r") as file:
        return json.load(file)

groq_creds = load_groq_credentials()
os.environ["GROQ_API_KEY"] = groq_creds["GROQ_API_KEY"]


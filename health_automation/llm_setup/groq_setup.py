import os
import json

from crewai import LLM


# Carregar credenciais do Groq
def load_groq_credentials():
    certs_path = os.path.join("certs", "groq.json")
    with open(certs_path, "r") as file:
        return json.load(file)


def groq_setup(
    model="groq/gemma2-9b-it",
    max_tokens=2000,
    temperature=0.3,
    timeout=120,
    frequency_penalty=0.6,
):
    """Configura o LLM do Groq com limites seguros."""
    return LLM(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
        frequency_penalty=frequency_penalty,
    )


groq_creds = load_groq_credentials()
os.environ["GROQ_API_KEY"] = groq_creds["GROQ_API_KEY"]

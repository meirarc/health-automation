import json
import os

def load_credentials(filename):
    """Carrega credenciais de um arquivo JSON dentro da pasta certs/"""
    path = os.path.join(os.path.dirname(__file__), "..", "certs", filename)
    with open(path, "r") as file:
        return json.load(file)

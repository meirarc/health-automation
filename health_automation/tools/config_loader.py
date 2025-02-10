import json

def load_credentials(filename):
    """Carrega credenciais de um arquivo JSON dentro da pasta certs/"""
    with open(filename, "r") as file:
        return json.load(file)

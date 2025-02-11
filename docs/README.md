
# versao python
3.12

# install uv
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

# create venv
```sh
uv venv .venv
source .venv/bin/activate
```

# install rust
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

# iniciar terminal rust
```sh
source $HOME/.cargo/env
```

# upgrade pip
```sh
uv pip install --upgrade pip
```

# install crewai
```sh
uv pip install crewai "crewai[tools]"
```


# instalacao via uv requirements
```sh
# Ferramentas Dev
uv pip install -r requirements-dev.txt

# Demais ferramentas
uv pip install -r requirements.txt
```


# 📌 ferramentas de dev
✅ pytest → Framework para testes automatizados
✅ python-dotenv → Carregar variáveis de ambiente do .env
✅ rich → Melhor formatação de logs e prints coloridos
✅ loguru → Biblioteca avançada para logs
✅ black → Autoformatador de código
✅ isort → Organiza imports automaticamente
✅ pre-commit → Executa verificações de código antes de commits


# Pre-commit
✅ Instalar o pre-commit → uv pip install pre-commit
✅ Criar o arquivo .pre-commit-config.yaml e adicionar regras
✅ Rodar pre-commit autoupdate para baixar as versões mais recentes
✅ Executar pre-commit run --all-files para testar
✅ Instalar os hooks com pre-commit install para rodar antes dos commits

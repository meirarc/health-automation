## **Project Setup**

## **Environment Setup**
Configure seu ambiente local para garantir compatibilidade com a **CI pipeline**. Isso inclui a versão correta do Python e todas as dependências necessárias.

### **1️⃣ Verifique a instalação do Python**
Certifique-se de ter **Python 3.x** instalado. Verifique a versão com:

```sh
python --version
```

Se não tiver instalado, faça o download em [python.org](https://www.python.org/downloads/).

---

### **2️⃣ Criando e ativando um ambiente virtual (`venv`)**
Usar um **virtual environment** evita conflitos de dependências entre projetos.

#### **Linux/MacOS**
```sh
python -m venv venv
source venv/bin/activate
```

#### **Windows**
```sh
python -m venv venv
venv\Scripts\activate
```

Se preferir um **script automático**, pode criar um arquivo `setup.bat` no Windows para ativar o ambiente.

---

### **3️⃣ Instalar Dependências**
Instale todos os pacotes listados no `requirements.txt`:

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se precisar de ferramentas adicionais para **testes e linting**, instale-as com:

```sh
pip install pytest black isort pydocstyle
```

---

## **Usage**
Para rodar o projeto, use:

```sh
python -m main
```


---

## **Contributing**
Se deseja contribuir, veja as [Diretrizes de Contribuição](../CONTRIBUTING.md). Lá você encontrará informações sobre **convenções de código**, **formatadores** e **testes**.

---

Para mais detalhes, consulte a documentação no diretório [`docs`](./).

🚀 **Obrigado por contribuir!**  

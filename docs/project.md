## **🔹 Estrutura Revisada do CrewAI**
### **🧠 Agentes**
1. **📋 Analysis Agent (Agente de Análise)**  
   - Analisa os suplementos e medicamentos registrados no Notion.  
   - Verifica interações entre suplementos e medicamentos.  
   - Avalia se o consumo e os horários estão otimizados.  
   - Sugere ajustes para melhorar absorção e eficácia.  

2. **🔬 Research Agent (Agente de Pesquisa)**  
   - Pesquisa estudos científicos atualizados sobre suplementação.  
   - Busca combinações de suplementos mais eficientes e econômicas.  
   - Identifica marcas confiáveis e opções que **reduzam o custo e a quantidade de cápsulas ingeridas**.  
   - Sugere produtos que combinem vitaminas para otimizar a ingestão diária.  

3. **📧 Report Agent (Agente de Relatório)** _(antes Reminder Agent)_  
   - Formata e gera um relatório com as análises e pesquisas.  
   - Envia um **e-mail bem estruturado** com:  
     - **Análise da suplementação atual**.  
     - **Sugestões de ajustes** baseadas na Research e Analysis.  
     - **Sugestões de compras com marcas e preços aproximados**.  
   - O e-mail deve ser fácil de entender, bem formatado e pronto para ação.  

---

## **📌 Novas Tarefas**
1. **Analisar os dados do Notion** para verificar interações e otimizar a suplementação.  
2. **Pesquisar estudos científicos e opções de suplementos mais eficientes e econômicos**.  
3. **Gerar um relatório detalhado e enviar por e-mail** com sugestões de ajustes e recomendações de compra.  

---

## **🛠 Ferramentas (CrewAI Compatible)**
Para garantir **integração direta com CrewAI**, vamos utilizar ferramentas já compatíveis:  

- **📊 Notion API**: Para acessar a tabela de suplementos.  
- **📚 PubMed/NLM API**: Para pesquisa científica.  
- **🌐 SerperDevTool** _(Google Search)_ → Para encontrar suplementos e preços.  
- **📧 SMTP Email Tool** → Para enviar os relatórios.  

---

## **🚀 Execução Revisada**
- **Analysis Agent** → **Diário ou Semanal** _(Analisa Notion e otimiza a suplementação)_.  
- **Research Agent** → **Mensal** _(Busca estudos e suplementos melhores)_.  
- **Report Agent** → **Semanal ou Mensal** _(Envia e-mail formatado)_.  

# 🤖 AI Tool Use - LlamaIndex com Function Calling

Um projeto demonstrando o uso do LlamaIndex com ferramentas personalizadas (function calling) e integração com Groq e Tavily.

## ✨ Funcionalidades

- 🧮 **Operações Matemáticas**: Soma, subtração e multiplicação via function calling
- 🔍 **Busca na Internet**: Integração com Tavily para pesquisas em tempo real
- 🚀 **Modelo**: Llama 3.3 70B Versatile via Groq
- 💻 **Interface Web**: UI interativa com Streamlit
- 📝 **Logging**: Sistema de logs em JSON para análise das interações

## 🛠️ Tecnologias

- [LlamaIndex](https://docs.llamaindex.ai/) - Framework para aplicações LLM
- [Groq](https://groq.com/) - Inferência com LPU
- [Tavily](https://tavily.com/) - API de busca para IA
- [Streamlit](https://streamlit.io/) - Framework para interfaces web

## 🧠 Lógica de Implementação

### Como o Agente Decide Quando Usar Ferramentas

O projeto utiliza o **ReActAgent** do LlamaIndex, que implementa o padrão ReAct (Reasoning + Acting). A lógica funciona assim:

1. **Recebe a pergunta** do usuário
2. **Analisa o contexto** usando o LLM (Llama 3.3 70B)
3. **Decide automaticamente**:
   - Se for uma pergunta matemática → usa as ferramentas `add`, `subtract` ou `multiply`
   - Se precisar de informações atuais → usa a ferramenta `search_web`
   - Se for uma pergunta de conhecimento geral → responde diretamente com o modelo

### Por que Groq?

O Groq foi escolhido pela sua baixa latência de inferência. Utilizando a tecnologia LPU (Language Processing Unit), o Groq oferece respostas significativamente mais rápidas comparado a outras APIs, proporcionando uma experiência mais fluida para o usuário.

### Interface Visual

Foi criada uma **interface web com Streamlit** para facilitar os testes por usuários não técnicos. A interface permite:
- Enviar perguntas de forma intuitiva via chat
- Visualizar as respostas em tempo real

### Exemplo de Fluxo

```
Usuário: "Quanto é 128 vezes 46?"
    ↓
Agente analisa → Detecta operação matemática
    ↓
Chama tool: multiply(128, 46)
    ↓
Recebe resultado: 5888
    ↓
Responde: "O resultado de 128 × 46 é 5888."
```

```
Usuário: "Quem foi Albert Einstein?"
    ↓
Agente analisa → Pergunta de conhecimento geral
    ↓
Responde diretamente com base no conhecimento do modelo
```

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Conta no [Groq](https://console.groq.com/) para obter API key
- Conta no [Tavily](https://tavily.com/) para obter API key (opcional)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/MatheusDiani/ai-tool-use.git
cd ai-tool-use
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> ⚠️ A instalação pode demorar alguns minutos devido às dependências do LlamaIndex.

### 4. Configure as variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto (use o `.env.example` como referência):

```bash
cp .env.example .env
```

Depois edite o arquivo `.env` com suas chaves:

```env
GROQ_API_KEY=sua_chave_groq_aqui
TAVILY_API_KEY=sua_chave_tavily_aqui
```

## 💻 Uso

### Interface Streamlit

```bash
streamlit run src/app.py
```

Acesse `http://localhost:8501` no seu navegador.

## 📝 Exemplos de Prompts

| Tipo | Prompt |
|------|--------|
| Soma | "Quanto é 15 + 27?" |
| Subtração | "Calcule 100 - 45" |
| Multiplicação | "Quanto é 8 vezes 12?" |
| Busca | "Pesquise sobre Barack Obama" |

## 📁 Estrutura do Projeto

```
ai-tool-use/
├── .env.example          # Template de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Documentação
├── requirements.txt      # Dependências
├── logs/                 # Logs das interações (JSON)
└── src/
    ├── __init__.py
    ├── app.py            # Interface Streamlit
    ├── agent.py          # Configuração do ReActAgent
    ├── logger.py         # Sistema de logging
    └── tools/
        ├── __init__.py
        ├── math_tools.py   # Ferramentas: add, subtract, multiply
        └── search_tools.py # Ferramenta: search_web (Tavily)
```

## 📚 Aprendizados

Durante o desenvolvimento deste projeto, aprendi:

- Como funciona o padrão **ReAct** (Reasoning + Acting) para agentes de IA
- Integração do **LlamaIndex** com diferentes LLMs via Groq
- Implementação de **function calling** com ferramentas personalizadas
- Uso da **Tavily API** para busca de informações em tempo real

## 🔮 O Que Faria Diferente com Mais Tempo

1. **Definição do Problema**: Definiria melhor o escopo, se seria um agente somente para cálculos ou para tarefas mais amplas, e quais tipos de operações matemáticas seriam suportadas (divisão, potenciação, raiz quadrada, etc.).

2. **Análise de Soluções**: Mapearia todas as possíveis formas de resolver o problema e, se dentro de um time, conversaria com uma pessoa mais sênior sobre os caminhos propostos. Caso contrário, usaria uma LLM para analisar os prós e contras de cada abordagem.

3. **Planejamento com IA**: Usaria uma IDE com IA integrada para planejar e implementar uma primeira versão estruturada do projeto.

4. **Avaliação e Métricas**: Criaria um banco de perguntas e respostas de referência para avaliar o output do agente. Mediria:
   - Taxa de acerto no acionamento de ferramentas
   - Precisão das respostas matemáticas
   - Qualidade das buscas
   - Pesquisaria métricas específicas para avaliar esse tipo de aplicação com LLM

5. **Arquitetura Escalável na AWS**: Para uma primeira versão, configuraria:
   - **DynamoDB**: Armazenar metadados (ID da sessão, timestamp, custo de tokens, mensagens)
   - **S3**: Hospedar o frontend estático
   - **Lambda**: Processar as requisições do agente
   - **CloudFront**: URL pública
   - **Cognito**: Autenticação de usuários

## 👤 Autor

Matheus Diani

---
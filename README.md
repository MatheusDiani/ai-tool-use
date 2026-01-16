# 🤖 AI Tool Use - LlamaIndex with Function Calling

A project demonstrating the use of LlamaIndex with custom tools (function calling) and integration with Groq and Tavily.

## ✨ Features

- 🧮 **Mathematical Operations**: Addition, subtraction and multiplication via function calling
- 🔍 **Web Search**: Tavily integration for real-time searches
- 🚀 **Model**: Llama 3.3 70B Versatile via Groq
- 💻 **Web Interface**: Interactive UI with Streamlit
- 📝 **Logging**: JSON logging system for interaction analysis

## 🛠️ Technologies

- [LlamaIndex](https://docs.llamaindex.ai/) - LLM application framework
- [Groq](https://groq.com/) - LPU inference
- [Tavily](https://tavily.com/) - Search API for AI
- [Streamlit](https://streamlit.io/) - Web interface framework

## 🧠 Implementation Logic

### How the Agent Decides When to Use Tools

The project uses **ReActAgent** from LlamaIndex, which implements the ReAct pattern (Reasoning + Acting). The logic works as follows:

1. **Receives the question** from the user
2. **Analyzes the context** using the LLM (Llama 3.3 70B)
3. **Automatically decides**:
   - If it's a math question → uses `add`, `subtract` or `multiply` tools
   - If it needs current information → uses `search_web` tool
   - If it's a general knowledge question → responds directly with the model

### Why Groq?

Groq was chosen for its low latency inference. Using LPU (Language Processing Unit) technology, Groq offers significantly faster responses compared to other APIs, providing a smoother user experience.

### Visual Interface

A **Streamlit web interface** was created to facilitate testing by non-technical users. The interface allows:
- Sending questions intuitively via chat
- Viewing responses in real-time

### Flow Example

```
User: "What is 128 times 46?"
    ↓
Agent analyzes → Detects mathematical operation
    ↓
Calls tool: multiply(128, 46)
    ↓
Receives result: 5888
    ↓
Responds: "The result of 128 × 46 is 5888."
```

```
User: "Who was Albert Einstein?"
    ↓
Agent analyzes → General knowledge question
    ↓
Responds directly based on model knowledge
```

## 📋 Prerequisites

- Python 3.10 or higher
- [Groq](https://console.groq.com/) account to get API key
- [Tavily](https://tavily.com/) account to get API key (optional)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/MatheusDiani/ai-tool-use.git
cd ai-tool-use
```

### 2. Create and activate virtual environment

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Installation may take a few minutes due to LlamaIndex dependencies.

### 4. Configure environment variables

Create a file named `.env` in the project root (use `.env.example` as reference):

```bash
cp .env.example .env
```

Then edit the `.env` file with your keys:

```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

## 💻 Usage

### Streamlit Interface

```bash
streamlit run src/app.py
```

Access `http://localhost:8501` in your browser.

## 📝 Prompt Examples

| Type | Prompt |
|------|--------|
| Addition | "What is 15 + 27?" |
| Subtraction | "Calculate 100 - 45" |
| Multiplication | "What is 8 times 12?" |
| Search | "Search about Barack Obama" |

## 📁 Project Structure

```
ai-tool-use/
├── .env.example          # Environment variables template
├── .gitignore            # Files ignored by Git
├── README.md             # Documentation
├── requirements.txt      # Dependencies
├── logs/                 # Interaction logs (JSON)
└── src/
    ├── __init__.py
    ├── app.py            # Streamlit interface
    ├── agent.py          # ReActAgent configuration
    ├── logger.py         # Logging system
    └── tools/
        ├── __init__.py
        ├── math_tools.py   # Tools: add, subtract, multiply
        └── search_tools.py # Tool: search_web (Tavily)
```

## 📚 Lessons Learned

During the development of this project, I learned:

- How the **ReAct** pattern (Reasoning + Acting) works for AI agents
- **LlamaIndex** integration with different LLMs via Groq
- **Function calling** implementation with custom tools
- Using the **Tavily API** for real-time information search

## 🔮 What I Would Do Differently with More Time

1. **Problem Definition**: Better define the scope - whether it's an agent only for calculations or broader tasks, and what types of mathematical operations would be supported (division, exponentiation, square root, etc.).

2. **Solution Analysis**: Map all possible ways to solve the problem and, if in a team, discuss with a senior engineer about the proposed approaches. Otherwise, use an LLM to analyze the pros and cons of each approach.

3. **Planning with AI**: Use an AI-integrated IDE to plan and implement a structured first version of the project.

4. **Evaluation and Metrics**: Create a question-answer benchmark to evaluate the agent's output. Measure:
   - Tool activation accuracy rate
   - Mathematical response precision
   - Search quality
   - Research specific metrics for evaluating this type of LLM application

5. **Scalable AWS Architecture**: For a first version, would configure:
   - **DynamoDB**: Store metadata (session ID, timestamp, token cost, messages)
   - **S3**: Host static frontend
   - **Lambda**: Process agent requests
   - **CloudFront**: Public URL
   - **Cognito**: User authentication

6. **Infrastructure as Code**: Use **Terraform** or **AWS CDK** to provision and manage infrastructure in an automated and versioned way.

7. **CI/CD with GitHub Actions**: Create integration and continuous deployment pipelines to:
   - Run automated tests on each pull request
   - Automatic deploy to staging/production environment
   - Facilitate project maintenance and evolution

## 👤 Author

Matheus Diani

---
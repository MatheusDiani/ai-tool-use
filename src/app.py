import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.agent import create_agent

st.set_page_config(
    page_title="AI Tool Use",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.agent_error = None
    if "session_id" not in st.session_state:
        from datetime import datetime
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")


def load_agent():
    if st.session_state.agent is None and st.session_state.agent_error is None:
        try:
            with st.spinner("🔄 Carregando agente..."):
                st.session_state.agent = create_agent(st.session_state.session_id)
        except Exception as e:
            st.session_state.agent_error = str(e)


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🛠️ Ferramentas")
        st.markdown("""
        - `add(a, b)` - Soma
        - `subtract(a, b)` - Subtração  
        - `multiply(a, b)` - Multiplicação
        - `search_web(query)` - Busca
        """)
        
        st.divider()
        
        st.markdown("## 💡 Exemplos")
        
        st.markdown("**Matemática:**")
        st.code("Quanto é 125 + 37?", language=None)
        st.code("Calcule 500 - 123", language=None)
        
        st.markdown("**Pesquisa:**")
        st.code("Pesquise sobre inteligência artificial", language=None)
        st.code("Quais são as últimas notícias de tecnologia?", language=None)
        
        st.divider()
        
        if os.getenv("GROQ_API_KEY"):
            st.success("✅ Groq")
        else:
            st.error("❌ Groq")
        
        if os.getenv("TAVILY_API_KEY", "") not in ["", "your_tavily_api_key_here"]:
            st.success("✅ Tavily")
        else:
            st.warning("⚠️ Tavily")
        
        st.divider()
        st.caption("**Llama 3.3 70B** via Groq")
        
        if st.button("🗑️ Limpar"):
            st.session_state.messages = []
            st.rerun()


def render_chat():
    st.markdown('<h1 class="main-header">🤖 AI Tool Use</h1>', unsafe_allow_html=True)
    st.caption("LlamaIndex • Function Calling • Groq")
    
    st.divider()
    
    if st.session_state.agent_error:
        st.error(f"❌ {st.session_state.agent_error}")
        return
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Digite sua pergunta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Pensando..."):
                try:
                    response = st.session_state.agent.run(prompt)
                except Exception as e:
                    response = f"❌ Erro: {str(e)}"
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    init_session_state()
    load_agent()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()

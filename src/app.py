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
    """Initializes session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.agent_error = None
    if "session_id" not in st.session_state:
        from datetime import datetime
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")


def load_agent():
    """Loads the agent if not already loaded."""
    if st.session_state.agent is None and st.session_state.agent_error is None:
        try:
            with st.spinner("🔄 Loading agent..."):
                st.session_state.agent = create_agent(st.session_state.session_id)
        except Exception as e:
            st.session_state.agent_error = str(e)


def render_sidebar():
    """Renders the sidebar."""
    with st.sidebar:
        st.markdown("## 🛠️ Tools")
        st.markdown("""
        - `add(a, b)` - Addition
        - `subtract(a, b)` - Subtraction  
        - `multiply(a, b)` - Multiplication
        - `search_web(query)` - Search
        """)
        
        st.divider()
        
        st.markdown("## 💡 Examples")
        
        st.markdown("**Math:**")
        st.code("What is 125 + 37?", language=None)
        st.code("Calculate 500 - 123", language=None)
        
        st.markdown("**Search:**")
        st.code("Search about Barack Obama", language=None)
        st.code("What are the latest tech news?", language=None)
        
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
        
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()


def render_chat():
    """Renders the chat area."""
    st.markdown('<h1 class="main-header">🤖 AI Tool Use</h1>', unsafe_allow_html=True)
    st.caption("LlamaIndex • Function Calling • Groq")
    
    st.divider()
    
    if st.session_state.agent_error:
        st.error(f"❌ {st.session_state.agent_error}")
        return
    
    # Display message history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # User input
    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = st.session_state.agent.run(prompt)
                except Exception as e:
                    response = f"❌ Error: {str(e)}"
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    """Main Streamlit function."""
    init_session_state()
    load_agent()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()

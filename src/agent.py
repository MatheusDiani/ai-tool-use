import os
import asyncio
from typing import Optional

from llama_index.core.agent import ReActAgent
from llama_index.llms.groq import Groq

from .tools import get_math_tools, get_search_tools
from .tools.math_tools import set_tool_logger as set_math_logger
from .tools.search_tools import set_tool_logger as set_search_logger
from .logger import get_logger, AgentLogger

MODEL_NAME = "llama-3.3-70b-versatile"


class LoggedAgentWrapper:
    def __init__(self, agent: ReActAgent, model: str, logger: AgentLogger):
        self.agent = agent
        self.model = model
        self.logger = logger
    
    async def run_async(self, message: str) -> str:
        """Executa o agente e retorna a resposta."""
        self.logger.start_interaction(message)
        
        try:
            response = await self.agent.run(message)
            response_text = str(response)
            
            self.logger.end_interaction(
                response=response_text,
                model=self.model,
                status="success"
            )
            
            return response_text
            
        except Exception as e:
            self.logger.end_interaction(
                response="",
                model=self.model,
                status="error",
                error_message=str(e)
            )
            raise
    
    def run(self, message: str) -> str:
        """Executa síncronamente."""
        return asyncio.run(self.run_async(message))


def create_agent(session_id: Optional[str] = None) -> LoggedAgentWrapper:
    """Cria o agente ReAct com LlamaIndex e Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada.")
    
    logger = get_logger(session_id)
    set_math_logger(logger)
    set_search_logger(logger)
    
    llm = Groq(
        model=MODEL_NAME,
        api_key=api_key,
    )
    
    tools = []
    
    math_tools = get_math_tools()
    tools.extend(math_tools)
    
    search_tools = get_search_tools()
    if search_tools:
        tools.extend(search_tools)
    
    agent = ReActAgent(
        tools=tools,
        llm=llm,
    )
    
    print(f"✅ Agente criado - Sessão: {logger.session_id}")
    
    return LoggedAgentWrapper(agent, MODEL_NAME, logger)

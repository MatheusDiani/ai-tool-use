import os
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.core.tools import FunctionTool

# Referência global ao logger
_tool_logger = None


def set_tool_logger(logger):
    """Define o logger para as ferramentas de busca."""
    global _tool_logger
    _tool_logger = logger


def search_web(query: str) -> str:
    """
    Pesquisa informações na internet usando Tavily.
    
    Args:
        query: O que você quer pesquisar na internet
        
    Returns:
        Resultados da pesquisa
    """
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key or api_key == "your_tavily_api_key_here":
        return "Erro: TAVILY_API_KEY não configurada."
    
    try:
        tavily = TavilyToolSpec(api_key=api_key)
        result = tavily.search(query)
        result_str = str(result)
        
        # Log da chamada
        if _tool_logger:
            _tool_logger.log_tool_call("search_web", {"query": query}, result_str[:500])
        
        return result_str
    except Exception as e:
        return f"Erro na pesquisa: {str(e)}"


def get_search_tools() -> list:
    """Retorna as ferramentas de busca."""
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key or api_key == "your_tavily_api_key_here":
        print("⚠️  TAVILY_API_KEY não configurada. Busca na internet desabilitada.")
        return []
    
    search_tool = FunctionTool.from_defaults(
        fn=search_web,
        name="search_web",
        description="Pesquisa informações na internet. Use para buscar notícias, fatos atuais, ou qualquer informação que não esteja na sua base de conhecimento."
    )
    
    return [search_tool]

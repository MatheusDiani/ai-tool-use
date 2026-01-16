import os
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.core.tools import FunctionTool

# Global reference to logger
_tool_logger = None


def set_tool_logger(logger):
    """Sets the logger for search tools."""
    global _tool_logger
    _tool_logger = logger


def search_web(query: str) -> str:
    """
    Searches for information on the internet using Tavily.
    
    Args:
        query: What you want to search on the internet
        
    Returns:
        Search results
    """
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key or api_key == "your_tavily_api_key_here":
        return "Error: TAVILY_API_KEY not configured."
    
    try:
        tavily = TavilyToolSpec(api_key=api_key)
        result = tavily.search(query)
        result_str = str(result)
        
        # Log the call
        if _tool_logger:
            _tool_logger.log_tool_call("search_web", {"query": query}, result_str[:500])
        
        return result_str
    except Exception as e:
        return f"Search error: {str(e)}"


def get_search_tools() -> list:
    """Returns search tools."""
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key or api_key == "your_tavily_api_key_here":
        print("⚠️  TAVILY_API_KEY not configured. Web search disabled.")
        return []
    
    search_tool = FunctionTool.from_defaults(
        fn=search_web,
        name="search_web",
        description="Searches for information on the internet. Use to find news, current facts, or any information not in your knowledge base."
    )
    
    return [search_tool]

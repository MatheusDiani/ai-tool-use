from llama_index.core.tools import FunctionTool

# Global reference to logger (injected by agent)
_tool_logger = None


def set_tool_logger(logger):
    """Sets the logger for the tools."""
    global _tool_logger
    _tool_logger = logger


def _log_tool_call(name: str, args: dict, result):
    """Logs a tool call if logger is available."""
    if _tool_logger:
        _tool_logger.log_tool_call(name, args, result)


def add(a: float, b: float) -> float:
    """Adds two numbers."""
    result = a + b
    _log_tool_call("add", {"a": a, "b": b}, result)
    return result


def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    result = a - b
    _log_tool_call("subtract", {"a": a, "b": b}, result)
    return result


def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    result = a * b
    _log_tool_call("multiply", {"a": a, "b": b}, result)
    return result


def get_math_tools() -> list[FunctionTool]:
    """Returns mathematical tools for the agent."""
    add_tool = FunctionTool.from_defaults(
        fn=add,
        name="add",
        description="Adds two numbers. Use when you need to calculate the sum of values."
    )
    
    subtract_tool = FunctionTool.from_defaults(
        fn=subtract,
        name="subtract",
        description="Subtracts the second number from the first. Use to calculate differences."
    )
    
    multiply_tool = FunctionTool.from_defaults(
        fn=multiply,
        name="multiply",
        description="Multiplies two numbers. Use to calculate products."
    )
    
    return [add_tool, subtract_tool, multiply_tool]

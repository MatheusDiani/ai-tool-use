from llama_index.core.tools import FunctionTool

# Referência global ao logger (será injetado pelo agent)
_tool_logger = None


def set_tool_logger(logger):
    """Define o logger para as ferramentas."""
    global _tool_logger
    _tool_logger = logger


def _log_tool_call(name: str, args: dict, result):
    """Registra uma chamada de ferramenta se o logger estiver disponível."""
    if _tool_logger:
        _tool_logger.log_tool_call(name, args, result)


def add(a: float, b: float) -> float:
    """Soma dois números."""
    result = a + b
    _log_tool_call("add", {"a": a, "b": b}, result)
    return result


def subtract(a: float, b: float) -> float:
    """Subtrai o segundo número do primeiro."""
    result = a - b
    _log_tool_call("subtract", {"a": a, "b": b}, result)
    return result


def multiply(a: float, b: float) -> float:
    """Multiplica dois números."""
    result = a * b
    _log_tool_call("multiply", {"a": a, "b": b}, result)
    return result


def get_math_tools() -> list[FunctionTool]:
    """Retorna ferramentas matemáticas para o agente."""
    add_tool = FunctionTool.from_defaults(
        fn=add,
        name="add",
        description="Soma dois números. Use quando precisar calcular a adição de valores."
    )
    
    subtract_tool = FunctionTool.from_defaults(
        fn=subtract,
        name="subtract",
        description="Subtrai o segundo número do primeiro. Use para calcular diferenças."
    )
    
    multiply_tool = FunctionTool.from_defaults(
        fn=multiply,
        name="multiply",
        description="Multiplica dois números. Use para calcular produtos."
    )
    
    return [add_tool, subtract_tool, multiply_tool]

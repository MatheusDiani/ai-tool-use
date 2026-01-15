import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, asdict


# Diretório de logs
LOGS_DIR = Path(__file__).parent.parent / "logs"


@dataclass
class ToolCall:
    """Representa uma chamada de ferramenta."""
    name: str
    arguments: dict
    result: Any


@dataclass
class LogEntry:
    """Representa uma entrada de log."""
    timestamp: str
    session_id: str
    question: str
    response: str
    model: str
    latency_ms: float
    tokens_in: int
    tokens_out: int
    tools_called: list[dict]
    status: str  # "success" ou "error"
    error_message: Optional[str] = None


class AgentLogger:
    """Logger para registrar interações com o agente."""
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Inicializa o logger.
        
        Args:
            session_id: ID da sessão (gerado automaticamente se não fornecido)
        """
        self.session_id = session_id or self._generate_session_id()
        self.logs_dir = LOGS_DIR
        self._ensure_logs_dir()
        
        # Estado temporário para tracking
        self._current_question: str = ""
        self._start_time: float = 0
        self._tools_called: list[ToolCall] = []
    
    def _generate_session_id(self) -> str:
        """Gera um ID único para a sessão."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _ensure_logs_dir(self):
        """Garante que o diretório de logs existe."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_log_file_path(self) -> Path:
        """Retorna o caminho do arquivo de log do dia."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.logs_dir / f"log_{date_str}.json"
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estima o número de tokens em um texto.
        Usa uma aproximação simples: ~4 caracteres por token.
        
        Args:
            text: Texto para estimar tokens
            
        Returns:
            Número estimado de tokens
        """
        return max(1, len(text) // 4)
    
    def _load_existing_logs(self) -> list[dict]:
        """Carrega logs existentes do arquivo."""
        log_file = self._get_log_file_path()
        if log_file.exists():
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_logs(self, logs: list[dict]):
        """Salva logs no arquivo."""
        log_file = self._get_log_file_path()
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def start_interaction(self, question: str):
        """
        Inicia o tracking de uma interação.
        
        Args:
            question: Pergunta do usuário
        """
        self._current_question = question
        self._start_time = time.time()
        self._tools_called = []
    
    def log_tool_call(self, name: str, arguments: dict, result: Any):
        """
        Registra uma chamada de ferramenta.
        
        Args:
            name: Nome da ferramenta
            arguments: Argumentos passados
            result: Resultado retornado
        """
        tool_call = ToolCall(
            name=name,
            arguments=arguments,
            result=str(result)
        )
        self._tools_called.append(tool_call)
    
    def end_interaction(
        self,
        response: str,
        model: str,
        status: str = "success",
        error_message: Optional[str] = None
    ):
        """
        Finaliza o tracking e salva o log.
        
        Args:
            response: Resposta da LLM
            model: Modelo usado
            status: Status da interação ("success" ou "error")
            error_message: Mensagem de erro (se houver)
        """
        latency_ms = (time.time() - self._start_time) * 1000
        
        tokens_in = self._estimate_tokens(self._current_question)
        tokens_out = self._estimate_tokens(response)
        
        # Adicionar tokens das ferramentas
        for tool in self._tools_called:
            tokens_in += self._estimate_tokens(str(tool.arguments))
            tokens_out += self._estimate_tokens(str(tool.result))
        
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            session_id=self.session_id,
            question=self._current_question,
            response=response,
            model=model,
            latency_ms=round(latency_ms, 2),
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            tools_called=[asdict(t) for t in self._tools_called],
            status=status,
            error_message=error_message
        )
        
        # Salvar log
        logs = self._load_existing_logs()
        logs.append(asdict(entry))
        self._save_logs(logs)
        
        # Limpar estado
        self._current_question = ""
        self._start_time = 0
        self._tools_called = []
        
        return entry
    
    def get_session_logs(self) -> list[dict]:
        """Retorna todos os logs da sessão atual."""
        logs = self._load_existing_logs()
        return [log for log in logs if log.get("session_id") == self.session_id]
    
    def get_all_logs(self) -> list[dict]:
        """Retorna todos os logs do dia."""
        return self._load_existing_logs()


# Instância global do logger
_logger: Optional[AgentLogger] = None


def get_logger(session_id: Optional[str] = None) -> AgentLogger:
    """
    Obtém a instância do logger (singleton por sessão).
    
    Args:
        session_id: ID da sessão
        
    Returns:
        Instância do AgentLogger
    """
    global _logger
    if _logger is None or (session_id and _logger.session_id != session_id):
        _logger = AgentLogger(session_id)
    return _logger

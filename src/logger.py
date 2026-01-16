import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, asdict


# Logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"


@dataclass
class ToolCall:
    """Represents a tool call."""
    name: str
    arguments: dict
    result: Any


@dataclass
class LogEntry:
    """Represents a log entry."""
    timestamp: str
    session_id: str
    question: str
    response: str
    model: str
    latency_ms: float
    tokens_in: int
    tokens_out: int
    tools_called: list[dict]
    status: str  # "success" or "error"
    error_message: Optional[str] = None


class AgentLogger:
    """Logger for recording agent interactions."""
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initializes the logger.
        
        Args:
            session_id: Session ID (auto-generated if not provided)
        """
        self.session_id = session_id or self._generate_session_id()
        self.logs_dir = LOGS_DIR
        self._ensure_logs_dir()
        
        # Temporary state for tracking
        self._current_question: str = ""
        self._start_time: float = 0
        self._tools_called: list[ToolCall] = []
    
    def _generate_session_id(self) -> str:
        """Generates a unique session ID."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _ensure_logs_dir(self):
        """Ensures the logs directory exists."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_log_file_path(self) -> Path:
        """Returns the log file path for today."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.logs_dir / f"log_{date_str}.json"
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimates the number of tokens in a text.
        Uses a simple approximation: ~4 characters per token.
        
        Args:
            text: Text to estimate tokens
            
        Returns:
            Estimated number of tokens
        """
        return max(1, len(text) // 4)
    
    def _load_existing_logs(self) -> list[dict]:
        """Loads existing logs from file."""
        log_file = self._get_log_file_path()
        if log_file.exists():
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_logs(self, logs: list[dict]):
        """Saves logs to file."""
        log_file = self._get_log_file_path()
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def start_interaction(self, question: str):
        """
        Starts tracking an interaction.
        
        Args:
            question: User's question
        """
        self._current_question = question
        self._start_time = time.time()
        self._tools_called = []
    
    def log_tool_call(self, name: str, arguments: dict, result: Any):
        """
        Logs a tool call.
        
        Args:
            name: Tool name
            arguments: Arguments passed
            result: Result returned
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
        Finishes tracking and saves the log.
        
        Args:
            response: LLM response
            model: Model used
            status: Interaction status ("success" or "error")
            error_message: Error message (if any)
        """
        latency_ms = (time.time() - self._start_time) * 1000
        
        tokens_in = self._estimate_tokens(self._current_question)
        tokens_out = self._estimate_tokens(response)
        
        # Add tokens from tools
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
        
        # Save log
        logs = self._load_existing_logs()
        logs.append(asdict(entry))
        self._save_logs(logs)
        
        # Clear state
        self._current_question = ""
        self._start_time = 0
        self._tools_called = []
        
        return entry
    
    def get_session_logs(self) -> list[dict]:
        """Returns all logs from the current session."""
        logs = self._load_existing_logs()
        return [log for log in logs if log.get("session_id") == self.session_id]
    
    def get_all_logs(self) -> list[dict]:
        """Returns all logs from today."""
        return self._load_existing_logs()


# Global logger instance
_logger: Optional[AgentLogger] = None


def get_logger(session_id: Optional[str] = None) -> AgentLogger:
    """
    Gets the logger instance (singleton per session).
    
    Args:
        session_id: Session ID
        
    Returns:
        AgentLogger instance
    """
    global _logger
    if _logger is None or (session_id and _logger.session_id != session_id):
        _logger = AgentLogger(session_id)
    return _logger

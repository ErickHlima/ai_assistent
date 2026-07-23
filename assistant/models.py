from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolCall:
    tool: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionResult:
    success: bool
    message: str
    tool_call: ToolCall | None = None
    raw_response: str = ""
    data: Any = None

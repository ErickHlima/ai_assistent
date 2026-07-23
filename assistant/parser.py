import json
import re
from typing import Any

from assistant.models import ToolCall

_JSON_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.IGNORECASE | re.DOTALL)


def tentar_json(texto: str) -> dict[str, Any] | list[Any] | None:
	if not texto:
		return None

	candidato = texto.strip()
	fenced = _JSON_FENCE.fullmatch(candidato)
	if fenced is not None:
		candidato = fenced.group(1).strip()

	try:
		return json.loads(candidato)
	except json.JSONDecodeError:
		inicio = candidato.find("{")
		fim = candidato.rfind("}")
		if inicio != -1 and fim != -1 and fim > inicio:
			trecho = candidato[inicio : fim + 1]
			try:
				return json.loads(trecho)
			except json.JSONDecodeError:
				return None
		return None


def parse_tool_call(texto_ou_objeto: str | dict[str, Any] | None) -> ToolCall | None:
	if texto_ou_objeto is None:
		return None

	if isinstance(texto_ou_objeto, dict):
		payload: Any = texto_ou_objeto
	else:
		payload = tentar_json(texto_ou_objeto)

	if not isinstance(payload, dict):
		return None

	tool = payload.get("tool")
	args = payload.get("args", {})

	if not isinstance(tool, str):
		return None

	if args is None:
		args = {}

	if not isinstance(args, dict):
		return None

	return ToolCall(tool=tool, args=args)


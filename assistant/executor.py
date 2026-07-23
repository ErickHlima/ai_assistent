from typing import Any

from assistant.models import ExecutionResult, ToolCall
from tools.apps import abrir_programa
from tools.browser import abrir_site, pesquisar_google
from tools.files import criar_pasta


_DISPATCH = {
	"abrir_programa": abrir_programa,
	"pesquisar_google": pesquisar_google,
	"abrir_site": abrir_site,
	"criar_pasta": criar_pasta,
}


def _obter_acao(tool: str):
	return _DISPATCH.get(tool)


def executar(tool_call: ToolCall | dict[str, Any]) -> ExecutionResult:
	if isinstance(tool_call, dict):
		tool_call = ToolCall(
			tool=str(tool_call.get("tool", "")),
			args=dict(tool_call.get("args", {})),
		)

	acao = _obter_acao(tool_call.tool)
	if acao is None:
		return ExecutionResult(
			success=False,
			message=f"Ferramenta desconhecida: {tool_call.tool}",
			tool_call=tool_call,
		)

	try:
		retorno = acao(**tool_call.args)
	except TypeError as exc:
		return ExecutionResult(
			success=False,
			message=f"Argumentos invalidos para {tool_call.tool}: {exc}",
			tool_call=tool_call,
		)
	except Exception as exc:
		return ExecutionResult(
			success=False,
			message=f"Falha ao executar {tool_call.tool}: {exc}",
			tool_call=tool_call,
		)

	mensagem = retorno if isinstance(retorno, str) else f"{tool_call.tool} executado."
	return ExecutionResult(
		success=True,
		message=mensagem,
		tool_call=tool_call,
		data=retorno,
	)


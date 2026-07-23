from assistant.prompts import SYSTEM_PROMPT
from assistant.executor import executar
from assistant.models import ExecutionResult, ToolCall
from assistant.parser import parse_tool_call
from providers.lmstudio import perguntar


def gerar_resposta(prompt_usuario: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_usuario},
    ]
    return perguntar(messages)


def interpretar_resposta(resposta_modelo: str) -> ToolCall | None:
    return parse_tool_call(resposta_modelo)


def executar_prompt(prompt_usuario: str) -> ExecutionResult:
    resposta_modelo = gerar_resposta(prompt_usuario)
    tool_call = interpretar_resposta(resposta_modelo)

    if tool_call is None:
        return ExecutionResult(
            success=False,
            message="A resposta do modelo nao foi um JSON de ferramenta valido.",
            raw_response=resposta_modelo,
        )

    resultado = executar(tool_call)
    resultado.raw_response = resposta_modelo
    return resultado

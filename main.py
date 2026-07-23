from __future__ import annotations

import argparse
from typing import Iterable

from assistant.agent import executar_prompt


def _imprimir_resultado(prompt: str) -> int:
    resultado = executar_prompt(prompt)
    print("Resposta do modelo:")
    print(resultado.raw_response)
    print()
    print(resultado.message)
    return 0 if resultado.success else 1


def _modo_interativo() -> int:
    print("Digite um prompt. Escreva sair para encerrar.")
    while True:
        prompt = input("> ").strip()
        if prompt.lower() in {"sair", "exit", "quit"}:
            return 0

        if not prompt:
            continue

        codigo = _imprimir_resultado(prompt)
        print()
        if codigo != 0:
            print("Nenhuma acao foi executada.")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local AI Assistant")
    parser.add_argument("prompt", nargs="*", help="Prompt para o assistente")
    parser.add_argument("--gui", action="store_true", help="Abrir interface grafica")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.gui:
        from gui.window import abrir_janela

        abrir_janela()
        return 0

    if args.prompt:
        return _imprimir_resultado(" ".join(args.prompt))

    return _modo_interativo()


if __name__ == "__main__":
    raise SystemExit(main())


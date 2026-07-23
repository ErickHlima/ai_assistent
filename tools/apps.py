from subprocess import Popen


def abrir_programa(programa: str) -> str:
	programa_limpo = programa.strip()
	if not programa_limpo:
		raise ValueError("Nome do programa vazio.")

	Popen(programa_limpo, shell=True)
	return f"Tentando abrir o programa: {programa_limpo}"


from pathlib import Path


def criar_pasta(nome: str) -> str:
	pasta = Path(nome).expanduser()
	if not pasta.is_absolute():
		pasta = Path.cwd() / pasta

	pasta.mkdir(parents=True, exist_ok=True)
	return f"Pasta criada: {pasta}"


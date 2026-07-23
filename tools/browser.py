from urllib.parse import quote_plus
import webbrowser


def abrir_site(url: str) -> str:
	url_limpa = url.strip()
	if not url_limpa:
		raise ValueError("URL vazia.")

	webbrowser.open_new_tab(url_limpa)
	return f"Site aberto: {url_limpa}"


def pesquisar_google(pesquisa: str) -> str:
	termo = pesquisa.strip()
	if not termo:
		raise ValueError("Termo de pesquisa vazio.")

	url = f"https://www.google.com/search?q={quote_plus(termo)}"
	webbrowser.open_new_tab(url)
	return f"Pesquisa aberta no Google: {termo}"


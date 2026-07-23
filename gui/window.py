from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from assistant.agent import executar_prompt


class AssistantWindow:
	def __init__(self) -> None:
		self.root = tk.Tk()
		self.root.title("Local AI Assistant")
		self.root.geometry("720x520")
		self.root.minsize(640, 420)

		self.prompt_var = tk.StringVar()

		container = ttk.Frame(self.root, padding=16)
		container.pack(fill="both", expand=True)

		title = ttk.Label(container, text="Local AI Assistant", font=("Segoe UI", 16, "bold"))
		title.pack(anchor="w")

		subtitle = ttk.Label(
			container,
			text="Digite um prompt e deixe o agente decidir a acao.",
		)
		subtitle.pack(anchor="w", pady=(4, 12))

		entry_row = ttk.Frame(container)
		entry_row.pack(fill="x")

		entry = ttk.Entry(entry_row, textvariable=self.prompt_var)
		entry.pack(side="left", fill="x", expand=True)
		entry.bind("<Return>", lambda _event: self._on_submit())

		button = ttk.Button(entry_row, text="Executar", command=self._on_submit)
		button.pack(side="left", padx=(8, 0))

		self.status_var = tk.StringVar(value="Pronto")
		status = ttk.Label(container, textvariable=self.status_var)
		status.pack(anchor="w", pady=(10, 6))

		self.output = tk.Text(container, wrap="word", height=18)
		self.output.pack(fill="both", expand=True)
		self.output.configure(state="disabled")

		entry.focus_set()

	def _append_output(self, text: str) -> None:
		self.output.configure(state="normal")
		self.output.insert("end", text + "\n\n")
		self.output.see("end")
		self.output.configure(state="disabled")

	def _set_busy(self, busy: bool) -> None:
		self.status_var.set("Executando..." if busy else "Pronto")

	def _on_submit(self) -> None:
		prompt = self.prompt_var.get().strip()
		if not prompt:
			return

		self.prompt_var.set("")
		self._append_output(f"> {prompt}")
		self._set_busy(True)

		thread = threading.Thread(target=self._run_prompt, args=(prompt,), daemon=True)
		thread.start()

	def _run_prompt(self, prompt: str) -> None:
		try:
			resultado = executar_prompt(prompt)
			bloco = [
				"Resposta do modelo:",
				resultado.raw_response,
				"",
				resultado.message,
			]
		except Exception as exc:
			bloco = ["Erro ao executar o prompt:", str(exc)]

		self.root.after(0, lambda: self._finish_run("\n".join(bloco)))

	def _finish_run(self, texto: str) -> None:
		self._append_output(texto)
		self._set_busy(False)

	def run(self) -> None:
		self.root.mainloop()


def abrir_janela() -> None:
	AssistantWindow().run()


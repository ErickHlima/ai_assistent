import unittest

import assistant.executor as executor_module
from assistant.executor import executar
from assistant.models import ToolCall


class TestExecutor(unittest.TestCase):
    def test_executar_abrir_site_chama_ferramenta_certa(self):
        original = executor_module._DISPATCH["abrir_site"]
        chamadas = []

        def abrir_site_mock(**kwargs):
            chamadas.append(kwargs)
            return "Site aberto"

        executor_module._DISPATCH["abrir_site"] = abrir_site_mock
        try:
            resultado = executar(ToolCall(tool="abrir_site", args={"url": "https://github.com"}))
        finally:
            executor_module._DISPATCH["abrir_site"] = original

        self.assertTrue(resultado.success)
        self.assertEqual(resultado.message, "Site aberto")
        self.assertEqual(chamadas, [{"url": "https://github.com"}])

    def test_executar_rejeita_ferramenta_desconhecida(self):
        resultado = executar(ToolCall(tool="nao_existe", args={}))

        self.assertFalse(resultado.success)
        self.assertIn("Ferramenta desconhecida", resultado.message)
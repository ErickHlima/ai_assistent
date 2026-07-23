import unittest

from assistant.parser import parse_tool_call, tentar_json


class TestParser(unittest.TestCase):
    def test_tentar_json_aceita_bloco_fenced(self):
        texto = """```json
        {"tool":"abrir_site","args":{"url":"https://example.com"}}
        ```"""

        resultado = tentar_json(texto)

        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado["tool"], "abrir_site")

    def test_parse_tool_call_retorna_none_para_texto_invalido(self):
        self.assertIsNone(parse_tool_call("texto qualquer"))
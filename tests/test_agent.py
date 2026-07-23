import unittest
from unittest.mock import patch

from assistant.agent import gerar_resposta, interpretar_resposta


class TestAgent(unittest.TestCase):
    def test_gerar_resposta_monta_mensagens_corretamente(self):
        with patch("assistant.agent.perguntar", return_value='{"tool":"abrir_site","args":{"url":"https://github.com"}}') as perguntar_mock:
            resposta = gerar_resposta("abrir github")

        self.assertEqual(resposta, '{"tool":"abrir_site","args":{"url":"https://github.com"}}')
        mensagens = perguntar_mock.call_args.args[0]
        self.assertEqual(mensagens[0]["role"], "system")
        self.assertEqual(mensagens[1]["role"], "user")
        self.assertEqual(mensagens[1]["content"], "abrir github")

    def test_interpretar_resposta_transforma_json_em_tool_call(self):
        tool_call = interpretar_resposta('{"tool":"criar_pasta","args":{"nome":"Projeto IA"}}')

        self.assertIsNotNone(tool_call)
        self.assertEqual(tool_call.tool, "criar_pasta")
        self.assertEqual(tool_call.args, {"nome": "Projeto IA"})
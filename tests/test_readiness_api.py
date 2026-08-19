import json
import unittest
from unittest.mock import Mock
from app.api.server import RayquazaAPI
class TestReadinessAPI(unittest.IsolatedAsyncioTestCase):
    def criar_api(self, pronto: bool) -> RayquazaAPI:
        bot = Mock()
        bot.is_ready.return_value = pronto
        return RayquazaAPI(bot=bot,
                           host="127.0.0.1",
                           port=8080,
                           notification_channel_id=123,
                           api_token="token-correto")
    async def test_health_deve_retornar_200_mesmo_sem_discord_pronto(self) -> None:
        api = self.criar_api(False)
        resposta = await api.verificar_saude(Mock())
        dados = json.loads(resposta.text)
        self.assertEqual(resposta.status, 200)
        self.assertEqual(dados["status"], "online")
        self.assertEqual(dados["servico"], "rayquaza-bot")
    async def test_ready_deve_retornar_200_quando_discord_estiver_pronto(self) -> None:
        api = self.criar_api(True)
        resposta = await api.verificar_prontidao(Mock())
        dados = json.loads(resposta.text)
        self.assertEqual(resposta.status, 200)
        self.assertEqual(dados["status"], "ready")
        self.assertEqual(dados["servico"], "rayquaza-bot")
        self.assertTrue(dados["discord"])
    async def test_ready_deve_retornar_503_quando_discord_nao_estiver_pronto(self) -> None:
        api = self.criar_api(False)
        resposta = await api.verificar_prontidao(Mock())
        dados = json.loads(resposta.text)
        self.assertEqual(resposta.status, 503)
        self.assertEqual(dados["status"], "not_ready")
        self.assertEqual(dados["servico"], "rayquaza-bot")
        self.assertFalse(dados["discord"])
if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import AsyncMock, Mock
from aiohttp.test_utils import TestClient, TestServer
from app.api.server import RayquazaAPI
class TestContratosHTTPAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.canal = Mock()
        self.canal.send = AsyncMock()
        self.bot = Mock()
        self.bot.is_ready.return_value = True
        self.bot.get_channel.return_value = self.canal
        self.api = RayquazaAPI(bot=self.bot,
                               host="127.0.0.1",
                               port=8080,
                               notification_channel_id=123,
                               api_token="token-correto")
        self.servidor = TestServer(self.api.criar_aplicacao())
        self.cliente = TestClient(self.servidor)
        await self.cliente.start_server()
    async def asyncTearDown(self) -> None:
        await self.cliente.close()
    async def test_health_deve_ser_publico(self) -> None:
        resposta = await self.cliente.get("/health")
        dados = await resposta.json()
        self.assertEqual(resposta.status, 200)
        self.assertEqual(dados, {"status": "online", "servico": "rayquaza-bot"})
    async def test_ready_deve_retornar_200_quando_discord_estiver_pronto(self) -> None:
        resposta = await self.cliente.get("/ready")
        dados = await resposta.json()
        self.assertEqual(resposta.status, 200)
        self.assertEqual(dados, {"status": "ready", "servico": "rayquaza-bot", "discord": True})
    async def test_ready_deve_retornar_503_quando_discord_nao_estiver_pronto(self) -> None:
        self.bot.is_ready.return_value = False
        resposta = await self.cliente.get("/ready")
        dados = await resposta.json()
        self.assertEqual(resposta.status, 503)
        self.assertEqual(dados, {"status": "not_ready", "servico": "rayquaza-bot", "discord": False})
    async def test_notificacao_de_teste_deve_recusar_requisicao_sem_token(self) -> None:
        resposta = await self.cliente.post("/notificacoes/teste", json={"mensagem": "Teste sem token"})
        dados = await resposta.json()
        self.assertEqual(resposta.status, 401)
        self.assertEqual(dados, {"erro": "nao autorizado."})
        self.assertEqual(resposta.headers["WWW-Authenticate"], "Bearer")
        self.canal.send.assert_not_awaited()
    async def test_notificacao_de_teste_deve_recusar_token_incorreto(self) -> None:
        resposta = await self.cliente.post("/notificacoes/teste",
                                           headers={"Authorization": "Bearer token-incorreto"},
                                           json={"mensagem": "Teste com token incorreto"})
        dados = await resposta.json()
        self.assertEqual(resposta.status, 401)
        self.assertEqual(dados, {"erro": "nao autorizado."})
        self.assertEqual(resposta.headers["WWW-Authenticate"], "Bearer")
        self.canal.send.assert_not_awaited()
    async def test_notificacao_de_teste_deve_aceitar_token_correto(self) -> None:
        resposta = await self.cliente.post("/notificacoes/teste",
                                           headers={"Authorization": "Bearer token-correto"},
                                           json={"mensagem": "Teste autenticado"})
        dados = await resposta.json()
        self.assertEqual(resposta.status, 200)
        self.assertEqual(dados, {"status": "notificacao enviada com sucesso.", "canal_id": 123})
        self.canal.send.assert_awaited_once_with("Teste autenticado")
    async def test_promocao_de_voo_deve_recusar_requisicao_sem_token(self) -> None:
        resposta = await self.cliente.post("/notificacoes/promocoes-de-voo", json={})
        dados = await resposta.json()
        self.assertEqual(resposta.status, 401)
        self.assertEqual(dados, {"erro": "nao autorizado."})
        self.assertEqual(resposta.headers["WWW-Authenticate"], "Bearer")
        self.canal.send.assert_not_awaited()
if __name__ == "__main__":
    unittest.main()

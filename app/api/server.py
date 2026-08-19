import logging
from typing import Any
import discord
from aiohttp import web
from discord.ext import commands
from app.api.autenticacao import criar_middleware_autenticacao
from app.notifications.promocoes_de_voo import PromocaoDeVoo, criar_embed_promocao_de_voo
logger = logging.getLogger(__name__)
class RayquazaAPI:
    def __init__(self, bot: commands.Bot, host: str, port: int, notification_channel_id: int, api_token: str) -> None:
        self.bot = bot
        self.host = host
        self.port = port
        self.notification_channel_id = notification_channel_id
        self.api_token = api_token
        self.runner: web.AppRunner | None = None
        self.site: web.TCPSite | None = None
    def criar_aplicacao(self) -> web.Application:
        app = web.Application(middlewares=[criar_middleware_autenticacao(self.api_token)])
        app.router.add_get("/health", self.verificar_saude)
        app.router.add_get("/ready", self.verificar_prontidao)
        app.router.add_post("/notificacoes/teste", self.enviar_noticacao_de_teste)
        app.router.add_post("/notificacoes/promocoes-de-voo", self.enviar_promocao_de_voo)
        return app
    async def start(self) -> None:
        app = self.criar_aplicacao()
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        logger.info(f"API do Rayquaza iniciada em http://{self.host}:{self.port}")
    async def finalizar(self) -> None:
        if self.runner is None:
            return
        await self.runner.cleanup()
        self.runner = None
        self.site = None
        logger.info("API do Rayquaza finalizada.")
    async def verificar_saude(self, request: web.Request) -> web.Response:
        return web.json_response({"status": "online", "servico": "rayquaza-bot"})
    async def verificar_prontidao(self, request: web.Request) -> web.Response:
        if self.bot.is_ready():
            return web.json_response({"status": "ready", "servico": "rayquaza-bot", "discord": True})
        return web.json_response({"status": "not_ready", "servico": "rayquaza-bot", "discord": False}, status=503)
    async def enviar_noticacao_de_teste(self, request: web.Request) -> web.Response:
        try:
            dados = await request.json()
        except (ValueError, TypeError):
            return web.json_response({"erro": "tem q ser um json valido."}, status=400)
        mensagem = self.obter_mensagem(dados)
        if mensagem is None:
            return web.json_response({"erro": "o campo mensagem eh obrigatorio e tem q conter entre 1 e 2000 caracteres."}, status=400)
        try:
            canal = await self.obter_canal()
        except discord.DiscordException:
            logger.exception("nao foi possivel localizar o canal | canal_id=%s", self.notification_channel_id)
            return web.json_response({"erro": "nao foi possivel localizar o canal de notificacoes."}, status=500)
        if canal is None or not hasattr(canal, "send"):
            logger.error("o canal de notificacoes nao eh valido para enviar mensagens | canal_id=%s", self.notification_channel_id)
            return web.json_response({"erro": "o canal configurado nao aceita mensagens."}, status=500)
        try:
            await canal.send(mensagem)
        except discord.DiscordException:
            logger.exception("erro ao enviar notificacao | canal_id=%s", self.notification_channel_id)
            return web.json_response({"erro": "nao foi possível enviar a mensagem ao discord."}, status=500)
        logger.info("notificacao enviada com sucesso | canal_id=%s", self.notification_channel_id)
        return web.json_response({"status": "notificacao enviada com sucesso.", "canal_id": self.notification_channel_id})
    async def enviar_promocao_de_voo(self, request: web.Request) -> web.Response:
        try:
            dados = await request.json()
            promocao = PromocaoDeVoo(origem=dados["origem"],
                                     destino=dados["destino"],
                                     preco=float(dados["preco"]),
                                     moeda=dados["moeda"],
                                     companhia=dados["companhia"],
                                     numero_voo=dados["numero_voo"],
                                     quantidade_escalas=int(dados["quantidade_escalas"]),
                                     duracao_minutos=int(dados["duracao_minutos"]),
                                     horario_chegada=dados["horario_chegada"],
                                     horario_saida=dados["horario_saida"],
                                     link=dados["link"])
        except (KeyError, TypeError, ValueError):
            return web.json_response({"erro": "os dados de promocao de voo sao invalidos ou estao incompletos"}, status=400)
        canal = await self.obter_canal()
        if canal is None or not hasattr(canal, "send"):
            logger.error("o canal de notificacoes nao eh valido | canal_id %s", self.notification_channel_id)
            return web.json_response({"erro": "o canal configurado nao aceita mensagens"}, status=500)
        embed = criar_embed_promocao_de_voo(promocao)
        try:
            await canal.send(embed=embed)
        except discord.DiscordException:
            logger.exception("erro ao enviar promocao de voo | canal_id=%s", self.notification_channel_id)
            return web.json_response({"erro": "nao foi possivel enviar a promocao ao discord"}, status=500)
        logger.info("promocao de voo enviada com sucesso | rota=%s-%s | preco=%.2f | canal_id=%s", promocao.origem, promocao.destino, promocao.preco, self.notification_channel_id)
        return web.json_response({"status": "promocao de voo enviada com sucesso.", "canal_id": self.notification_channel_id})
    def obter_mensagem(self, dados: dict[str, Any]) -> str | None:
        if not isinstance(dados, dict):
            return None
        mensagem = dados.get("mensagem")
        if not isinstance(mensagem, str) or not (1 <= len(mensagem) <= 2000):
            return None
        return mensagem
    async def obter_canal(self) -> discord.abc.Messageable | None:
        canal = self.bot.get_channel(self.notification_channel_id)
        if canal is None:
            try:
                canal = await self.bot.fetch_channel(self.notification_channel_id)
            except discord.DiscordException:
                logger.exception("erro ao buscar o canal de notificacoes | canal_id=%s", self.notification_channel_id)
                return None
        return canal

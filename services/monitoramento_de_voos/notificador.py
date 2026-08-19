import asyncio
import logging

import aiohttp

from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.modelos import OfertaVoo


logger = logging.getLogger(__name__)


class NotificadorRayquaza:
    def __init__(self, configuracoes: ConfiguracoesMonitoramento) -> None:
        self.api_url = configuracoes.rayquaza_api_url.rstrip("/")
        self.api_token = configuracoes.api_token
        self.max_retries = configuracoes.max_retries

    async def enviar_oferta(self, oferta: OfertaVoo) -> None:
        url = f"{self.api_url}/notificacoes/promocoes-de-voo"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        dados_oferta = {
            "origem": oferta.origem,
            "destino": oferta.destino,
            "preco": oferta.preco,
            "moeda": oferta.moeda,
            "companhia": oferta.companhia,
            "numero_voo": oferta.numero_voo,
            "quantidade_escalas": oferta.quantidade_escalas,
            "duracao_minutos": oferta.duracao_minutos,
            "horario_saida": oferta.horario_saida,
            "horario_chegada": oferta.horario_chegada,
            "link": oferta.link,
        }

        for tentativa in range(self.max_retries + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=15)

                async with aiohttp.ClientSession(timeout=timeout) as sessao:
                    async with sessao.post(url, headers=headers, json=dados_oferta) as resposta:
                        dados = await resposta.json()

                        if resposta.status != 200:
                            erro = dados.get("erro", "erro desconhecido")
                            raise RuntimeError(f"Erro ao notificar o Rayquaza: {erro}")

                logger.info("Notificação enviada | rota=%s-%s", oferta.origem, oferta.destino)
                return

            except (asyncio.TimeoutError, aiohttp.ClientError) as erro:
                if tentativa >= self.max_retries:
                    logger.error("Notificação falhou | tentativas=%d | erro=%s", tentativa + 1, type(erro).__name__)
                    raise

                espera = 2 ** tentativa

                logger.warning("Erro ao notificar Rayquaza | tentativa=%d | aguardando=%ds | erro=%s", tentativa + 1, espera, type(erro).__name__)

                await asyncio.sleep(espera)

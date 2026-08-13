import logging

from services.monitoramento_de_voos.cliente_serpapi import ClienteSerpApi
from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.notificador import NotificadorRayquaza


logger = logging.getLogger(__name__)


class MonitoramentoDeVoos:
    def __init__(
        self,
        configuracoes: ConfiguracoesMonitoramento,
        cliente: ClienteSerpApi,
        notificador: NotificadorRayquaza,
    ) -> None:
        self.configuracoes = configuracoes
        self.cliente = cliente
        self.notificador = notificador

    async def executar(self) -> None:
        logger.info(
            "Monitoramento iniciado | rota=%s-%s | limite=%s",
            self.configuracoes.aeroporto_origem,
            self.configuracoes.aeroporto_destino,
            self.configuracoes.preco_maximo,
        )

        ofertas = await self.cliente.buscar_ofertas()

        if not ofertas:
            logger.warning("Nenhuma oferta encontrada")
            return

        menor_oferta = min(ofertas, key=lambda oferta: oferta.preco)

        logger.info(
            "Menor preço encontrado | preco=%s | companhia=%s",
            menor_oferta.preco,
            menor_oferta.companhia,
        )

        if menor_oferta.preco > self.configuracoes.preco_maximo:
            logger.info(
                "Preço acima do limite | encontrado=%s | limite=%s",
                menor_oferta.preco,
                self.configuracoes.preco_maximo,
            )
            return

        await self.notificador.enviar_oferta(menor_oferta)
import asyncio
import logging

from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.monitor import MonitoramentoDeVoos


logger = logging.getLogger(__name__)


class FlightMonitorWorker:
    def __init__(
        self,
        configuracoes: ConfiguracoesMonitoramento,
        monitoramento: MonitoramentoDeVoos,
    ) -> None:
        self.configuracoes = configuracoes
        self.monitoramento = monitoramento

    async def start(self) -> None:
        intervalo = self.configuracoes.intervalo_minutos * 60

        logger.info(
            "Worker iniciado | intervalo=%d min | timeout=%d s",
            self.configuracoes.intervalo_minutos,
            self.configuracoes.timeout_ciclo_segundos,
        )

        while True:
            try:
                await asyncio.wait_for(
                    self.monitoramento.executar(),
                    timeout=self.configuracoes.timeout_ciclo_segundos,
                )

            except asyncio.TimeoutError:
                logger.error(
                    "Monitoramento excedeu o timeout | timeout=%d s",
                    self.configuracoes.timeout_ciclo_segundos,
                )

            except Exception:
                logger.exception("Erro ao executar monitoramento")

            logger.info(
                "Próximo monitoramento em %d minutos",
                self.configuracoes.intervalo_minutos,
            )

            await asyncio.sleep(intervalo)